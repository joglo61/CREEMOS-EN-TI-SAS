from __future__ import annotations
from datetime import date, datetime
from calendar import monthrange
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.prestamo import Prestamo
from app.models.pago import Pago
from app.models.factura import Factura
from app.models.cronograma import Cronograma
from app.models.log import Log
from app.models.configuracion import Configuracion
from app.repositories.pago_repository import PagoRepository


class PagoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PagoRepository(db)

    def _generar_numero_factura(self) -> str:
        config = self.db.query(Configuracion).first()
        num = config.siguiente_factura if config else 1
        factura = f"FACT-{num:06d}"
        if config:
            config.siguiente_factura = num + 1
        return factura

    def _calcular_intereses(self, saldo: Decimal, tasa: Decimal, dias: int) -> Decimal:
        return (saldo * tasa / Decimal("100") / Decimal("30") * Decimal(str(dias))).quantize(Decimal("1"))  # type: ignore

    def _calcular(self, prestamo_id: int, valor_pagado: Decimal, fecha_pago: date, aplicar_interes: bool = True, tasa_interes: Decimal | None = None) -> dict:
        prestamo = self.db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
        if not prestamo:
            raise ValueError("Préstamo no encontrado.")
        if prestamo.estado in ("PAGADO", "CANCELADO"):
            raise ValueError("El préstamo ya está cancelado o pagado.")

        ultimo_pago = self.repo.get_ultimo_pago(prestamo_id)
        if ultimo_pago:
            prox = prestamo.fecha_proximo_pago
            month = prox.month - 1
            year = prox.year
            if month < 1:
                month = 12
                year -= 1
            last_day = monthrange(year, month)[1]
            day = min(prox.day, last_day)
            fecha_desde = date(year, month, day)
        else:
            fecha_desde = min(prestamo.fecha_inicio, prestamo.fecha_proximo_pago)

        if fecha_pago < fecha_desde:
            raise ValueError("La fecha de pago no puede ser anterior a la fecha de inicio del período.")

        fecha_proximo = prestamo.fecha_proximo_pago
        dias_mora = (fecha_pago - fecha_proximo).days if fecha_pago > fecha_proximo else 0
        dias_base = 30
        dias_calculados = dias_base + dias_mora

        saldo_anterior = prestamo.saldo_actual
        tasa = tasa_interes if tasa_interes is not None else prestamo.tasa_interes

        if not aplicar_interes:
            intereses = Decimal("0")
            intereses_mora = Decimal("0")
        else:
            intereses = self._calcular_intereses(saldo_anterior, tasa, dias_base)
            intereses_mora = self._calcular_intereses(valor_pagado, tasa, dias_mora) if dias_mora >= 5 else Decimal("0")

        intereses_totales = intereses + intereses_mora

        if not aplicar_interes or valor_pagado < intereses:
            capital = valor_pagado if not aplicar_interes else Decimal("0")
            intereses = Decimal("0") if not aplicar_interes else valor_pagado
            intereses_mora = Decimal("0")
        elif valor_pagado < intereses_totales:
            capital = Decimal("0")
            intereses_mora = valor_pagado - intereses
            intereses_totales = valor_pagado
        else:
            capital = valor_pagado - intereses_totales

        if capital > saldo_anterior:
            capital = saldo_anterior

        saldo_nuevo = saldo_anterior - capital
        if saldo_nuevo < Decimal("0"):
            saldo_nuevo = Decimal("0")

        tasa_aplicada = tasa if aplicar_interes else Decimal("0")

        return {
            "prestamo_id": prestamo_id,
            "valor_pagado": valor_pagado,
            "fecha_pago": fecha_pago,
            "dias_calculados": dias_calculados,
            "dias_mora": dias_mora,
            "saldo_anterior": saldo_anterior,
            "intereses": intereses,
            "intereses_mora": intereses_mora,
            "intereses_totales": intereses_totales,
            "capital": capital,
            "saldo_nuevo": saldo_nuevo,
            "aplicar_interes": aplicar_interes,
            "tasa_interes_aplicada": tasa_aplicada,
        }

    def calcular(self, prestamo_id: int, valor_pagado: Decimal, fecha_pago: date, aplicar_interes: bool = True, tasa_interes: Decimal | None = None) -> dict:
        return self._calcular(prestamo_id, valor_pagado, fecha_pago, aplicar_interes=aplicar_interes, tasa_interes=tasa_interes)

    def registrar(self, prestamo_id: int, valor_pagado: Decimal, fecha_pago: date, observaciones: str | None = None, usuario_id: int | None = None, ip: str | None = None, aplicar_interes: bool = True, tasa_interes: Decimal | None = None) -> dict:
        calculo = self._calcular(prestamo_id, valor_pagado, fecha_pago, aplicar_interes=aplicar_interes, tasa_interes=tasa_interes)
        prestamo = self.db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
        saldo_anterior = calculo["saldo_anterior"]
        intereses = calculo["intereses"]
        intereses_mora = calculo["intereses_mora"]
        capital = calculo["capital"]
        saldo_nuevo = calculo["saldo_nuevo"]
        dias_calculados = calculo["dias_calculados"]
        dias_mora = calculo["dias_mora"]
        tasa_aplicada = calculo["tasa_interes_aplicada"]

        numero_factura = self._generar_numero_factura()

        pago = Pago(
            prestamo_id=prestamo_id, numero_factura=numero_factura, fecha_pago=fecha_pago,
            dias_calculados=dias_calculados, dias_mora=dias_mora,
            saldo_anterior=saldo_anterior, intereses=intereses, intereses_mora=intereses_mora,
            capital=capital, valor_pagado=valor_pagado, saldo_nuevo=saldo_nuevo,
            observaciones=observaciones, usuario_id=usuario_id,
            tasa_interes_aplicada=tasa_aplicada,
        )
        self.repo.create(pago)

        # Mark cronograma entries as PAGADO (up to abono amount)
        cronos = self.db.query(Cronograma).filter(
            Cronograma.prestamo_id == prestamo_id, Cronograma.estado == "PENDIENTE",
        ).order_by(Cronograma.numero_cuota).all()
        pending = capital
        for c in cronos:
            if pending <= Decimal("0"):
                break
            if c.capital_estimado <= pending:
                c.estado = "PAGADO"
                pending -= c.capital_estimado
            else:
                c.capital_estimado -= pending
                pending = Decimal("0")

        prestamo.saldo_actual = saldo_nuevo
        next_month = prestamo.fecha_proximo_pago.month + 1
        year = prestamo.fecha_proximo_pago.year
        if next_month > 12:
            next_month = 1
            year += 1
        last_day = monthrange(year, next_month)[1]
        day = min(prestamo.fecha_proximo_pago.day, last_day)
        prestamo.fecha_proximo_pago = date(year, next_month, day)

        if saldo_nuevo <= Decimal("0"):
            prestamo.estado = "PAGADO"

        self.db.commit()

        factura = Factura(
            numero_factura=numero_factura, cliente_id=prestamo.cliente_id,
            pago_id=pago.id, fecha=fecha_pago, estado="EMITIDA",
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(pago)

        log = Log(
            usuario_id=usuario_id, accion="REGISTRAR_PAGO", modulo="Motor Financiero",
            descripcion=f"Pago ${valor_pagado} registrado para préstamo #{prestamo_id}. Factura {numero_factura}.",
            direccion_ip=ip,
        )
        self.db.add(log)
        self.db.commit()

        return {"pago": pago, "factura": factura}
