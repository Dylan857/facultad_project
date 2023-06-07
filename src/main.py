from flask import Flask, jsonify, request
from models.usuarios_class import Usuario
from models.roles_class import Rol
from models.asignatura_class import Asignatura
from models.solicitud_class import Solicitud
from models.tutoria_class import Tutoria
from configs.database import Database
from controllers.solicitud_controller import solicitud
from controllers.auth_controller import auth
from Json.jwt_class import JWT
from controllers.usuario_controller import usuario
from controllers.tutoria_controller import tutoria

app = Flask(__name__)

db = Database()
JWT._init_jwt(app)

app.register_blueprint(solicitud)
app.register_blueprint(auth)
app.register_blueprint(usuario)
app.register_blueprint(tutoria)

if __name__ == '__main__':
    app.run(debug=True)