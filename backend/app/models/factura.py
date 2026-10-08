from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(20), unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    pago_id = Column(Integer, ForeignKey("pagos.id"), nullable=False, unique=True)
    fecha = Column(Date, nullable=False, index=True)
    ruta_pdf = Column(String(500), nullable=True)
    estado = Column(String(20), nullable=False, default="EMITIDA")
    created_at = Column(DateTime, server_default=func.now())

    cliente = relationship("Cliente")
    pago = relationship("Pago", back_populates="factura")
