from sqlalchemy import Column, Integer, Numeric, String, Date, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"), nullable=False, index=True)
    numero_factura = Column(String(20), unique=True, nullable=False, index=True)
    fecha_pago = Column(Date, nullable=False, index=True)
    dias_calculados = Column(Integer, nullable=False)
    dias_mora = Column(Integer, nullable=False, default=0)
    saldo_anterior = Column(Numeric(12, 0), nullable=False)
    intereses = Column(Numeric(12, 0), nullable=False)
    intereses_mora = Column(Numeric(12, 0), nullable=False, default=0)
    capital = Column(Numeric(12, 0), nullable=False)
    valor_pagado = Column(Numeric(12, 0), nullable=False)
    saldo_nuevo = Column(Numeric(12, 0), nullable=False)
    observaciones = Column(Text, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tasa_interes_aplicada = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    prestamo = relationship("Prestamo", back_populates="pagos")
    usuario = relationship("Usuario", back_populates="pagos")
    factura = relationship("Factura", back_populates="pago", uselist=False, cascade="all, delete-orphan")
