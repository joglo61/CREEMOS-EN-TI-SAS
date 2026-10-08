from datetime import date
from calendar import monthrange
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.models.prestamo import Prestamo
from app.models.cronograma import Cronograma
from app.models.log import Log
from app.models.configuracion import Configuracion
from app.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ClienteRepository(db)

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
                prestamo_id=prestamo_id,
                numero_cuota=num,
                fecha_estimada=fecha,
                capital_estimado=abono,
                interes_estimado=interes,
                valor_estimado=abono + interes,
                saldo_estimado=saldo_nuevo if saldo_nuevo >= 0 else Decimal("0"),
                estado="PENDIENTE",
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

    def _add_month(self, dt: date) -> date:
        month = dt.month + 1
        year = dt.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        last_day = monthrange(year, month)[1]
        day = min(dt.day, last_day)
        return date(year, month, day)

    def crear(self, nombre: str, cedula: str, placa: str, telefono: str | None, direccion: str | None, correo: str | None, observaciones: str | None, capital_inicial: Decimal, valor_cuota: Decimal, fecha_inicio: date, fecha_primer_pago: date | None = None, usuario_id: int | None = None, ip: str | None = None) -> dict:
        existing_cedula = self.repo.get_by_cedula(cedula)
        if existing_cedula:
            raise ValueError("Ya existe un cliente con esa cédula.")
        existing_placa = self.repo.get_by_placa(placa)
        if existing_placa:
            raise ValueError("Ya existe un cliente con esa placa.")

        tasa = self._get_tasa()
        if fecha_primer_pago is None:
            fecha_primer_pago = self._add_month(fecha_inicio)

        cliente = Cliente(
            nombre=nombre, cedula=cedula, placa=placa,
            telefono=telefono, direccion=direccion, correo=correo,
            observaciones=observaciones,
        )
        cliente = self.repo.create(cliente)

        prestamo = Prestamo(
            cliente_id=cliente.id,
            placa=placa,
            capital_inicial=capital_inicial,
            saldo_actual=capital_inicial,
            valor_cuota=valor_cuota,
            tasa_interes=tasa,
            fecha_inicio=fecha_inicio,
            fecha_primer_pago=fecha_primer_pago,
            fecha_proximo_pago=fecha_primer_pago,
            estado="ACTIVO",
        )
        self.db.add(prestamo)
        self.db.flush()

        cronogramas = self._generar_cronograma(prestamo.id, capital_inicial, valor_cuota, tasa, fecha_primer_pago)
        for c in cronogramas:
            self.db.add(c)

        self.db.commit()
        self.db.refresh(cliente)

        log = Log(
            usuario_id=usuario_id, accion="CREAR_CLIENTE", modulo="Clientes",
            descripcion=f"Cliente {nombre} ({cedula}) creado con préstamo ${capital_inicial}.",
            direccion_ip=ip,
        )
        self.db.add(log)
        self.db.commit()

        return {"cliente": cliente, "prestamo": prestamo, "cronograma": cronogramas}

    def actualizar(self, cliente_id: int, nombre: str | None, telefono: str | None, direccion: str | None, correo: str | None, observaciones: str | None, usuario_id: int | None = None, ip: str | None = None) -> Cliente:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado.")
        if nombre is not None:
            cliente.nombre = nombre
        if telefono is not None:
            cliente.telefono = telefono
        if direccion is not None:
            cliente.direccion = direccion
        if correo is not None:
            cliente.correo = correo
        if observaciones is not None:
            cliente.observaciones = observaciones
        self.repo.update(cliente)

        log = Log(
            usuario_id=usuario_id, accion="EDITAR_CLIENTE", modulo="Clientes",
            descripcion=f"Cliente {cliente.nombre} ({cliente.cedula}) editado.",
            direccion_ip=ip,
        )
        self.db.add(log)
        self.db.commit()

        return cliente

    def obtener_cronograma(self, cliente_id: int, page: int = 1, page_size: int = 360) -> dict:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado.")
        prestamo = cliente.prestamos[0] if cliente.prestamos else None
        if not prestamo:
            raise ValueError("El cliente no tiene préstamos.")
        query = self.db.query(Cronograma).where(Cronograma.prestamo_id == prestamo.id).order_by(Cronograma.numero_cuota)
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "prestamo_id": prestamo.id,
        }

    def obtener_historial(self, cliente_id: int, page: int = 1, page_size: int = 50) -> dict:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado.")
        like = f"%{cliente.cedula}%"
        query = self.db.query(Log).where(
            Log.descripcion.like(like),
        ).order_by(Log.created_at.desc())
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
