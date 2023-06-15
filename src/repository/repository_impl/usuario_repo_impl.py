from flask import current_app
from flask_mail import Message
from repository.repository_interface.usuario_repo import UsuarioRepo
from models.usuarios_class import Usuario
from models.roles_class import Rol
from models.asignatura_class import Asignatura
from models.carrera_class import Carrera
from configs.database import Database
from passlib.hash import pbkdf2_sha256
from Json.jwt_class import JWT
from sqlalchemy.exc import IntegrityError
import random
from models.codigo_class import Codigo
from sqlalchemy import and_

db = Database()

class UsuarioRepoImpl(UsuarioRepo):

    def create_user(self, nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas):

        try:

            session = db.get_session()
            roles = self.validar_roles(rol)

            if roles:
                return roles

            if "ROLE_ADMIN" in rol and "ROLE_ESTUDIANTE" in rol:
                password_hashed = self.hashear_password(password)
                new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed)
            
                carrera_encontrada = session.query(Carrera).filter(Carrera.id == carrera and Carrera.activo == 1).first()

                if carrera_encontrada:
                    new_user.carreras.append(carrera_encontrada)
                else:
                    error = "Carrera no encontrada"
                    return error
                
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

                validar_asignatura = self.validar_asignaturas(asignaturas)
                if validar_asignatura:
                    return validar_asignatura

                for asignatura in asignaturas:
                    asignatura_encontrada = session.query(Asignatura).filter(Asignatura.id == asignatura and Asignatura.activo == 1).first()
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
                carrera_encontrada = session.query(Carrera).filter(Carrera.id == carrera and Carrera.activo == 1).first()
                if carrera_encontrada:
                    new_user.carreras.append(carrera_encontrada)
                else:
                    error = "Carrera no encontrada"
                    return error

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

                validar_asignatura = self.validar_asignaturas(asignaturas)
                if validar_asignatura:
                    return validar_asignatura
            
                for asignatura in asignaturas:
                    asignatura_encontrada = session.query(Asignatura).filter(Asignatura.id == asignatura and Asignatura.activo == 1).first()
                    new_user.asignaturas.append(asignatura_encontrada) 
                
                session.add(new_user)
                session.commit()
                
                mail = current_app.extensions['mail']
                msg = Message("Registro exitoso", sender="tutoriasingenierias@gmail.com", recipients=[email])
                msg.body = f"Se ha registrado exitosamente, usuario: {nombre}"
                mail.send(msg)
                session.close()
                return True
        except IntegrityError as e:
            raise e
        
    def generar_codigo(self, email):
        session = db.get_session()
        codigo_verificacion = random.randint(100000, 999999)
        new_codigo = Codigo(codigo_verificacion)
        session.add(new_codigo)
        session.commit()

        mail = current_app.extensions['mail']
        msg = Message("Codigo de verificacion", sender = "tutoriasingenierias@gmail.com", recipients=[email])
        msg.body = "Para culminar su registro, por favor digite el siguiente codigo de verificacion en la pagina: " + str(codigo_verificacion)
        mail.send(msg)
        return codigo_verificacion
    
    def verify_codigo(self, codigo):
        session = db.get_session()

        codigo_access = session.query(Codigo).filter(and_(Codigo.codigo_access == codigo, Codigo.used == 1)).first()

        if codigo_access:
            codigo_access.used = 0
            session.commit()
            session.close()
            return True
        else:
            return False
        
    def login(self, email, password):
        session = db.get_session()
        
        usuario = session.query(Usuario).filter(and_(Usuario.email == email, Usuario.activo == 1)).first()
        
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
        usuarios = session.query(Usuario).filter(Usuario.activo == 1).all()
        usuarios_list = []
        for usuario in usuarios:

            roles = self.get_roles_by_usuario(usuario.roles)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_identificacion' : usuario.tipo_identificacion,
                'numero_identificacion' : usuario.numero_identificacion,
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
        usuarios_estudiante = session.query(Usuario).filter(Usuario.roles.contains(rol_estudiante) and Usuario.activo == 1).all()
        usuarios_list = []
        for usuario in usuarios_estudiante:
            roles = self.get_roles_by_usuario(usuario.roles)
            carreras = self.get_carreras()

            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_idenficacion' : usuario.tipo_identificacion,
                'numero_identificacion' : usuario.numero_identificacion,
                'roles' : roles,
                'carrera' : carreras
            }
            usuarios_list.append(usuario_dict)
        session.close()
        return usuarios_list
    

    def get_users_admin(self):
        session = db.get_session()
        rol_admin = session.query(Rol).filter(Rol.rol == "ROLE_ADMIN").first()
        usuarios_admins = session.query(Usuario).filter(Usuario.roles.contains(rol_admin) and Usuario.activo == 1).all()
        usuarios_list = []
        for usuario in usuarios_admins:
            roles = self.get_roles_by_usuario(usuario.roles)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_identificacion' : usuario.tipo_identificacion,
                'numero_identificacion' : usuario.numero_identificacion,
                'roles' : roles
            }
            usuarios_list.append(usuario_dict)
        
        session.close()
        return usuarios_list
    
    def get_users_docentes(self):
        session = db.get_session()
        rol_docente = session.query(Rol).filter(Rol.rol == "ROLE_DOCENTE").first()
        usuarios_docentes = session.query(Usuario).filter(Usuario.roles.contains(rol_docente) and Usuario.activo == 1).all()
        usuarios_list = []
        for usuario in usuarios_docentes:
            roles = self.get_roles_by_usuario(usuario.roles)
            asignaturas = self.get_asignaturas(usuario.asignaturas)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_identificacion' : usuario.tipo_identificacion,
                'numero_identificacion' : usuario.numero_identificacion,
                'asignaturas' : asignaturas,
                'roles' : roles
            }
            usuarios_list.append(usuario_dict)

        session.close()        
        return usuarios_list
    

    def get_roles(self, email):
        session = db.get_session()
        usuario = session.query(Usuario).filter(Usuario.email == email and Usuario.activo == 1).first()
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
    
    def validar_roles(self, roles):

        session = db.get_session()
        for rol in roles:
            rol_encontrado = session.query(Rol).filter(Rol.rol == rol).first()
            print(rol_encontrado)
            if rol_encontrado == None:
                error = "Rol no encontrado"
                return error
            
    def validar_asignaturas(self, asignaturas):
        session = db.get_session()

        for asignatura in asignaturas:
            asignatura_encontrada = session.query(Asignatura).filter(Asignatura.id == asignatura).first()

            if asignatura_encontrada == None:
                error = "asignatura no encontrada"
                return error
        
    def validar_email(self, email):
        session = db.get_session()

        usuario_found = session.query(Usuario).filter(Usuario.email == email).first()

        if usuario_found:
            return True
        else:
            return False
    
    def validar_documento(self, cedula):
        session = db.get_session()

        usuario_found = session.query(Usuario).filter(Usuario.numero_identificacion == cedula).first()

        if usuario_found:
            return True
        else:
            return False
        
    def validar_celular(self, celular):
        session = db.get_session()

        usuario_found = session.query(Usuario).filter(Usuario.celular == celular).first()

        if usuario_found:
            return True
        else:
            return False