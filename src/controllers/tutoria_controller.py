from flask import Blueprint, jsonify, request
from service.tutoria_service import TutoriaService
from repository.repository_impl.tutoria_repo_impl import TutoriaRepoImpl

tutoria = Blueprint('tutoria', __name__, url_prefix = "/tutoria")
tutoria_repository = TutoriaRepoImpl()
tutoria_service = TutoriaService(tutoria_repository)

@tutoria.route("/create_tutoria", methods = ['POST'])
def create_tutoria():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    data = request.get_json()
    
    docente_id = data.get('docente_id')
    fecha = data.get('fecha')
    hora_inicio = data.get('hora_inicio')
    hora_fin = data.get('hora_fin')
    asignatura_id = data.get('asignatura_id')
    estudiantes = data.get('estudiantes')

    new_tutoria = tutoria_service.create_tutoria(docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id)

    if new_tutoria:
        return jsonify(response)
    else:
        response['status_code'] = 400
        response['message'] = "Hubo un problema con la consulta"
        return jsonify(response)

@tutoria.route("/tutorias")
def get_tutorias():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    response['datos'] = tutoria_service.get_tutorias()
    return jsonify(response)

@tutoria.route("/find_tutoria/<string:numero_documento>", methods = ['GET'])
def get_tutoria_by_docente(numero_documento):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.find_tutorias_by_docente(numero_documento)
    response['datos'] = tutorias
    return jsonify(response)

@tutoria.route("/find_tutoria_fecha/<string:fecha>", methods = ['GET'])
def get_tutoria_by_fecha(fecha):
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    tutorias = tutoria_service.find_tutorias_by_fecha(fecha)
    response['datos'] = tutorias
    return jsonify(response)

@tutoria.route("/find_tutoria_asignatura/<string:asignatura>")
def get_tutoria_by_asignatura(asignatura):

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    response['datos'] = tutoria_service.find_tutorias_by_asignatura(asignatura)
    return jsonify(response)