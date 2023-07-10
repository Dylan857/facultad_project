from flask import Flask
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
from dotenv import load_dotenv
from flask_apscheduler import APScheduler
import os

load_dotenv()

app = Flask(__name__)

db = Database()
JWT._init_jwt(app)
app.config.from_object(MailConfig)

app.config['SCHEDULER_API_ENABLED'] = os.getenv("SCHEDULER_API_ENABLED")
app.config["JOBS"] = eval(os.getenv("JOBS"))
mail = Mail(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:5173",  # El origen permitido para las solicitudes
        "methods": ["GET", "POST", "PUT", "DELETE"],  # Los métodos HTTP permitidos
        "allow_headers": ["Content-Type", "Authorization"]  # Los encabezados permitidos
    }
})

scheduler = APScheduler()

app.register_blueprint(solicitud)
app.register_blueprint(auth)
app.register_blueprint(usuario)
app.register_blueprint(tutoria)
app.register_blueprint(asignatura)
app.register_blueprint(carrera)

scheduler.init_app(app)

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True, use_reloader = False)