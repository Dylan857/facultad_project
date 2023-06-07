from flask import Blueprint, jsonify, request
from service.usuario_service import UsuarioService
from repository.repository_impl.usuario_repo_impl import UsuarioRepoImpl
from Json.jwt_class import JWT
from flask_jwt_extended import jwt_required


auth = Blueprint('auth', __name__, url_prefix="/auth")
usuario_repository = UsuarioRepoImpl()
usuario_service = UsuarioService(usuario_repository)


@auth.route("/register", methods = ['POST'])
def create_user():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    celular = data.get('celular')
    tipo_identificacion = data.get('tipo_identificacion')
    numero_identificacion = data.get('numero_identificacion')
    carrera = data.get('carrera')
    password = data.get('password')
    rol = data.get('rol')
    asignaturas = data.get('asignaturas')

    new_user = usuario_service.create_user(nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas)

    if new_user:
        return jsonify(response)
    else:
        response['status_code'] = 400
        response['message'] = 'Hubo un error en la insercion'
        return jsonify(response), 400
    

@auth.route("/login", methods = ['POST'])
def login():
    response = {
        'status_code' : 200,
        'message' : "OK",
        'token' : []
    }

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    usuario_logueado = usuario_service.login(email, password)
    if usuario_logueado:
        response['token'] = usuario_logueado
        return jsonify(response)
    else:
        response['status_code'] = 401
        response['message'] = "Credenciales de inicio de sesion incorrectos"
        return jsonify(response), 401

# @auth.route("/ruta_protegida")
# @jwt_required()
# def ruta_protegida():
#     current_user = JWT.get_current_user()
#     usuario_roles = usuario_service.get_roles(current_user)
#     for rol in usuario_roles:
#         if "ROLE_ESTUDIANTE" in rol.get('rol'):
#             return jsonify({'message' : 'Tiene acceso'})