from service.tutoria_service import TutoriaService
from repository.repository_impl.tutoria_repo_impl import TutoriaRepoImpl
from flask import current_app, render_template
from flask_mail import Message

tutoria_repository = TutoriaRepoImpl()
tutoria_service = TutoriaService(tutoria_repository)

def envio_notificacion_tutoria(app):

    with app.app_context():
        print("Ejecutando")
        tutorias = tutoria_service.tutorias_day()

        if tutorias:
            for tutoria in tutorias:
                emails_estudiantes = get_emails_estudiante(tutoria['estudiantes'])
                mail = current_app.extensions['mail']
                msg = Message("Recordatoria de tutoria", sender="tutoriasingenierias@gmail.com", recipients=emails_estudiantes)
                msg.html = render_template("recordatorio_tutoria.html", fecha = tutoria['fecha'], hora_inicio = tutoria['hora_inicio'], 
                hora_fin = tutoria['hora_fin'], asignatura = tutoria['asignatura'][0]['nombre'], docente = tutoria['docente'][0]['nombre'])
                mail.send(msg)


def envio_notificacion_tutoria_docentes(app):

    with app.app_context():
        print("Ejecutando")
        tutorias = tutoria_service.tutorias_day()

        if tutorias:
            for tutoria in tutorias:
                emails_estudiantes = get_emails_estudiante(tutoria['estudiantes'])
                mail = current_app.extensions['mail']
                msg = Message("Recordatoria de tutoria", sender="tutoriasingenierias@gmail.com", recipients=emails_estudiantes)
                msg.html = render_template("recordatorio_tutoria.html", fecha = tutoria['fecha'], hora_inicio = tutoria['hora_inicio'], 
                hora_fin = tutoria['hora_fin'], asignatura = tutoria['asignatura'][0]['nombre'], docente = tutoria['docente'][0]['nombre'])
                mail.send(msg)

def get_emails_estudiante(estudiantes):
    emails = []
    for estudiante in estudiantes:
        emails.append(estudiante['email'])

    return emails