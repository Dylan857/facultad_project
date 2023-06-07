class SolicitudService:
    def __init__(self, solicitud_repository):
        self.solicitud_repository = solicitud_repository


    def get_solicitudes(self):
        return self.solicitud_repository.get_solicitudes()
    
    def get_solicitud_by_docente(self, id):
        return self.solicitud_repository.get_solicitud_by_docente(id)
    
    def make_a_request(self, estudiante_id, docente_id, descripcion_solicitud):
        return self.solicitud_repository.make_a_request(estudiante_id, docente_id, descripcion_solicitud)
