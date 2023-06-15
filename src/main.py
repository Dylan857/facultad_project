from flask import Flask, jsonify, request
from configs.database import Database
from controllers.solicitud_controller import solicitud
from controllers.auth_controller import auth
from Json.jwt_class import JWT
from controllers.usuario_controller import usuario
from controllers.tutoria_controller import tutoria
from configs.mail import MailConfig
from flask_mail import Mail

app = Flask(__name__)

db = Database()
JWT._init_jwt(app)
app.config.from_object(MailConfig)
mail = Mail(app)

app.register_blueprint(solicitud)
app.register_blueprint(auth)
app.register_blueprint(usuario)
app.register_blueprint(tutoria)

if __name__ == '__main__':
    app.run(debug=True)