from repository.repository_interface.asignatura_repo import AsignaturaRepo
from configs.database import Database
from models.asignatura_class import Asignatura

db = Database()
class AsignaturaRepoImpl(AsignaturaRepo):

    def get_asignaturas(self):
        session = db.get_session()

        asignaturas = session.query(Asignatura).filter(Asignatura.activo == 1).all()

        asignaturas_dict = [asignatura.to_dict() for asignatura in asignaturas]

        return asignaturas_dict
