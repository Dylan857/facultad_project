from flask import Flask, jsonify, request
from flask_cors import CORS
from configs.database import Database
from controllers.solicitud_controller import solicitud
from controllers.auth_controller import auth
from Json.jwt_class import JWT
from controllers.usuario_controller import usuario
from controllers.tutoria_controller import tutoria
from controllers.asignatura_controller import asignatura
from controllers.carrera_controller import carrera
from configs.mail import MailConfig
from flask_mail import Mail

app = Flask(__name__)

db = Database()
JWT._init_jwt(app)
app.config.from_object(MailConfig)
mail = Mail(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:5173",  # El origen permitido para las solicitudes
        "methods": ["GET", "POST", "PUT", "DELETE"],  # Los métodos HTTP permitidos
        "allow_headers": ["Content-Type", "Authorization"]  # Los encabezados permitidos
    }
})

app.register_blueprint(solicitud)
app.register_blueprint(auth)
app.register_blueprint(usuario)
app.register_blueprint(tutoria)
app.register_blueprint(asignatura)
app.register_blueprint(carrera)

if __name__ == '__main__':
    app.run(debug=True)