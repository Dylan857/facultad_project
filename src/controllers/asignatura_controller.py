from flask import jsonify, Blueprint
from service.asignatura_service import AsignaturaService
from repository.repository_impl.asignatura_repo_impl import AsignaturaRepoImpl
from flask_jwt_extended import jwt_required
from validate.JWT_validate import JWTValidate
from Json.jwt_class import JWT

asignatura = Blueprint('asignatura', __name__, url_prefix='/asignatura')
asignatura_repository = AsignaturaRepoImpl()
asignatura_service = AsignaturaService(asignatura_repository)


@asignatura.route("/get_asignaturas", methods = ['GET'])
@jwt_required()
def get_asignaturas():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_admin(current_user)
    if token:
        return jsonify(token)

    asignaturas = asignatura_service.get_asignaturas()

    if asignaturas:
        response['datos'] = asignaturas
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No hay asignaturas creadas hasta el momento"
        return jsonify(response), 404