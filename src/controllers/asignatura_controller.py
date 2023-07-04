from flask import jsonify, Blueprint
from service.asignatura_service import AsignaturaService
from repository.repository_impl.asignatura_repo_impl import AsignaturaRepoImpl

asignatura = Blueprint('asignatura', __name__, url_prefix='/asignatura')
asignatura_repository = AsignaturaRepoImpl()
asignatura_service = AsignaturaService(asignatura_repository)


@asignatura.route("/get_asignaturas", methods = ['GET'])
def get_asignaturas():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    asignaturas = asignatura_service.get_asignaturas()

    if asignaturas:
        response['datos'] = asignaturas
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No hay asignaturas creadas hasta el momento"
        return jsonify(response), 404