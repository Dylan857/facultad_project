from flask import current_app, render_template
from repository.repository_interface.solicitud_repo import SolicitudRepository
from models.solicitud_class import Solicitud
from configs.database import Database
from models.usuarios_class import Usuario
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Message
from sqlalchemy import and_
from email.utils import formataddr

db = Database()

class SolicitudRepositoryImpl(SolicitudRepository):
    def get_solicitudes(self):
        session = db.get_session()
        estudiante_alias = aliased(Usuario)
        join_estudiante = session.query(Solicitud).join(estudiante_alias, Solicitud.estudiante_id == estudiante_alias.id)
        docente_alias = aliased(Usuario)
        join_docente = join_estudiante.join(docente_alias, Solicitud.docente_id == docente_alias.id)
        query = join_docente.add_columns(estudiante_alias, docente_alias)
        results = query.all()

        solicitudes_list = []

        for solicitud, usuario, docente in results:
            solicitud_dict = {
                'id' : f'{solicitud.id}',
                'estudiante' : f'{usuario.nombre}',
                'docente' : f'{docente.nombre}'
            }
            solicitudes_list.append(solicitud_dict)
        session.close()
        return solicitudes_list
    
    def get_solicitud_by_docente(self, id):
        session = db.get_session()
        estudiante_alias = aliased(Usuario)
        join_estudiante = session.query(Solicitud).join(estudiante_alias, Solicitud.estudiante_id == estudiante_alias.id)
        docente_alias = aliased(Usuario)
        join_docente = join_estudiante.join(docente_alias, Solicitud.docente_id == docente_alias.id)
        query = join_docente.add_columns(estudiante_alias, docente_alias).filter(Solicitud.docente_id == id)
        results = query.all()

        solicitudes_list = []

        for solicitud, usuario, docente in results:
            solicitud_dict = {
                'id' : f'{solicitud.id}',
                'estudiante' : f'{usuario.nombre}',
                'docente' : f'{docente.nombre}'
            }
            solicitudes_list.append(solicitud_dict)
        session.close()
        return solicitudes_list
    
    def make_a_request(self, cedula_estudiante, cedula_docente, descripcion_solicitud):
        session = db.get_session()
        try:

            estudiante = session.query(Usuario).filter(and_(Usuario.numero_identificacion == cedula_estudiante, Usuario.activo == 1)).first()
            docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == cedula_docente, Usuario.activo == 1)).first()
            if estudiante == None:
                return estudiante
            elif docente == None:
                return docente
            
            solicitud = Solicitud(estudiante.id, docente.id, descripcion_solicitud)
            session.add(solicitud)
            session.commit()

            mail = current_app.extensions['mail']
            msg = Message("Solicitud de tutoria", sender = formataddr(("Tutorias ingenieria", "tutoriasingenierias@gmail.com")), recipients=[docente.email])
            msg.html = render_template("solicitud.html", docente = docente.nombre, estudiante_email = estudiante.email, estudiante = estudiante.nombre, descripcion_solicitud = descripcion_solicitud)
            mail.send(msg)
            session.close()
            return True
        except SQLAlchemyError as e:
            print(f'Error al hacer la solicitud: {str(e)}')
            return False