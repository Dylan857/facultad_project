from sqlalchemy import Column, String, ForeignKey, DateTime, func, Integer
from configs.database import Base
from sqlalchemy.orm import relationship
import uuid

class Solicitud(Base):

    __tablename__ = 'solicitud'

    id = Column(String(50), primary_key=True, default=lambda: uuid.uuid4().hex)
    estudiante_id = Column(String(50), ForeignKey('usuario.id'))
    docente_id = Column(String(50), ForeignKey('usuario.id'))
    descripcion_solicitud = Column(String(255), nullable=False)
    activo = Column(Integer, default = 1, nullable=False)
    fecha_reg = Column(DateTime, default=func.current_timestamp())

    estudiante = relationship('Usuario', foreign_keys=[estudiante_id])
    docente = relationship('Usuario', foreign_keys=[docente_id])

    def __init__(self, estudiante_id, docente_id, descripcion_solicitud):
        self.docente_id = docente_id
        self.estudiante_id = estudiante_id
        self.descripcion_solicitud = descripcion_solicitud

    def to_dict(self):
        return {
            'id' : self.id,
            'estudiante' : self.estudiante_id,
            'docente' : self.docente_id,
            'descripcion_solicitud' : self.descripcion_solicitud
        }
