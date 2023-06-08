class TutoriaRepo:
    def create_tutoria(self, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):
        raise NotImplementedError
    def get_tutorias(self):
        raise NotImplementedError
    def find_tutoria_by_docente(self, documento_docente):
        raise NotImplementedError
    def find_tutoria_by_fecha(self, fecha):
        raise NotImplementedError
    def find_tutoria_by_asignatura(self, asignatura):
        raise NotImplementedError
    def update_tutoria(self, id, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):
        raise NotImplementedError
    def delete_tutoria(self, id):
        raise NotImplementedError