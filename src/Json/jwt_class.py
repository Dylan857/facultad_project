from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager


jwt = JWTManager()

class JWT:

    @staticmethod
    def _init_jwt(app):
        app.config['JWT_SECRET_KEY'] = "juniormanda"
        jwt.init_app(app)

    @staticmethod
    def generate_access_token(identity, additional_claims = None):
        return create_access_token(identity, additional_claims)
    
    @staticmethod
    def get_current_user():
        return get_jwt_identity()