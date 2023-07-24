from sqlalchemy import Column, String, ForeignKey, Integer
from configs.database import Base
import uuid

class CambioClave(Base):
    
    __tablename__ = 'cambio_clave'

    id = id = Column(String(50), primary_key=True, default=lambda: uuid.uuid4().hex)
    usuario_id = Column(String(50), ForeignKey('usuario.id'), nullable=False)
    codigo_verificacion = Column(Integer, nullable=False)
    used = Column(Integer, nullable=False, default = 0)


    def __init__(self, usuario_id, codigo_verificacion):
        self.usuario_id = usuario_id
        self.codigo_verificacion = codigo_verificacion