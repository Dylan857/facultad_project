from sqlalchemy import Column, String, ForeignKey, Table, DateTime, func, Integer
from sqlalchemy.orm import relationship
from configs.database import Base
import uuid 

class Usuario(Base):
    
    __tablename__ = 'usuario'

    id = Column(String(50), primary_key=True, default=lambda: uuid.uuid4().hex)
    nombre = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    celular = Column(String(15), nullable=False)
    tipo_identificacion = Column(String(5), nullable=False)
    numero_identificacion = Column(String(15), nullable=False)
    password = Column(String(255), nullable=False)
    fecha_reg = Column(DateTime, default=func.current_timestamp())
    activo = Column(Integer, default = 1, nullable=False)

    carreras = relationship('Carrera', secondary='estudiante_carrera')
    asignaturas = relationship('Asignatura', secondary='docente_asignatura')
    roles = relationship('Rol', secondary='rol_usuario', back_populates='usuario')

    def __init__(self, nombre, email, celular, tipo_identificacion, numero_identificacion, password):
        self.nombre = nombre
        self.email = email
        self.celular = celular
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.password = password
        
    rol_usuario = Table('rol_usuario', Base.metadata, Column('rol_id', ForeignKey('rol.id')), 
                        Column('usuario_id', ForeignKey('usuario.id')))
    
    asignatura_docente = Table('docente_asignatura', Base.metadata, Column('docente_id', ForeignKey('usuario.id')), Column('asignatura_id', ForeignKey('asignatura.id')))

    carrera_estudiante = Table('estudiante_carrera', Base.metadata, Column('estudiante_id', ForeignKey('usuario.id')), Column('carrera_id', ForeignKey('carrera.id')))