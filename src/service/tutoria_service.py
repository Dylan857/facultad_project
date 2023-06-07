class TutoriaService:
    def __init__(self, tutoria_repository):
        self.tutoria_repository = tutoria_repository

    def create_tutoria(self, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):
        return self.tutoria_repository.create_tutoria(docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id)
    
    def get_tutorias(self):
        return self.tutoria_repository.get_tutorias()
    
    def find_tutorias_by_docente(self, documento_docente):
        return self.tutoria_repository.find_tutoria_by_docente(documento_docente)
    
    def find_tutorias_by_fecha(self, fecha):
        return self.tutoria_repository.find_tutoria_by_fecha(fecha)
    
    def find_tutorias_by_asignatura(self, asignatura):
        return self.tutoria_repository.find_tutoria_by_asignatura(asignatura)