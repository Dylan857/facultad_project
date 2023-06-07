from flask import Blueprint, jsonify
from service.usuario_service import UsuarioService
from repository.repository_impl.usuario_repo_impl import UsuarioRepoImpl


usuario = Blueprint('usuario', __name__, url_prefix="/usuario")
usuario_repository = UsuarioRepoImpl()
usuario_service = UsuarioService(usuario_repository)

@usuario.route("/users", methods = ['GET'])
def get_users():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    response['datos'] = usuario_service.get_users()
    return jsonify(response)


@usuario.route("/users_estudiante", methods = ['GET'])
def get_users_estudiante():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    response['datos'] = usuario_service.get_user_estudiante()
    return jsonify(response)

@usuario.route("/users_admin", methods = ['GET'])
def get_users_admin():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    response['datos'] = usuario_service.get_user_admin()
    return jsonify(response)

@usuario.route("/users_docentes", methods = ['GET'])
def get_users_docente():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    response['datos'] = usuario_service.get_user_docente()
    return jsonify(response)
