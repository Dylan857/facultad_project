from service.tutoria_service import TutoriaService
from repository.repository_impl.tutoria_repo_impl import TutoriaRepoImpl
from flask import current_app, render_template
from flask_mail import Message
from service.usuario_service import UsuarioService
from repository.repository_impl.usuario_repo_impl import UsuarioRepoImpl
import traceback

tutoria_repository = TutoriaRepoImpl()
tutoria_service = TutoriaService(tutoria_repository)

usuario_repository = UsuarioRepoImpl()
usuario_service = UsuarioService(usuario_repository)

def envio_notificacion_tutoria(app):

    with app.app_context():
        tutorias = tutoria_service.tutorias_day()

        if tutorias:
            for tutoria in tutorias:
                emails_estudiantes = get_emails_estudiante(tutoria['estudiantes'])
                mail = current_app.extensions['mail']
                msg = Message("Recordatoria de tutoria", sender="tutoriasingenierias@gmail.com", recipients=emails_estudiantes)
                msg.html = render_template("recordatorio_tutoria.html", fecha = tutoria['fecha'], hora_inicio = tutoria['hora_inicio'], 
                hora_fin = tutoria['hora_fin'], asignatura = tutoria['asignatura']['nombre'], docente = tutoria['docente']['nombre'])
                mail.send(msg)


def envio_notificacion_tutoria_docentes(app):
    with app.app_context():
        try:
            docentes = usuario_service.get_user_docente()

            for docente in docentes:
                tutorias = tutoria_service.tutorias_day_docente(docente['numero_identificacion'])
                if tutorias:
                    enviar_email(docente, tutorias)
        except Exception as e:
            traceback.print_exc()
            print(f"Error al enviar el correo: {str(e)}")

def enviar_email(docente, tutorias):
    print(docente['email'])
    mail = current_app.extensions['mail']
    msg = Message("Lista tutorias hoy", sender="tutoriasingenierias@gmail.com", recipients=[docente['email']])
    msg.html = render_template("recordatorio_tutoria_docente.html", tutorias = tutorias) 
    mail.send(msg)
    
def get_emails_estudiante(estudiantes):
    emails = []
    for estudiante in estudiantes:
        emails.append(estudiante['email'])
    return emails