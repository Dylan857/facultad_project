from flask import jsonify, Blueprint
from repository.repository_impl.carrera_repo_impl import CarreraRepoImpl
from service.carrera_service import CarreraService


carrera = Blueprint('carrera', __name__, url_prefix='/carrera')
carrera_repository = CarreraRepoImpl()
carrera_service = CarreraService(carrera_repository)


@carrera.route("/get_carreras", methods = ['GET'])
def get_carreras():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    carreras = carrera_service.get_carreras()

    if carreras:
        response['datos'] = carreras
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "No hay carreras registradas"
        return jsonify(response), 404