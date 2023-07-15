from flask import current_app, render_template
from flask_mail import Message
from repository.repository_interface.tutoria_repo import TutoriaRepo
from configs.database import Database
from models.tutoria_class import Tutoria
from models.usuarios_class import Usuario
from models.asignatura_class import Asignatura
from sqlalchemy.exc import DataError
from sqlalchemy import and_, func
from datetime import date

db = Database()

class TutoriaRepoImpl(TutoriaRepo):

    def create_tutoria(self, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id, tema_desarrollar):

        try:
            
            session = db.get_session()

            emails = []
            docente_valido = self.validar_docente(docente_id)

            if docente_valido:
                return docente_valido
            
            estudiante_valido = self.validar_estudiantes(estudiantes)

            if estudiante_valido:
                return estudiante_valido
            
            asignatura_valido = self.validar_asignatura(asignatura_id)

            if asignatura_valido:
                return asignatura_valido
            
            asignatura = session.query(Asignatura).filter(and_(Asignatura.id == asignatura_id, Asignatura.activo == 1)).first()

            docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == docente_id, Usuario.activo == 1)).first()

            new_tutoria = Tutoria(docente.id, fecha, hora_inicio, hora_fin, asignatura_id, tema_desarrollar)

            for estudiante in estudiantes:
                estudiante = session.query(Usuario).filter(and_(Usuario.numero_identificacion == estudiante, Usuario.activo == 1)).first()
                new_tutoria.estudiantes.append(estudiante)
                emails.append(estudiante.email)
            
            session.add(new_tutoria)

            session.commit()

            hora_inicio_12h = self.hora_12h(new_tutoria.hora_inicio)
            hora_fin_12h = self.hora_12h(new_tutoria.hora_fin)
            fecha_formateada = self.fecha_formateada(new_tutoria.fecha)

            mail = current_app.extensions['mail']
            msg_estudiante = Message("Tutoria agendada", sender = "tutoriasingenierias@gmail.com", recipients=emails)
            msg_estudiante.html = render_template("agendado_tutoria.html", docente = docente.nombre, hora_inicio = hora_inicio_12h, hora_fin = hora_fin_12h, fecha = fecha_formateada, asignatura = asignatura.nombre)
            mail.send(msg_estudiante)

            msg_docente = Message("Tutoria agendada", sender="Tutorias ingenierias", recipients=[docente.email])
            msg_docente.html = render_template("agendado_tutoria_docente.html", docente = docente.nombre, hora_inicio = hora_inicio_12h, hora_fin = hora_fin_12h, fecha = fecha_formateada, asignatura = asignatura.nombre, estudiantes=new_tutoria.estudiantes)
            mail.send(msg_docente)
            session.close()

            return True
        except DataError as e:
            raise e
        
    def hora_12h(self, hora):
        hora_12h = hora.strftime("%I:%M %p")
        return hora_12h
    
    def fecha_formateada(self, fecha):
        fecha_formateada = fecha.strftime("%d/%m/%Y")        
        return fecha_formateada

    
    def get_tutorias(self):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(Tutoria.activo == 1).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def find_tutoria_by_docente(self, documento_docente):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()

        if docente == None:
            error = None
            return error
        
        tutorias = session.query(Tutoria).filter(and_(Tutoria.docente_id == docente.id, Tutoria.activo == 1)).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def find_tutoria_by_fecha(self, fecha):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.fecha == fecha, Tutoria.activo == 1)).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def find_tutoria_by_asignatura(self, asignatura):
        session = db.get_session()
        asignatura = session.query(Asignatura).filter(and_(Asignatura.nombre == asignatura, Asignatura.activo == 1)).first()

        if asignatura == None:
            error = None
            return error
        
        tutorias = session.query(Tutoria).filter(and_(Tutoria.asignatura_id == asignatura.id, Tutoria.activo == 1)).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def find_tutoria_by_docente_asignatura(self, documento_docente, asignatura):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        asignatura = session.query(Asignatura).filter(and_(Asignatura.nombre == asignatura, Asignatura.activo == 1)).first()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.docente_id == docente.id, Tutoria.asignatura_id == asignatura.id, Tutoria.activo == 1)).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        return tutorias_list
    
    def find_tutoria_by_fecha_asignatura(self, fecha, asignatura):
        session = db.get_session()
        asignatura = session.query(Asignatura).filter(and_(Asignatura.nombre == asignatura, Asignatura.activo == 1)).first()
        tutorias = session.query(Tutoria).filter(Tutoria.asignatura_id == asignatura.id, Tutoria.fecha == fecha, Tutoria.activo == 1).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
        
    def find_tutoria_by_docente_fecha(self, documento_docente, fecha):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.docente_id == docente.id, Tutoria.fecha == fecha, Tutoria.activo == 1)).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def find_tutoria_by_docente_fecha_asignatura(self, documento_docente, fecha, asignatura):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        asignatura = session.query(Asignatura).filter(and_(Asignatura.nombre == asignatura, Asignatura.activo == 1)).first()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.docente_id == docente.id, Tutoria.fecha == fecha, Tutoria.asignatura_id == asignatura.id, Tutoria.activo == 1)).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def find_tutoria_by_id(self, id_tutoria):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.id == id_tutoria, Tutoria.activo == 1)).first()

        if tutorias:
            tutorias_list = self.tutoria_to_dict(tutorias)
            session.close()
            return tutorias_list
        else:
            return False
        
    def find_tutoria_between_dates(self, fecha_inicio, fecha_final):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.fecha.between(fecha_inicio, fecha_final), Tutoria.activo == 1)).order_by(Tutoria.fecha.asc()).all()
        if tutorias:
            tutorias_list = self.tutorias_to_dict(tutorias)
            session.close()
            return tutorias_list
        else:
            return False
    
    def get_tutorias_soon(self, documento_docente):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.docente_id == docente.id, Tutoria.activo == 1, Tutoria.fecha > date.today())).limit(5).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def count_tutorias_month_by_docente(self, documento_docente):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        tutorias_count = session.query(func.count(Tutoria.id)).filter(and_(Tutoria.docente_id == docente.id, Tutoria.activo == 1, (Tutoria.fecha - date.today() <= 30),(Tutoria.fecha - date.today() >= 0))).scalar()
        session.close()
        return tutorias_count
    
    def count_tutorias_week_by_docente(self, documento_docente):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        tutorias_count = session.query(func.count(Tutoria.id)).filter(and_(Tutoria.docente_id == docente.id, Tutoria.activo == 1, (Tutoria.fecha - date.today() <= 7),(Tutoria.fecha - date.today() >= 0))).scalar()
        session.close()
        return tutorias_count
    
    def count_tutorias_day_by_docente(self, documento_docente):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == documento_docente, Usuario.activo == 1)).first()
        tutorias_count = session.query(func.count(Tutoria.id)).filter(and_(Tutoria.docente_id == docente.id, Tutoria.activo == 1, (Tutoria.fecha - date.today() == 0),(Tutoria.fecha - date.today() >= 0))).scalar()
        session.close()
        return tutorias_count
    
    def get_tutorias_soon_admin(self):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.activo == 1, Tutoria.fecha > date.today())).limit(5).all()
        tutorias_list = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_list
    
    def count_tutorias_month_admin(self):
        session = db.get_session()
        tutorias_count = session.query(func.count(Tutoria.id)).filter(and_(Tutoria.activo == 1, (Tutoria.fecha - date.today() <= 30),(Tutoria.fecha - date.today() >= 0))).scalar()
        session.close()
        return tutorias_count
    
    def count_tutorias_week_admin(self):
        session = db.get_session()
        tutorias_count = session.query(func.count(Tutoria.id)).filter(and_(Tutoria.activo == 1, (Tutoria.fecha - date.today() <= 7),(Tutoria.fecha - date.today() >= 0))).scalar()
        session.close()
        return tutorias_count
    
    def count_tutorias_day_admin(self):
        session = db.get_session()
        tutorias_count = session.query(func.count(Tutoria.id)).filter(and_(Tutoria.activo == 1, (Tutoria.fecha - date.today() == 0),(Tutoria.fecha - date.today() >= 0))).scalar()
        session.close()
        return tutorias_count
    
    def tutorias_day(self):
        session = db.get_session()
        tutorias = session.query(Tutoria).filter(and_(Tutoria.activo == 1, Tutoria.fecha == date.today())).all()
        tutorias_dict = self.tutorias_to_dict(tutorias)
        session.close()
        return tutorias_dict
    
    def get_estudiantes(self, estudiantes):
        estudiantes_list = []
        for estudiante in estudiantes:
            estudiante_dict = {
                'nombre' : estudiante.nombre,
                'tipo_identificacion' : estudiante.tipo_identificacion,
                'numero_identificacion' : estudiante.numero_identificacion,
                'email' : estudiante.email,
                'carreras' : self.get_programa(estudiante.carreras)
            }
            estudiantes_list.append(estudiante_dict)
        return estudiantes_list
    
    def get_docente(self, docente_id):
        session = db.get_session()
        docente = session.query(Usuario).filter(and_(Usuario.id == docente_id, Usuario.activo == 1)).first()
        docente_list = []
        docente_dict = {
            'nombre' : docente.nombre,
            'tipo_identificacion' : docente.tipo_identificacion,
            'numero_identificacion' : docente.numero_identificacion,
            'programa' : self.get_programa(docente.programas)
        }
        docente_list.append(docente_dict)
        session.close()
        return docente_list
    
    def get_programa(self, programas):
        programa_list = [programa.to_dict() for programa in programas]
        return programa_list
    
    def get_asignatura(self, asignatura_id):

        session = db.get_session()
        asignatura_list = []
        asignatura = session.query(Asignatura).filter(and_(Asignatura.id == asignatura_id, Asignatura.activo == 1)).first()
        asignatura_list.append(asignatura.to_dict())
        session.close()
        return asignatura_list
    

    def tutorias_to_dict(self, tutorias):
        tutorias_list = []

        for tutoria in tutorias:
            estudiantes_list = self.get_estudiantes(tutoria.estudiantes)

            docente_list = self.get_docente(tutoria.docente_id)

            asignatura_list = self.get_asignatura(tutoria.asignatura_id)
            hora_inicio_12h = self.hora_12h(tutoria.hora_inicio)
            hora_fin_12h = self.hora_12h(tutoria.hora_fin)
            fecha_format = self.fecha_formateada(tutoria.fecha)

            tutorias_dict = {
                'id' : tutoria.id,
                'fecha' : fecha_format,
                'hora_inicio' : hora_inicio_12h,
                'hora_fin' : hora_fin_12h,
                'docente' : docente_list,
                'estudiantes' : estudiantes_list,
                'asignatura' : asignatura_list,
                'tema_desarrollar' : tutoria.tema_desarrollar
            }
            tutorias_list.append(tutorias_dict)
        
        return tutorias_list
    
    def tutoria_to_dict(self, tutoria):
        estudiantes_list = self.get_estudiantes(tutoria.estudiantes)

        docente_list = self.get_docente(tutoria.docente_id)

        asignatura_list = self.get_asignatura(tutoria.asignatura_id)
        hora_inicio_12h = self.hora_12h(tutoria.hora_inicio)
        hora_fin_12h = self.hora_12h(tutoria.hora_fin)
        fecha_format = self.fecha_formateada(tutoria.fecha)

        tutoria_dict = {
            'id' : tutoria.id,
            'fecha' : fecha_format,
            'hora_inicio' : hora_inicio_12h,
            'hora_fin' : hora_fin_12h,
            'docente' : docente_list,
            'estudiantes' : estudiantes_list,
            'asignatura' : asignatura_list,
            'tema_desarrollar' : tutoria.tema_desarrollar
        }
        return tutoria_dict
    
    def update_tutoria(self, id, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):

        try:       
            session = db.get_session()

            emails = []
            docente_valido = self.validar_docente(docente_id)

            if docente_valido:
                return docente_valido
            
            estudiante_valido = self.validar_estudiantes(estudiantes)

            if estudiante_valido:
                return estudiante_valido
            
            asignatura_valido = self.validar_asignatura(asignatura_id)

            if asignatura_valido:
                return asignatura_valido

            tutoria = session.query(Tutoria).filter(and_(Tutoria.id == id, Tutoria.activo == 1)).first()
            docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == docente_id, Usuario.activo == 1)).first()
            asignatura = session.query(Asignatura).filter(and_(Asignatura.id == asignatura_id, Asignatura.activo == 1)).first()

            if tutoria:
                tutoria.asignatura_id = docente_id
                tutoria.fecha = fecha
                tutoria.hora_inicio = hora_inicio
                tutoria.hora_fin = hora_fin
                tutoria.asignatura_id = asignatura_id
                tutoria.estudiantes.clear()

                for estudiante in estudiantes:
                    estudiante_encontrado = session.query(Usuario).filter(and_(Usuario.numero_identificacion == estudiante, Usuario.activo == 1)).first()
                    tutoria.estudiantes.append(estudiante_encontrado)
                    emails.append(estudiante_encontrado.email)
                
                session.commit()

                hora_inicio_12h = self.hora_12h(tutoria.hora_inicio)
                hora_fin_12h = self.hora_12h(tutoria.hora_fin)
                fecha_formateada = self.fecha_formateada(tutoria.fecha)

                mail = current_app.extensions['mail']
                msg = Message("Tutoria modificada", sender = "Tutorias ingenierias", recipients=emails)
                msg.html = render_template("tutoria_modificada.html", docente = docente.nombre, hora_inicio = hora_inicio_12h, hora_fin = hora_fin_12h, fecha = fecha_formateada, asignatura = asignatura.nombre)
                mail.send(msg)

                msg_docente = Message("Tutoria modificada", sender="Tutorias ingenierias", recipients=[docente.email])
                msg_docente.html = render_template("tutoria_modificada_docente.html", docente = docente.nombre, hora_inicio = hora_inicio_12h, hora_fin = hora_fin_12h, fecha = fecha_formateada, asignatura = asignatura.nombre, estudiantes=tutoria.estudiantes)
                mail.send(msg_docente)

                session.close()

                return True
            else:
                return False
        except DataError as e:
            raise e
            
    def delete_tutoria(self, id):

        session = db.get_session()

        tutoria = session.query(Tutoria).filter(and_(Tutoria.id == id, Tutoria.activo == 1)).first()

        if tutoria:
            emails = []
            tutoria.activo = 0
            session.commit()
            docente = session.query(Usuario).filter(and_(Usuario.id == tutoria.docente_id, Usuario.activo == 1)).first()
            emails.append(docente.email)

            asignatura = session.query(Asignatura).filter(and_(Asignatura.id == tutoria.asignatura_id, Asignatura.activo == 1)).first()
            hora_inicio_12h = self.hora_12h(tutoria.hora_inicio)
            hora_fin_12h = self.hora_12h(tutoria.hora_fin)
            fecha_formateada = self.fecha_formateada(tutoria.fecha)
            
            for estudiante in tutoria.estudiantes:
                emails.append(estudiante.email)

            mail = current_app.extensions['mail']
            msg = Message("Tutoria cancelada", sender = "tutoriasingenierias@gmail.com", recipients=emails)
            msg.html = render_template("tutoria_eliminada.html", hora_inicio = hora_inicio_12h, hora_fin = hora_fin_12h, fecha = fecha_formateada, asignatura = asignatura.nombre)
            mail.send(msg)
            session.close()
            return True
        else:
            return False
        
    def validar_docente(self, docente_id):
        session = db.get_session()

        docente = session.query(Usuario).filter(and_(Usuario.numero_identificacion == docente_id, Usuario.activo == 1)).first()

        if docente == None:
            error = "docente no encontrado"
            return error
        

    def validar_estudiantes(self, estudiantes):
        session = db.get_session()

        for estudiante in estudiantes:
            estudiante_encontrado = session.query(Usuario).filter(and_(Usuario.numero_identificacion == estudiante, Usuario.activo == 1)).first()

            if estudiante_encontrado == None:
                error = "Estudiantes no validos"
                return error
            
    def validar_asignatura(self, asignatura_id):
        session = db.get_session()

        asignatura = session.query(Asignatura).filter(and_(Asignatura.id == asignatura_id, Asignatura.activo == 1)).first()
        if asignatura == None:
            error = "Asignatura no valida"
            return error