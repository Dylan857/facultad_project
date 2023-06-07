class SolicitudRepository:

    def get_solicitudes(self):
        raise NotImplementedError
    
    def get_solicitud_by_docente(self, id):
        raise NotImplementedError
    
    def make_a_request(self, estudiante_id, docente_id, descripcion_solicitud):
        raise NotImplementedError