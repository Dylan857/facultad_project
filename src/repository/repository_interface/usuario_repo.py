class UsuarioRepo:
    def create_user(self, nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password):
        raise NotImplementedError
    def login(self, email, password):
        raise NotImplementedError
    def hashear_password(self, password):
        raise NotImplementedError
    def get_roles(self, email):
        raise NotImplementedError
    def get_users(self):
        raise NotImplementedError
    def get_users_admin(self):
        raise NotImplementedError
    def get_users_estudiante(self):
        raise NotImplementedError
    def get_users_docentes(self):
        raise NotImplementedError