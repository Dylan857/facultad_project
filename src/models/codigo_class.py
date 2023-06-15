from sqlalchemy import Column, String, DateTime, func, Integer
from sqlalchemy.orm import relationship
from configs.database import Base
import uuid

class Codigo(Base):

    __tablename__ = "codigo_verificacion"

    id = Column(String(50), primary_key=True, default=lambda: uuid.uuid4().hex)
    codigo_access = Column(Integer, nullable=False)
    used = Column(Integer, nullable=False, default= 1)

    def __init__(self, codigo_access):
        self.codigo_access = codigo_access

    def to_dict(self):
        return {
            'id' : self.id,
            'codigo' : self.codigo_access,
            'used' : self.used
        }