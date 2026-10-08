from sqlalchemy import Column, Integer, Numeric, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Cronograma(Base):
    __tablename__ = "cronograma"

    id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"), nullable=False, index=True)
    numero_cuota = Column(Integer, nullable=False)
    fecha_estimada = Column(Date, nullable=False)
    capital_estimado = Column(Numeric(12, 0), nullable=False)
    interes_estimado = Column(Numeric(12, 0), nullable=False)
    valor_estimado = Column(Numeric(12, 0), nullable=False)
    saldo_estimado = Column(Numeric(12, 0), nullable=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    created_at = Column(DateTime, server_default=func.now())

    prestamo = relationship("Prestamo", back_populates="cronograma")
