from flask import Blueprint, jsonify, request
from service.solicitud_service import SolicitudService
from repository.repository_impl.solicitud_repo_impl import SolicitudRepositoryImpl
from configs.database import Database

solicitud = Blueprint('solicitud', __name__, url_prefix='/solicitud')
solicitud_repository = SolicitudRepositoryImpl()
solicitud_service = SolicitudService(solicitud_repository)


@solicitud.route('/solicitudes', methods = ['GET'])
def get_solicitudes():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }
    response['datos'] = solicitud_service.get_solicitudes()
    return jsonify(response)

@solicitud.route("/solicitud_docente/<string:id>", methods = ['GET'])
def get_solicitud_by_docente(id):
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    solicitudes = solicitud_service.get_solicitud_by_docente(id)
    if solicitudes:
        response['datos'] = solicitudes
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = 'El docente no cuenta con solicitudes'
        return jsonify(response), 404

@solicitud.route("/hacer_solicitud", methods = ['POST'])
def hacer_solicitud():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    data = request.get_json()
    estudiante_id = data.get('cedula_estudiante')
    docente_id = data.get('cedula_docente')
    descripcion_solicitud = data.get('descripcion_solicitud')
    solicitud = solicitud_service.make_a_request(estudiante_id, docente_id, descripcion_solicitud)

    if solicitud is None:
        return jsonify({'error' : 'Cedula no valida'}), 404
    

    if solicitud:
        return jsonify(response)
    else:
        response['status_code'] = 400
        response['message'] = "Hubo un problema haciendo la solicitud"
        return jsonify(response), 400