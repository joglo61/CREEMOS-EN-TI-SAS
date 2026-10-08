from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    accion = Column(String(100), nullable=False)
    modulo = Column(String(50), nullable=True, index=True)
    descripcion = Column(Text, nullable=True)
    direccion_ip = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    usuario = relationship("Usuario", back_populates="logs")
