from flask import Blueprint, jsonify, request, current_app
from service.usuario_service import UsuarioService
from repository.repository_impl.usuario_repo_impl import UsuarioRepoImpl
from Json.jwt_class import JWT
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from jsonschema.validators import validate
from jsonschema import ValidationError
from validate.jsonschema import json_schema
from flask_mail import Message
from validate.JWT_validate import JWTValidate


auth = Blueprint('auth', __name__, url_prefix="/auth")
usuario_repository = UsuarioRepoImpl()
usuario_service = UsuarioService(usuario_repository)

@auth.route("/register", methods = ['POST'])
def create_user():
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'codigo_access' : []
    }
    try:
        data = request.get_json()
        validate(instance=data, schema=json_schema)

        nombre = data.get('nombre')
        email = data.get('email')
        celular = data.get('celular')
        tipo_identificacion = data.get('tipo_identificacion')
        numero_identificacion = data.get('numero_identificacion')
        carrera = data.get('carrera')
        password = data.get('password')
        rol = data.get('rol')
        asignaturas = data.get('asignaturas')

        if usuario_service.validar_email(email):
            response['status_code'] = 400
            response['message'] = "Email ya en uso"
            return jsonify(response), 400
        elif usuario_service.validar_celular(celular):
            response['status_code'] = 400
            response['message'] = "Celular ya en uso"
            return jsonify(response), 400
        elif usuario_service.validar_documento(numero_identificacion):
            response['status_code'] = 400
            response['message'] = "Numero de documento ya en uso"
            return jsonify(response), 400
        
        new_user = usuario_service.create_user(nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas)

        if new_user == True:
            return jsonify(response)
        elif new_user:
            response['status_code'] = 400
            response['message'] = new_user
            return jsonify(response)
        else:
            response['status_code'] = 400
            response['message'] = "Hubo un error al momento de crear el usuario"
            return jsonify(response)
        
    except ValidationError as e:        
        response['status_code'] = 400
        response['message'] = "Algo salio mal al momento de crear el usuario"
        return jsonify(response), 400
    
@auth.route("/verify", methods = ['POST'])
def verificar_codigo():
    
    response = {
        'status_code' : 200,
        'message' : 'OK',
        'datos' : []
    }

    data = request.get_json()
    codigo = data.get('codigo')
    verified_code = usuario_service.verify_codigo(codigo)

    if verified_code:
        return jsonify(response)
    else:
        response['status_code'] = 400
        response['message'] = "codigo no valido o usuario ya activado"
        return jsonify(response)

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
        response['message'] = "Credenciales de inicio de sesion incorrectos o usuario no activado"
        return jsonify(response), 401
    
@auth.route("/ruta_protegida")
@jwt_required()
def ruta_protegida():
    current_user = JWT.get_current_user()
    JWTValidate.validar_token_admin(current_user)

    return jsonify({'message' : 'Funciono lo que pense'})        