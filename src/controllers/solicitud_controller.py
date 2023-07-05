from flask import Blueprint, jsonify, request
from service.solicitud_service import SolicitudService
from repository.repository_impl.solicitud_repo_impl import SolicitudRepositoryImpl
from configs.database import Database
from jsonschema.validators import validate
from jsonschema import ValidationError
from validate.jsonschema import json_schema_solicitud
from flask_jwt_extended import jwt_required
from validate.JWT_validate import JWTValidate
from Json.jwt_class import JWT

solicitud = Blueprint('solicitud', __name__, url_prefix='/solicitud')
solicitud_repository = SolicitudRepositoryImpl()
solicitud_service = SolicitudService(solicitud_repository)


@solicitud.route('/solicitudes', methods = ['GET'])
@jwt_required()
def get_solicitudes():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_admin(current_user)
    if token:
        return jsonify(token)
    
    response['datos'] = solicitud_service.get_solicitudes()
    return jsonify(response)

@solicitud.route("/solicitud_docente/<string:id>", methods = ['GET'])
@jwt_required()
def get_solicitud_by_docente(id):
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_docente(current_user)
    if token:
        return jsonify(token)

    solicitudes = solicitud_service.get_solicitud_by_docente(id)
    if solicitudes:
        response['datos'] = solicitudes
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = 'El docente no cuenta con solicitudes'
        return jsonify(response), 404

@solicitud.route("/hacer_solicitud", methods = ['POST'])
@jwt_required()
def hacer_solicitud():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_estudiante(current_user)
    if token:
        return jsonify(token)

    try:

        data = request.get_json()

        validate(instance=data, schema=json_schema_solicitud)

        estudiante_id = data.get('cedula_estudiante')
        docente_id = data.get('cedula_docente')
        descripcion_solicitud = data.get('descripcion_solicitud')
        solicitud = solicitud_service.make_a_request(estudiante_id, docente_id, descripcion_solicitud)

        if solicitud is None:
            response['status_code'] = 400,
            response['message'] = "Cedula no valida"
            return jsonify(response), 400
        

        if solicitud:
            return jsonify(response)
        else:
            response['status_code'] = 400
            response['message'] = "Hubo un problema haciendo la solicitud"
            return jsonify(response), 400
        
    except ValidationError as e:
        response['status_code'] = 400
        response['message'] = "Datos introducidos no validos"
        return jsonify(response)