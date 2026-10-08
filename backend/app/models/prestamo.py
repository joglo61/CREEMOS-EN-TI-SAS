from sqlalchemy import Column, Integer, Numeric, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    # Placa del taxi de ESTE préstamo (un cliente puede tener varios taxis/préstamos)
    placa = Column(String(20), nullable=True, index=True)
    capital_inicial = Column(Numeric(12, 0), nullable=False)
    saldo_actual = Column(Numeric(12, 0), nullable=False)
    valor_cuota = Column(Numeric(12, 0), nullable=False)
    tasa_interes = Column(Numeric(5, 2), nullable=False, default=2.5)
    fecha_inicio = Column(Date, nullable=False)
    fecha_primer_pago = Column(Date, nullable=False)
    fecha_proximo_pago = Column(Date, nullable=False, index=True)
    estado = Column(String(20), nullable=False, default="ACTIVO", index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    cliente = relationship("Cliente", back_populates="prestamos")
    pagos = relationship("Pago", back_populates="prestamo", cascade="all, delete-orphan")
    cronograma = relationship("Cronograma", back_populates="prestamo", cascade="all, delete-orphan")
