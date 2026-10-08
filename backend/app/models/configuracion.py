from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from app.database.database import Base


class Configuracion(Base):
    __tablename__ = "configuracion"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String(200), nullable=False, default="CREEMOS EN TI SAS")
    nit = Column(String(20), nullable=False, default="")
    direccion = Column(String(300), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True)
    logo = Column(String(500), nullable=True)
    tasa_interes = Column(Numeric(5, 2), nullable=False, default=2.5)
    dias_gracia = Column(Integer, nullable=False, default=5)
    siguiente_factura = Column(Integer, nullable=False, default=1)
    ruta_recibos = Column(String(500), nullable=False, default="./recibos")
    ruta_backups = Column(String(500), nullable=False, default="./backups")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
