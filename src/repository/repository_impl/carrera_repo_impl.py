from repository.repository_interface.carrera_repo import CarreraRepo
from configs.database import Database
from models.carrera_class import Carrera

db = Database()
class CarreraRepoImpl(CarreraRepo):
    
    def get_carreras(self):
        session = db.get_session()
        carreras = session.query(Carrera).filter(Carrera.activo == 1).all()
        carreras_dict = [carrera.to_dict() for carrera in carreras]

        return carreras_dict