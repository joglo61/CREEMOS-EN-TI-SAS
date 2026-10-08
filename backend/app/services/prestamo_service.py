from __future__ import annotations
from datetime import date
from calendar import monthrange
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.prestamo import Prestamo
from app.models.cliente import Cliente
from app.models.cronograma import Cronograma
from app.models.log import Log
from app.models.configuracion import Configuracion
from app.repositories.prestamo_repository import PrestamoRepository


class PrestamoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PrestamoRepository(db)

    def _add_month(self, dt: date) -> date:
        month = dt.month + 1
        year = dt.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        last_day = monthrange(year, month)[1]
        day = min(dt.day, last_day)
        return date(year, month, day)

    def _get_tasa(self) -> Decimal:
        config = self.db.query(Configuracion).first()
        return Decimal(str(config.tasa_interes)) if config else Decimal("2.5")

    def _generar_cronograma(self, prestamo_id: int, capital: Decimal, valor_cuota: Decimal, tasa: Decimal, primer_pago: date) -> list[Cronograma]:
        entries = []
        saldo = capital
        num = 1
        fecha = primer_pago
        while saldo > 0 and num <= 360:
            interes = (saldo * tasa / Decimal("100")).quantize(Decimal("1"))
            abono = valor_cuota - interes
            if abono <= Decimal("0"):
                abono = Decimal("0")
                saldo_nuevo = saldo
            elif abono >= saldo:
                abono = saldo
                saldo_nuevo = Decimal("0")
            else:
                saldo_nuevo = saldo - abono
            entries.append(Cronograma(
                prestamo_id=prestamo_id, numero_cuota=num, fecha_estimada=fecha,
                capital_estimado=abono, interes_estimado=interes, valor_estimado=abono + interes,
                saldo_estimado=saldo_nuevo if saldo_nuevo >= 0 else Decimal("0"), estado="PENDIENTE",
            ))
            saldo = saldo_nuevo
            num += 1
            next_month = fecha.month + 1
            year = fecha.year
            if next_month > 12:
                next_month = 1
                year += 1
            last_day = monthrange(year, next_month)[1]
            day = min(fecha.day, last_day)
            fecha = date(year, next_month, day)
        return entries

    def crear(self, cliente_id: int, capital_inicial: Decimal, valor_cuota: Decimal, fecha_inicio: date, fecha_primer_pago: date | None = None, usuario_id: int | None = None, ip: str | None = None) -> dict:
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError("Cliente no encontrado.")
        activo = self.db.query(Prestamo).filter(Prestamo.cliente_id == cliente_id, Prestamo.estado.in_(["ACTIVO", "MORA"])).first()
        if activo:
            raise ValueError("El cliente ya tiene un préstamo activo.")

        tasa = self._get_tasa()
        if fecha_primer_pago is None:
            fecha_primer_pago = self._add_month(fecha_inicio)
        prestamo = Prestamo(
            cliente_id=cliente_id, capital_inicial=capital_inicial, saldo_actual=capital_inicial,
            valor_cuota=valor_cuota, tasa_interes=tasa, fecha_inicio=fecha_inicio,
            fecha_primer_pago=fecha_primer_pago, fecha_proximo_pago=fecha_primer_pago, estado="ACTIVO",
        )
        prestamo = self.repo.create(prestamo)

        cronogramas = self._generar_cronograma(prestamo.id, capital_inicial, valor_cuota, tasa, fecha_primer_pago)
        for c in cronogramas:
            self.db.add(c)
        self.db.commit()
        self.db.refresh(prestamo)

        log = Log(
            usuario_id=usuario_id, accion="CREAR_PRESTAMO", modulo="Prestamos",
            descripcion=f"Préstamo ${capital_inicial} creado para cliente {cliente.nombre} ({cliente.cedula}).",
            direccion_ip=ip,
        )
        self.db.add(log)
        self.db.commit()
        return {"prestamo": prestamo, "cronograma": cronogramas}

    def actualizar_estado_automatico(self, prestamo: Prestamo) -> str:
        hoy = date.today()
        if prestamo.saldo_actual <= Decimal("0"):
            prestamo.estado = "PAGADO"
        elif prestamo.fecha_proximo_pago and hoy > prestamo.fecha_proximo_pago:
            config = self.db.query(Configuracion).first()
            dias_gracia = config.dias_gracia if config else 5
            diff = (hoy - prestamo.fecha_proximo_pago).days
            if diff > dias_gracia:
                prestamo.estado = "MORA"
            else:
                prestamo.estado = "ACTIVO"
        else:
            prestamo.estado = "ACTIVO"
        self.repo.update(prestamo)
        return prestamo.estado

    def actualizar(self, prestamo_id: int, valor_cuota: Decimal | None = None, estado: str | None = None, usuario_id: int | None = None, ip: str | None = None) -> Prestamo:
        prestamo = self.repo.get_by_id(prestamo_id)
        if not prestamo:
            raise ValueError("Préstamo no encontrado.")
        if valor_cuota is not None:
            prestamo.valor_cuota = valor_cuota
        if estado is not None:
            prestamo.estado = estado
        self.repo.update(prestamo)
        self.db.commit()

        log = Log(
            usuario_id=usuario_id, accion="EDITAR_PRESTAMO", modulo="Prestamos",
            descripcion=f"Préstamo #{prestamo.id} actualizado.",
            direccion_ip=ip,
        )
        self.db.add(log)
        self.db.commit()
        return prestamo
