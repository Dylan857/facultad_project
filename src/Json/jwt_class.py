from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

jwt = JWTManager()

class JWT:

    @staticmethod
    def _init_jwt(app):
        app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
        jwt.init_app(app)

    @staticmethod
    def generate_access_token(identity, additional_claims = None):
        return create_access_token(identity, additional_claims)
    
    @staticmethod
    def get_current_user():
        return get_jwt_identity()