from sqlalchemy import Column, String, DateTime, func, Integer
from configs.database import Base
import uuid

class Asignatura(Base):

    __tablename__ = 'asignatura'

    id = Column(String(50), primary_key=True, default=uuid.uuid4().hex)
    nombre = Column(String(50), nullable=False)
    fecha_reg = Column(DateTime, default=func.current_timestamp())
    activo = Column(Integer, default = 1, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def to_dict(self):
        return {
            'nombre' : self.nombre
        }