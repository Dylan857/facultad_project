from sqlalchemy import Column, String, ForeignKey, Table, Date, Time, Integer, DateTime, func
from sqlalchemy.orm import relationship
from configs.database import Base
import uuid

class Tutoria(Base): 

    __tablename__ = 'tutoria'

    id = Column(String(50), primary_key=True, default=lambda: uuid.uuid4().hex)
    docente_id = Column(String(50), ForeignKey('usuario.id'))
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    asignatura_id = Column(String(50), ForeignKey('asignatura.id'))
    activo = Column(Integer, default = 1, nullable=False)
    fecha_reg = Column(DateTime, default=func.current_timestamp())

    estudiantes = relationship('Usuario', secondary='estudiante_tutoria', backref='tutorias')

    estudiante_tutoria = Table('estudiante_tutoria', Base.metadata, Column('estudiante_id', String(50), ForeignKey('usuario.id')),
                               Column('tutoria_id', String(50), ForeignKey('tutoria.id')))

    def __init__(self, docente_id, fecha, hora_inicio, hora_fin, asignatura_id):
        self.docente_id = docente_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.asignatura_id = asignatura_id