from sqlalchemy import Column, String, DateTime, func
from configs.database import Base
import uuid 

class Carrera(Base):

    __tablename__ = "carrera"

    id = Column(String(50), primary_key=True, default=lambda: uuid.uuid4().hex)
    nombre = Column(String(50), nullable=True)
    fecha_reg = Column(DateTime, default=func.current_timestamp())

    def __init__(self, nombre):
        self.nombre = nombre

    def to_dict(self):
        return {
            'nombre' : self.nombre
        }