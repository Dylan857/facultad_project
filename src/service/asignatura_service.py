class AsignaturaService:
    def __init__(self, asignatura_repository):
        self.asignatura_repository = asignatura_repository

    
    def get_asignaturas(self):
        return self.asignatura_repository.get_asignaturas()