from flask import jsonify
from service.usuario_service import UsuarioService
from repository.repository_impl.usuario_repo_impl import UsuarioRepoImpl

usuario_repository = UsuarioRepoImpl()
usuario_service = UsuarioService(usuario_repository)

class JWTValidate:

    @staticmethod
    def validar_token_estudiante(current_user):

        response = {
            'status_code' : 401,
            'message' : 'Acceso no autorizado',
            'datos' : []
        }

        usuario_roles = usuario_service.get_roles(current_user)
        if any("ROLE_ESTUDIANTE" in rol.get('rol') or "ROLE_ADMIN" in rol.get('rol') for rol in usuario_roles):
            pass
        else:
            return response
            

    @staticmethod
    def validar_token_docente(current_user):
        response = {
            'status_code' : 401,
            'message' : 'Acceso no autorizado',
            'datos' : []
        }
        usuario_roles = usuario_service.get_roles(current_user)
        if any("ROLE_DOCENTE" in rol.get('rol') or "ROLE_ADMIN" in rol.get('rol') for rol in usuario_roles):
            pass
        else:
            return response

    @staticmethod
    def validar_token_admin(current_user):
        
        response = {
            'status_code' : 401,
            'message' : 'Acceso no autorizado',
            'datos' : []
        }

        usuario_roles = usuario_service.get_roles(current_user)
        if any("ROLE_ADMIN" in rol.get('rol') for rol in usuario_roles):
            pass
        else:
            return response
        
    def validar_token(current_user):

        response = {
            'status_code' : 401,
            'message' : 'Acceso no autorizado',
            'datos' : []
        }

        usuario_roles = usuario_service.get_roles(current_user)
        if any("ROLE_ADMIN" in rol.get('rol') or "ROLE_ESTUDIANTE" in rol.get('rol') or "ROLE_DOCENTE" in rol.get('rol') for rol in usuario_roles):
            pass
        else:
            return response