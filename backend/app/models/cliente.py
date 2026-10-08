from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    placa = Column(String(20), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(300), nullable=True)
    correo = Column(String(100), nullable=True)
    estado = Column(String(20), nullable=False, default="ACTIVO", index=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    prestamos = relationship("Prestamo", back_populates="cliente", cascade="all, delete-orphan")
