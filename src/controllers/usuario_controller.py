from flask import Blueprint, jsonify
from service.usuario_service import UsuarioService
from repository.repository_impl.usuario_repo_impl import UsuarioRepoImpl
from flask_jwt_extended import jwt_required
from validate.JWT_validate import JWTValidate
from Json.jwt_class import JWT

usuario = Blueprint('usuario', __name__, url_prefix="/usuario")
usuario_repository = UsuarioRepoImpl()
usuario_service = UsuarioService(usuario_repository)



@usuario.route("/user_information")
@jwt_required()
def user_information():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token(current_user)
    if token:
        return jsonify(token)
    
    usuario_login = usuario_service.user_information(current_user)
    if usuario_login:
        response['datos'] = usuario_login
        return jsonify(response)
    else:
        response['status_code'] = 400
        response['message'] = "Hubo un problema con la informacion del usuario"
        return jsonify(response)
    
@usuario.route("/find_usuario/<string:numero_documento>")
@jwt_required()
def find_usuario(numero_documento):
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_docente(current_user)
    if token:
        return jsonify(token)
    
    usuario_found = usuario_service.find_user(numero_documento)
    if usuario_found:
        response['datos'] = usuario_found
        return jsonify(response)
    else:
        response['status_code'] = 404
        response['message'] = "Usuario no encontrado"
        return jsonify(response)

@usuario.route("/users", methods = ['GET'])
@jwt_required()
def get_users():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_admin(current_user)
    if token:
        return jsonify(token)

    usuarios = usuario_service.get_users()

    if usuarios:
        response['datos'] = usuarios 
        return jsonify(response)

    else:
        response['message'] = "No hay resultados a mostrar"
        return jsonify(response)
        


@usuario.route("/users_estudiante", methods = ['GET'])
@jwt_required()
def get_users_estudiante():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_admin(current_user)
    if token:
        return jsonify(token)

    usuarios = usuario_service.get_user_estudiante()

    if usuarios:
        response['datos'] = usuarios
        return jsonify(response)
    else:
        response['message'] = "No hay resultados a mostrar"

@usuario.route("/users_admin", methods = ['GET'])
@jwt_required()
def get_users_admin():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_admin(current_user)
    if token:
        return jsonify(token)

    usuarios = usuario_service.get_user_admin()

    if usuarios:
        response['datos'] = usuarios
        return jsonify(response)
    else:
        response['message'] = "No hay resultados a mostrar"
    return jsonify(response)

@usuario.route("/users_docentes", methods = ['GET'])
@jwt_required()
def get_users_docente():

    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    current_user = JWT.get_current_user()
    token = JWTValidate.validar_token_admin(current_user)
    if token:
        return jsonify(token)

    usuarios = usuario_service.get_user_docente()

    if usuarios:
        response['datos'] = usuarios
        return jsonify(response)
    else:
        response['message'] = "No hay resultados a mostrar"
    return jsonify(response)
