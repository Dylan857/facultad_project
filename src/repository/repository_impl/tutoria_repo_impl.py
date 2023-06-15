from repository.repository_interface.tutoria_repo import TutoriaRepo
from configs.database import Database
from models.tutoria_class import Tutoria
from models.usuarios_class import Usuario
from models.asignatura_class import Asignatura
from sqlalchemy.exc import DataError

db = Database()

class TutoriaRepoImpl(TutoriaRepo):

    def create_tutoria(self, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):

        try:
            
            session = db.get_session()

            docente_valido = self.validar_docente(docente_id)

            if docente_valido:
                return docente_valido
            
            estudiante_valido = self.validar_estudiantes(estudiantes)

            if estudiante_valido:
                return estudiante_valido

            docente = session.query(Usuario).filter(Usuario.id == docente_id and Tutoria.activo == 1).first()

            new_tutoria = Tutoria(docente.id, fecha, hora_inicio, hora_fin, asignatura_id)

            for estudiante in estudiantes:
                estudiante = session.query(Usuario).filter(Usuario.id == estudiante and Usuario.activo == 1).first()
                new_tutoria.estudiantes.append(estudiante)
            
            session.add(new_tutoria)
            session.commit()
            session.close()

            return True
        except DataError as e:
            raise e
    
    def get_tutorias(self):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(Tutoria.activo == 1).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        return tutorias_list
    
    def find_tutoria_by_docente(self, documento_docente):
        session = db.get_session()
        docente = session.query(Usuario).filter(Usuario.numero_identificacion == documento_docente and Usuario.activo == 1).first()
        tutorias = session.query(Tutoria).filter(Tutoria.docente_id == docente.id and Tutoria.activo == 1).all()

        tutorias_list = self.tutorias_to_dict(tutorias)

        return tutorias_list
    
    def find_tutoria_by_fecha(self, fecha):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(Tutoria.fecha == fecha and Tutoria.activo == 1).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        return tutorias_list
    
    def find_tutoria_by_asignatura(self, asignatura):
        session = db.get_session()
        asignatura = session.query(Asignatura).filter(Asignatura.nombre == asignatura and Asignatura.activo == 1).first()
        tutorias = session.query(Tutoria).filter(Tutoria.asignatura_id == asignatura.id and Tutoria.activo == 1).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        return tutorias_list
    

    def get_estudiantes(self, estudiantes):
        estudiantes_list = []
        for estudiante in estudiantes:
            estudiante_dict = {
                'nombre' : estudiante.nombre,
                'tipo_identificacion' : estudiante.tipo_identificacion,
                'numero_identificacion' : estudiante.numero_identificacion
                }
            estudiantes_list.append(estudiante_dict)
        return estudiantes_list
    
    def get_docente(self, docente_id):
        session = db.get_session()
        docente = session.query(Usuario).filter(Usuario.id == docente_id and Usuario.activo == 1).first()
        docente_list = []
        docente_dict = {
            'nombre' : docente.nombre,
            'tipo_identificacion' : docente.tipo_identificacion,
            'numero_identificacion' : docente.numero_identificacion
        }
        docente_list.append(docente_dict)

        return docente_list
    
    def get_asignatura(self, asignatura_id):

        session = db.get_session()
        asignatura_list = []
        asignatura = session.query(Asignatura).filter(Asignatura.id == asignatura_id and Asignatura.activo == 1).first()
        asignatura_list.append(asignatura.to_dict())
        return asignatura_list
    

    def tutorias_to_dict(self, tutorias):
        tutorias_list = []

        for tutoria in tutorias:
            estudiantes_list = self.get_estudiantes(tutoria.estudiantes)

            docente_list = self.get_docente(tutoria.docente_id)

            asignatura_list = self.get_asignatura(tutoria.asignatura_id)

            tutorias_dict = {
                'id' : tutoria.id,
                'fecha' : str(tutoria.fecha),
                'hora_inicio' : str(tutoria.hora_inicio),
                'hora_fin' : str(tutoria.hora_fin),
                'docente' : docente_list,
                'estudiantes' : estudiantes_list,
                'asignatura' : asignatura_list
            }
            tutorias_list.append(tutorias_dict)
        
        return tutorias_list
    
    def update_tutoria(self, id, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):

        try:       
            session = db.get_session()

            tutoria = session.query(Tutoria).filter(Tutoria.id == id).first()

            if tutoria:
                tutoria.asignatura_id = docente_id
                tutoria.fecha = fecha
                tutoria.hora_inicio = hora_inicio
                tutoria.hora_fin = hora_fin
                tutoria.asignatura_id = asignatura_id

                for estudiante in estudiantes:
                    estudiante_encontrado = session.query(Usuario).filter(Usuario.id == estudiante and Usuario.activo == 1).first()
                    tutoria.estudiantes.append(estudiante_encontrado)
                
                session.commit()
                session.close()

                return True
            else:
                return False
        except DataError as e:
            raise e
            
    def delete_tutoria(self, id):

        session = db.get_session()

        tutoria = session.query(Tutoria).filter(Tutoria.id == id and Tutoria.activo == 1).first()

        if tutoria:
            tutoria.activo = 0
            session.commit()
            session.close()
            return True
        else:
            return False
        
    def validar_docente(self, docente_id):
        session = db.get_session()

        docente = session.query(Usuario).filter(Usuario.id == docente_id and Usuario.activo == 1).first()

        if docente == None:
            error = "docente no encontrado"
            return error
        

    def validar_estudiantes(self, estudiantes):
        session = db.get_session()

        for estudiante in estudiantes:
            estudiante_encontrado = session.query(Usuario).filter(Usuario.id == estudiante).first()

            if estudiante_encontrado == None:
                error = "Estudiantes no validos"
                return error