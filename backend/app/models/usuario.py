from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    rol = Column(String(20), nullable=False, default="EMPLEADO")
    activo = Column(Boolean, nullable=False, default=True)
    intentos_fallidos = Column(Integer, nullable=False, default=0)
    bloqueado_hasta = Column(DateTime, nullable=True)
    ultimo_acceso = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    pagos = relationship("Pago", back_populates="usuario")
    logs = relationship("Log", back_populates="usuario")
    archivos = relationship("Archivo", back_populates="usuario")
    backups = relationship("Backup", back_populates="usuario")
