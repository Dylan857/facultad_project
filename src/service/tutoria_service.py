from sqlalchemy.exc import DataError
class TutoriaService:
    def __init__(self, tutoria_repository):
        self.tutoria_repository = tutoria_repository

    def create_tutoria(self, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id, tema_desarrollar):
        try:
            return self.tutoria_repository.create_tutoria(docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id, tema_desarrollar)
        except DataError as e:
            raise e
    
    def get_tutorias(self):
        return self.tutoria_repository.get_tutorias()
    
    def find_tutorias_by_docente(self, documento_docente):
        return self.tutoria_repository.find_tutoria_by_docente(documento_docente)
    
    def find_tutorias_by_fecha(self, fecha):
        return self.tutoria_repository.find_tutoria_by_fecha(fecha)
    
    def find_tutorias_by_asignatura(self, asignatura):
        return self.tutoria_repository.find_tutoria_by_asignatura(asignatura)
    
    def update_tutoria(self, id, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id):
        try:
            return self.tutoria_repository.update_tutoria(id, docente_id, fecha, hora_inicio, hora_fin, estudiantes, asignatura_id)
        except DataError as e:
            raise e
        
    def delete_tutoria(self, id):
        return self.tutoria_repository.delete_tutoria(id)
    
    def find_tutoria_between_dates(self, fecha_inicio, fecha_final):
        return self.tutoria_repository.find_tutoria_between_dates(fecha_inicio, fecha_final)
    
    def find_tutoria_between_dates_docente(self, fecha_inicio, fecha_final, documento_docente):
        return self.tutoria_repository.find_tutoria_between_dates_docente(fecha_inicio, fecha_final, documento_docente)

    def find_tutoria_by_docente_asignatura(self, documento_docente, asignatura):
        return self.tutoria_repository.find_tutoria_by_docente_asignatura(documento_docente, asignatura)
    
    def find_tutoria_by_fecha_asignatura(self, fecha, asignatura):
        return self.tutoria_repository.find_tutoria_by_fecha_asignatura(fecha, asignatura)
    
    def find_tutoria_by_docente_fecha(self, documento_docente, fecha):
        return self.tutoria_repository.find_tutoria_by_docente_fecha(documento_docente, fecha)
    
    def find_tutoria_by_docente_fecha_asignatura(self, documento_docente, fecha, asignatura):
        return self.tutoria_repository.find_tutoria_by_docente_fecha_asignatura(documento_docente, fecha, asignatura)
    
    def find_tutoria_by_id(self, id_tutoria):
        return self.tutoria_repository.find_tutoria_by_id(id_tutoria)
    
    def get_tutorias_soon(self, documento_docente):
        return self.tutoria_repository.get_tutorias_soon(documento_docente)
    
    def count_tutorias_month_by_docente(self, documento_docente):
        return self.tutoria_repository.count_tutorias_month_by_docente(documento_docente)
    
    def count_tutorias_week_by_docente(self, documento_docente):
        return self.tutoria_repository.count_tutorias_week_by_docente(documento_docente)
    
    def count_tutorias_day_by_docente(self, documento_docente):
        return self.tutoria_repository.count_tutorias_day_by_docente(documento_docente)
    
    def get_tutorias_soon_admin(self):
        return self.tutoria_repository.get_tutorias_soon_admin()
    
    def count_tutorias_month_admin(self):
        return self.tutoria_repository.count_tutorias_month_admin()
    
    def count_tutorias_week_admin(self):
        return self.tutoria_repository.count_tutorias_week_admin()
    
    def count_tutorias_day_admin(self):
        return self.tutoria_repository.count_tutorias_day_admin()
    
    def tutorias_day(self):
        return self.tutoria_repository.tutorias_day()
    
    def tutorias_day_docente(self, documento_docente):
        return self.tutoria_repository.tutorias_day_docente(documento_docente)