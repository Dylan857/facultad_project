from sqlalchemy.exc import IntegrityError

class UsuarioService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository


    def create_user(self, nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas):
        try:
            return self.usuario_repository.create_user(nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas)
        except IntegrityError as e:
            raise e
        
    def login(self, email, password):
        return self.usuario_repository.login(email, password)
    
    def get_roles(self, email):
        return self.usuario_repository.get_roles(email)
    
    def get_users(self):
        return self.usuario_repository.get_users()
    
    def get_user_estudiante(self):
        return self.usuario_repository.get_users_estudiante()
    
    def get_user_admin(self):
        return self.usuario_repository.get_users_admin()
    
    def get_user_docente(self):
        return self.usuario_repository.get_users_docentes()
    
    def generar_codigo(self, email):
        return self.usuario_repository.generar_codigo(email)
    
    def validar_email(self, email):
        return self.usuario_repository.validar_email(email)
    
    def validar_documento(self, cedula):
        return self.usuario_repository.validar_documento(cedula)
    
    def validar_celular(self, celular):
        return self.usuario_repository.validar_celular(celular)
    
    def verify_codigo(self, codigo):
        return self.usuario_repository.verify_codigo(codigo)