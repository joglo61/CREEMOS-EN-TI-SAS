from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Date, Text, func
from sqlalchemy.orm import declarative_base

BaseCartera = declarative_base()


class ClienteCartera(BaseCartera):
    __tablename__ = "clientes_cartera"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(300), nullable=False, index=True)
    telefono = Column(String(100), nullable=True)
    cedula = Column(String(20), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Credito(BaseCartera):
    __tablename__ = "creditos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20), nullable=False, index=True)
    sufijo_credito = Column(String(10), nullable=False, default="")
    cliente_id = Column(Integer, nullable=True)
    valor_credito = Column(Numeric(14, 0), nullable=True)
    valor_cuota = Column(Numeric(14, 0), nullable=True)
    fecha_desembolso = Column(Date, nullable=True)
    plazo_meses = Column(Integer, nullable=True)
    prenda = Column(String(50), nullable=True)
    tiene_historial_detallado = Column(Boolean, nullable=False, default=True)
    activo = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())


class PagoHistorico(BaseCartera):
    __tablename__ = "pagos_historicos"

    id = Column(Integer, primary_key=True, index=True)
    credito_id = Column(Integer, nullable=False, index=True)
    numero_pago = Column(Integer, nullable=True)
    recibo = Column(String(50), nullable=True)
    fecha_ultimo_pago = Column(Date, nullable=True)
    fecha_pago = Column(Date, nullable=True)
    dias = Column(Integer, nullable=True)
    cuota = Column(Numeric(14, 0), nullable=True)
    interes = Column(Numeric(14, 0), nullable=True)
    saldo_intereses = Column(Numeric(14, 0), nullable=True)
    capital = Column(Numeric(14, 0), nullable=True)
    saldo_real = Column(Numeric(14, 0), nullable=True)
    fuente = Column(String(20), nullable=False, default="excel_creemos")
    actualizado_en = Column(DateTime, server_default=func.now())


class SnapshotMensual(BaseCartera):
    __tablename__ = "snapshots_mensuales"

    id = Column(Integer, primary_key=True, index=True)
    credito_id = Column(Integer, nullable=True, index=True)
    placa_textual = Column(String(20), nullable=True)
    mes_reportado = Column(String(20), nullable=False)
    numero_bloque = Column(Integer, nullable=True)
    pago_del_mes = Column(Boolean, nullable=True, default=False)
    fecha_original = Column(Date, nullable=True)
    vr_credito = Column(Numeric(14, 0), nullable=True)
    vr_cuota = Column(Numeric(14, 0), nullable=True)
    saldo_anterior = Column(Numeric(14, 0), nullable=True)
    fecha_inicial = Column(Date, nullable=True)
    fecha_final = Column(Date, nullable=True)
    dias = Column(Integer, nullable=True)
    intereses = Column(Numeric(14, 0), nullable=True)
    interes_mora = Column(Numeric(14, 0), nullable=True)
    abono_capital = Column(Numeric(14, 0), nullable=True)
    cuota = Column(Numeric(14, 0), nullable=True)
    saldo_final = Column(Numeric(14, 0), nullable=True)
    origen_archivo = Column(String(20), nullable=False)
    actualizado_en = Column(DateTime, server_default=func.now())
