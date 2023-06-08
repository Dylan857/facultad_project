from sqlalchemy import Column, String, DateTime, func, Integer
from sqlalchemy.orm import relationship
from configs.database import Base
import uuid

class Rol(Base):

    __tablename__ = "rol"

    id = Column(String(50), primary_key=True, default=uuid.uuid4().hex)
    rol = Column(String(50))
    fecha_reg = Column(DateTime, default=func.current_timestamp())
    activo = Column(Integer, default = 1, nullable=False)
    usuario = relationship('Usuario', secondary='rol_usuario', back_populates='roles')

    def __init__(self, id, rol):
        self.id = id
        self.rol = rol

    def to_dict(self):
        return {
            'rol' : self.rol
        }