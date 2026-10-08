from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), nullable=False, index=True)
    nombre_original = Column(String(300), nullable=False)
    nombre_interno = Column(String(300), nullable=False)
    ruta = Column(String(500), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    fecha_carga = Column(DateTime, server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    activo = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="archivos")
