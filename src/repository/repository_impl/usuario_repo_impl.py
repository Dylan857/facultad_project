from repository.repository_interface.usuario_repo import UsuarioRepo
from models.usuarios_class import Usuario
from models.roles_class import Rol
from models.asignatura_class import Asignatura
from models.carrera_class import Carrera
from configs.database import Database
from passlib.hash import pbkdf2_sha256
from Json.jwt_class import JWT

db = Database()

class UsuarioRepoImpl(UsuarioRepo):

    def create_user(self, nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas):

        session = db.get_session()

        if "ROLE_ADMIN" in rol and "ROLE_ESTUDIANTE" in rol:
            password_hashed = self.hashear_password(password)
            new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed)
           
            carrera_encontrada = session.query(Carrera).filter(Carrera.id == carrera).first()

            if carrera_encontrada:
                new_user.carreras.append(carrera_encontrada)
            
            for role in rol:
                rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                new_user.roles.append(rol_encontrado)
            
            session.add(new_user)
            session.commit()
            session.close()
            return True
        
        elif "ROLE_ADMIN" in rol and "ROLE_DOCENTE" in rol:
            password_hashed = self.hashear_password(password)
            new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed)
            
            for role in rol:
                rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                new_user.roles.append(rol_encontrado)

            for asignatura in asignaturas:
                asignatura_encontrada = session.query(Asignatura).filter(Asignatura.id == asignatura).first()
                new_user.asignaturas.append(asignatura_encontrada)
            
            session.add(new_user)
            session.commit()
            session.close()
            return True
        
        elif "ROLE_ADMIN" in rol:
            password_hashed = self.hashear_password(password)
            new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed)
            for role in rol:
                rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                new_user.roles.append(rol_encontrado)
            session.add(new_user)
            session.commit()
            session.close()
            return True
        
        elif "ROLE_ESTUDIANTE" in rol:
            password_hashed = self.hashear_password(password)
            new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed)
            carrera_encontrada = session.query(Carrera).filter(Carrera.id == carrera).first()

            if carrera_encontrada:
                new_user.carreras.append(carrera_encontrada)

            for role in rol:
                rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                new_user.roles.append(rol_encontrado)
            session.add(new_user)
            session.commit()
            session.close()
            return True
        
        elif "ROLE_DOCENTE" in rol:
        
            password_hashed = self.hashear_password(password)
            new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed)
        
            for role in rol:
                rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                new_user.roles.append(rol_encontrado)
        
            for asignatura in asignaturas:
                asignatura_encontrada = session.query(Asignatura).filter(Asignatura.id == asignatura).first()
                new_user.asignaturas.append(asignatura_encontrada)
            
            session.add(new_user)
            session.commit()
            session.close()
            return True
    
    def login(self, email, password):
        session = db.get_session()
        
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        
        if usuario and pbkdf2_sha256.verify(password, usuario.password):
            roles = self.get_roles(usuario.email)
            additional_claims = {'roles' : roles,
                                 'nombre' : usuario.nombre,
                                 'celular' : usuario.celular
                                 }
            for rol in roles:
                if "ROLE_ESTUDIANTE" in rol.get('rol'):
                    carreras = self.get_carreras(usuario.carreras)
                    additional_claims['carreras'] = carreras
                elif "ROLE_DOCENTE" in rol.get('rol'):
                    asignaturas = self.get_asignaturas(usuario.asignaturas)
                    additional_claims['asignaturas'] = asignaturas

            
            access_token = JWT.generate_access_token(identity=usuario.email, additional_claims=additional_claims)
            return access_token
        else:
            return False


    def hashear_password(self, password):
        return pbkdf2_sha256.hash(password)
    
    def get_users(self):
        session = db.get_session()
        usuarios = session.query(Usuario).all()
        usuarios_list = []
        for usuario in usuarios:

            roles = self.get_roles_by_usuario(usuario.roles)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_idenficacion' : usuario.tipo_identificacion,
                'numero_identifacion' : usuario.numero_identificacion,
                'roles' : roles
            }

            for role in roles:
                
                if "ROLE_ESTUDIANTE" in role.get('rol'):
                    carreras = self.get_carreras(usuario.carreras)
                    usuario_dict['carrera'] = carreras

                if "ROLE_DOCENTE" in role.get('rol'):
                    asignaturas = self.get_asignaturas(usuario.asignaturas)
                    usuario_dict['asignaturas'] = asignaturas
            usuarios_list.append(usuario_dict)

        session.close()
        return usuarios_list

    def get_users_estudiante(self):
        session = db.get_session()
        rol_estudiante = session.query(Rol).filter(Rol.rol == "ROLE_ESTUDIANTE").first()
        usuarios_estudiante = session.query(Usuario).filter(Usuario.roles.contains(rol_estudiante)).all()
        usuarios_list = []
        for usuario in usuarios_estudiante:
            roles = self.get_roles_by_usuario(usuario.roles)
            carreras = self.get_carreras()

            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_idenficacion' : usuario.tipo_identificacion,
                'numero_identifacion' : usuario.numero_identificacion,
                'roles' : roles,
                'carrera' : carreras
            }
            usuarios_list.append(usuario_dict)
        session.close()
        return usuarios_list
    

    def get_users_admin(self):
        session = db.get_session()
        rol_admin = session.query(Rol).filter(Rol.rol == "ROLE_ADMIN").first()
        usuarios_admins = session.query(Usuario).filter(Usuario.roles.contains(rol_admin)).all()
        usuarios_list = []
        for usuario in usuarios_admins:
            roles = self.get_roles_by_usuario(usuario.roles)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_idenficacion' : usuario.tipo_identificacion,
                'numero_identifacion' : usuario.numero_identificacion,
                'roles' : roles
            }
            usuarios_list.append(usuario_dict)
        
        session.close()
        return usuarios_list
    
    def get_users_docentes(self):
        session = db.get_session()
        rol_docente = session.query(Rol).filter(Rol.rol == "ROLE_DOCENTE").first()
        usuarios_docentes = session.query(Usuario).filter(Usuario.roles.contains(rol_docente)).all()
        usuarios_list = []
        for usuario in usuarios_docentes:
            roles = self.get_roles_by_usuario(usuario.roles)
            asignaturas = self.get_asignaturas(usuario.asignaturas)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_idenficacion' : usuario.tipo_identificacion,
                'numero_identifacion' : usuario.numero_identificacion,
                'asignaturas' : asignaturas,
                'roles' : roles
            }
            usuarios_list.append(usuario_dict)

        session.close()        
        return usuarios_list
    

    def get_roles(self, email):
        session = db.get_session()
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        roles_list = []
        for rol in usuario.roles:
            roles_dict = {
                'rol' : rol.rol
            }
            roles_list.append(roles_dict)
        session.close()
        return roles_list
    
    def get_roles_by_usuario(self, roles):
        roles_list = []
        for rol in roles:
            roles_list.append(rol.to_dict())
        return roles_list
    
    def get_carreras(self, carreras):
        carreras_list = []
        for carrera in carreras:
            carreras_list.append(carrera.to_dict())
        return carreras_list
    
    def get_asignaturas(self, asignaturas):
        asignaturas_list = []
        for asignatura in asignaturas:
            asignaturas_list.append(asignatura.to_dict())
        return asignaturas_list