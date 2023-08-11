from flask import current_app, render_template
from flask_mail import Message
from repository.repository_interface.usuario_repo import UsuarioRepo
from models.cambio_clave_class import CambioClave
from models.usuarios_class import Usuario
from models.roles_class import Rol
from models.asignatura_class import Asignatura
from models.carrera_class import Carrera
from configs.database import Database
from passlib.hash import pbkdf2_sha256
from Json.jwt_class import JWT
from sqlalchemy.exc import IntegrityError
import random
from sqlalchemy import and_
from email.utils import formataddr

db = Database()

class UsuarioRepoImpl(UsuarioRepo):

    def create_user(self, nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, password, rol, asignaturas, programa):

        try:

            session = db.get_session()
            roles = self.validar_roles(rol)
            codigo_verificacion = self.generar_codigo()

            if roles:
                return roles

            if "ROLE_ADMIN" in rol and "ROLE_ESTUDIANTE" in rol:
                password_hashed = self.hashear_password(password)
                new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed, codigo_verificacion)
            
                carrera_encontrada = session.query(Carrera).filter(and_(Carrera.id == carrera, Carrera.activo == 1)).first()

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

                self.enviar_email(new_user.email, new_user.codigo_verificacion, new_user.nombre)
                session.close()
                return True
            
            elif "ROLE_ADMIN" in rol and "ROLE_DOCENTE" in rol:
                password_hashed = self.hashear_password(password)
                new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed, codigo_verificacion)
                
                programa_encontrado = session.query(Carrera).filter(and_(Carrera.id == programa, Carrera.activo == 1)).first()
                
                if programa_encontrado:
                    new_user.programas.append(programa_encontrado)
                else:
                    error = "Programa no encontrado"
                    return error
                
                for role in rol:
                    rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                    new_user.roles.append(rol_encontrado)

                validar_asignatura = self.validar_asignaturas(asignaturas)
                if validar_asignatura:
                    return validar_asignatura

                for asignatura in asignaturas:
                    asignatura_encontrada = session.query(Asignatura).filter(and_(Asignatura.id == asignatura, Asignatura.activo == 1)).first()
                    new_user.asignaturas.append(asignatura_encontrada)
                
                session.add(new_user)
                session.commit()
                self.enviar_email(new_user.email, new_user.codigo_verificacion, new_user.nombre)
                session.close()
                return True
            
            elif "ROLE_ADMIN" in rol:
                password_hashed = self.hashear_password(password)
                new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed, codigo_verificacion)
                for role in rol:
                    rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                    new_user.roles.append(rol_encontrado)
                session.add(new_user)
                session.commit()
                self.enviar_email(new_user.email, new_user.codigo_verificacion, new_user.nombre)
                session.close()
                return True
            
            elif "ROLE_ESTUDIANTE" in rol:
                password_hashed = self.hashear_password(password)
                new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed, codigo_verificacion)
                carrera_encontrada = session.query(Carrera).filter(and_(Carrera.id == carrera, Carrera.activo == 1)).first()
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
                self.enviar_email(new_user.email, new_user.codigo_verificacion, new_user.nombre)
                session.close()
                return True
            
            elif "ROLE_DOCENTE" in rol:
            
                password_hashed = self.hashear_password(password)
                new_user = Usuario(nombre, email, celular, tipo_identificacion, numero_identificacion, password_hashed, codigo_verificacion)

                programa_encontrado = session.query(Carrera).filter(and_(Carrera.id == programa, Carrera.activo == 1)).first()
                
                if programa_encontrado:
                    new_user.programas.append(programa_encontrado)
                else:
                    error = "Programa no encontrado"
                    return error

                for role in rol:
                    rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                    new_user.roles.append(rol_encontrado)

                validar_asignatura = self.validar_asignaturas(asignaturas)
                if validar_asignatura:
                    return validar_asignatura
            
                for asignatura in asignaturas:
                    asignatura_encontrada = session.query(Asignatura).filter(and_(Asignatura.id == asignatura, Asignatura.activo == 1)).first()
                    new_user.asignaturas.append(asignatura_encontrada) 
                
                session.add(new_user)
                session.commit()
                self.enviar_email(new_user.email, new_user.codigo_verificacion, new_user.nombre)
                session.close()
                return True
        except IntegrityError as e:
            raise e

    def inactive_user(self, user_id):
        session = db.get_session()
        usuario = session.query(Usuario).filter(and_(Usuario.id == user_id, Usuario.activo == 1)).first()

        if usuario:
            usuario.activo = 0
            session.commit()
            session.close()
            return True
        else:
            return False
        
    def update_user(self, nombre, email, celular, tipo_identificacion, numero_identificacion, carrera, rol, asignaturas, programa, user_id):
        try:

            session = db.get_session()
            user_found = session.query(Usuario).filter(and_(Usuario.numero_identificacion == user_id, Usuario.activo == 1)).first()

            if user_found:   
                roles = self.validar_roles(rol)

                if roles:
                    return roles

                if "ROLE_ADMIN" in rol and "ROLE_ESTUDIANTE" in rol:
                    user_found.nombre = nombre
                    user_found.email = email
                    user_found.celular = celular
                    user_found.tipo_identificacion = tipo_identificacion
                    user_found.numero_identificacion = numero_identificacion
                    user_found.carreras.clear()
                    
                    carrera_encontrada = session.query(Carrera).filter(and_(Carrera.id == carrera, Carrera.activo == 1)).first()

                    if carrera_encontrada:
                        user_found.carreras.append(carrera_encontrada)
                    else:
                        error = "Carrera no encontrada"
                        return error
                    
                    for role in rol:
                        rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                        user_found.roles.append(rol_encontrado)
                    
                    session.commit()
                    session.close()
                    return True
                
                elif "ROLE_ADMIN" in rol and "ROLE_DOCENTE" in rol:
                    user_found.nombre = nombre
                    user_found.email = email
                    user_found.celular = celular
                    user_found.tipo_identificacion = tipo_identificacion
                    user_found.numero_identificacion = numero_identificacion
                    user_found.programas.clear()

                    programa_encontrado = session.query(Carrera).filter(and_(Carrera.id == programa, Carrera.activo == 1)).first()
                    
                    if programa_encontrado:
                        user_found.programas.append(programa_encontrado)
                    else:
                        error = "Programa no encontrado"
                        return error
                    
                    for role in rol:
                        rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                        user_found.roles.append(rol_encontrado)

                    validar_asignatura = self.validar_asignaturas(asignaturas)
                    if validar_asignatura:
                        return validar_asignatura

                    for asignatura in asignaturas:
                        asignatura_encontrada = session.query(Asignatura).filter(and_(Asignatura.id == asignatura, Asignatura.activo == 1)).first()
                        user_found.asignaturas.append(asignatura_encontrada)
                    
                    session.commit()
                    session.close()
                    return True
                
                elif "ROLE_ADMIN" in rol:
                    user_found.nombre = nombre
                    user_found.email = email
                    user_found.celular = celular
                    user_found.tipo_identificacion = tipo_identificacion
                    user_found.numero_identificacion = numero_identificacion

                    for role in rol:
                        rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                        user_found.roles.append(rol_encontrado)
                    session.commit()
                    session.close()
                    return True
                
                elif "ROLE_ESTUDIANTE" in rol:
                    user_found.nombre = nombre
                    user_found.email = email
                    user_found.celular = celular
                    user_found.tipo_identificacion = tipo_identificacion
                    user_found.numero_identificacion = numero_identificacion
                    user_found.carreras.clear()

                    carrera_encontrada = session.query(Carrera).filter(and_(Carrera.id == carrera, Carrera.activo == 1)).first()
                    if carrera_encontrada:
                        user_found.carreras.append(carrera_encontrada)
                    else:
                        error = "Carrera no encontrada"
                        return error

                    for role in rol:
                        rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                        user_found.roles.append(rol_encontrado)
                    session.commit()
                    session.close()
                    return True
                
                elif "ROLE_DOCENTE" in rol:

                    user_found.nombre = nombre
                    user_found.email = email
                    user_found.celular = celular
                    user_found.tipo_identificacion = tipo_identificacion
                    user_found.numero_identificacion = numero_identificacion
                    user_found.programas.clear()

                    programa_encontrado = session.query(Carrera).filter(and_(Carrera.id == programa, Carrera.activo == 1)).first()
                    
                    if programa_encontrado:
                        user_found.programas.append(programa_encontrado)
                    else:
                        error = "Programa no encontrado"
                        return error

                    for role in rol:
                        rol_encontrado = session.query(Rol).filter(Rol.rol == role).first()
                        user_found.roles.append(rol_encontrado)

                    validar_asignatura = self.validar_asignaturas(asignaturas)
                    if validar_asignatura:
                        return validar_asignatura
                
                    for asignatura in asignaturas:
                        asignatura_encontrada = session.query(Asignatura).filter(and_(Asignatura.id == asignatura, Asignatura.activo == 1)).first()
                        user_found.asignaturas.append(asignatura_encontrada) 
                    
                    session.commit()
                    session.close()
                    return True
            else:
                return False
        except IntegrityError as e:
            raise e

    def inactive_user(self, user_id):
        session = db.get_session()
        usuario = session.query(Usuario).filter(and_(Usuario.numero_identificacion == user_id, Usuario.activo == 1)).first()

        if usuario:
            usuario.activo = 0
            session.commit()
            session.close()
            return True
        
    def enviar_email(self, email, codigo_verificacion, nombre):
        mail = current_app.extensions['mail']
        msg = Message("Código de verificación", sender=formataddr(("Tutorias ingenieria", "tutoriasingenierias@gmail.com")), recipients=[email])
        msg.html = render_template("codigo_verificacion.html", nombre = nombre, codigo_verificacion = codigo_verificacion)
        mail.send(msg)

    
    def generar_codigo(self):
        codigo_verificacion = random.randint(100000, 999999)
        return codigo_verificacion
    
    def verify_codigo(self, codigo):
        session = db.get_session()

        usuario_activado = session.query(Usuario).filter(and_(Usuario.codigo_verificacion == codigo, Usuario.activo == 0)).first()

        if usuario_activado:
            usuario_activado.activo = 1
            session.commit()

            mail = current_app.extensions['mail']
            msg = Message("Registro exitoso", sender=formataddr(("Tutorias ingenieria", "tutoriasingenierias@gmail.com")), recipients=[usuario_activado.email])
            msg.html = render_template("registro_exitoso.html", nombre = usuario_activado.nombre)
            mail.send(msg)
            session.close()
            return True
        else:
            return False
        
    def login(self, email, password):
        session = db.get_session()
        
        usuario = session.query(Usuario).filter(and_(Usuario.email == email, Usuario.activo == 1)).first()
        
        if usuario and pbkdf2_sha256.verify(password, usuario.password):
            roles = self.get_roles(usuario.email)
            additional_claims = {'roles' : roles}
            access_token = JWT.generate_access_token(identity=usuario.email, additional_claims=additional_claims)
            return access_token
        else:
            return False
        
    def change_password_generate_code(self, email):
        session = db.get_session()
        usuario = session.query(Usuario).filter(and_(Usuario.email == email, Usuario.activo == 1)).first()
        if usuario:
            codigo_verificacion = self.generar_codigo()
            change_password_code = CambioClave(usuario.id, codigo_verificacion)
            session.add(change_password_code)
            session.commit()

            mail = current_app.extensions['mail']
            msg = Message("Código de verificación cambio de contraseña", sender=formataddr(("Tutorias ingenieria", "tutoriasingenierias@gmail.com")), recipients=[usuario.email])
            msg.html = render_template("codigo_verificacion_password.html", nombre = usuario.nombre, codigo_verificacion = codigo_verificacion)
            mail.send(msg)
            session.close()
            return True
        else:
            return False
        
    def change_password(self, codigo, new_password):
        session = db.get_session()
        codigo_used = session.query(CambioClave).filter(and_(CambioClave.codigo_verificacion == codigo, CambioClave.used == 1)).first()
        if codigo_used:
            error = "El codigo anterior ya se uso"
            return error
        else:
            codigo_found = session.query(CambioClave).filter(and_(CambioClave.codigo_verificacion == codigo, CambioClave.used == 0)).first()
            if codigo_found:
                usuario = session.query(Usuario).filter(and_(Usuario.id == codigo_found.usuario_id, Usuario.activo == 1)).first()
                usuario.password = self.hashear_password(new_password)
                codigo_found.used = 1
                session.commit()

                session.close()
                return True
            else:
                return False

    def hashear_password(self, password):
        return pbkdf2_sha256.hash(password)
    
    def find_user(self, numero_documento):
        session = db.get_session()
        usuario = session.query(Usuario).filter(and_(Usuario.numero_identificacion == numero_documento, Usuario.activo == 1)).first()
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
                
            if "ROLE_ESTUDIANTE" in role:
                carreras = self.get_carreras(usuario.carreras)
                usuario_dict['carrera'] = carreras

            if "ROLE_DOCENTE" in role:
                programa = self.get_programa(usuario.programas)
                asignaturas = self.get_asignaturas(usuario.asignaturas)
                usuario_dict['programa'] = programa
                usuario_dict['asignaturas'] = asignaturas

        session.close()
        return usuario_dict
    
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
                
                if "ROLE_ESTUDIANTE" in role:
                    carreras = self.get_carreras(usuario.carreras)
                    usuario_dict['carrera'] = carreras

                if "ROLE_DOCENTE" in role:
                    programa = self.get_programa(usuario.programas)
                    asignaturas = self.get_asignaturas(usuario.asignaturas)
                    usuario_dict['programa'] = programa
                    usuario_dict['asignaturas'] = asignaturas
            usuarios_list.append(usuario_dict)

        session.close()
        return usuarios_list

    def get_users_estudiante(self):
        session = db.get_session()
        rol_estudiante = session.query(Rol).filter(Rol.rol == "ROLE_ESTUDIANTE").first()
        usuarios_estudiante = session.query(Usuario).filter(and_(Usuario.roles.contains(rol_estudiante), Usuario.activo == 1)).all()
        usuarios_list = []
        for usuario in usuarios_estudiante:
            roles = self.get_roles_by_usuario(usuario.roles)
            carreras = self.get_carreras(usuario.carreras)

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
        usuarios_admins = session.query(Usuario).filter(and_(Usuario.roles.contains(rol_admin), Usuario.activo == 1)).all()
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
        usuarios_docentes = session.query(Usuario).filter(and_(Usuario.roles.contains(rol_docente), Usuario.activo == 1)).all()
        usuarios_list = []
        for usuario in usuarios_docentes:
            roles = self.get_roles_by_usuario(usuario.roles)
            asignaturas = self.get_asignaturas(usuario.asignaturas)
            programa = self.get_programa(usuario.programas)
            usuario_dict = {
                'nombre' : usuario.nombre,
                'email' : usuario.email,
                'celular' : usuario.celular,
                'tipo_identificacion' : usuario.tipo_identificacion,
                'numero_identificacion' : usuario.numero_identificacion,
                'programa' : programa,
                'asignaturas' : asignaturas,
                'roles' : roles
            }
            usuarios_list.append(usuario_dict)

        session.close()        
        return usuarios_list
    

    def get_roles(self, email):
        session = db.get_session()
        usuario = session.query(Usuario).filter(and_(Usuario.email == email, Usuario.activo == 1)).first()
        roles_list = []
        for rol in usuario.roles:
            roles_list.append(rol.rol)
        session.close()
        return roles_list
    
    def user_information(self, email):
        session = db.get_session()
        usuario = session.query(Usuario).filter(and_(Usuario.email == email, Usuario.activo == 1)).first()
        roles_usuario = self.get_roles_by_usuario(usuario.roles)
        usuario_dict = {
            'nombre' : usuario.nombre,
            'email' : usuario.email,
            'celular' : usuario.celular,
            'tipo_identificacion' : usuario.tipo_identificacion,
            'numero_identificacion' : usuario.numero_identificacion,
            'roles' : roles_usuario
        }

        if any("ROLE_ESTUDIANTE" in rol for rol in roles_usuario):
            usuario_dict['carrera'] = self.get_carreras(usuario.carreras)
        elif any("ROLE_DOCENTE" in rol for rol in roles_usuario):
            usuario_dict['asignaturas'] = self.get_asignaturas(usuario.asignaturas)
        session.close()
        return usuario_dict
    
    def get_roles_by_usuario(self, roles):
        roles_list = []
        for rol in roles:
            roles_list.append(rol.rol)
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
    
    def get_programa(self, programas):
        programa_list = []
        for programa in programas:
            programa_list.append(programa.to_dict())
        return programa_list
    
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
            asignatura_encontrada = session.query(Asignatura).filter(and_(Asignatura.id == asignatura, Asignatura.activo == 1)).first()

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