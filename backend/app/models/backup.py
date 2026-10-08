from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Backup(Base):
    __tablename__ = "backups"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(30), nullable=False)
    archivo = Column(String(300), nullable=False)
    ruta = Column(String(500), nullable=False)
    tamano = Column(BigInteger, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="backups")
