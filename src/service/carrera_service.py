class CarreraService:
    def __init__(self, carrera_repository):
        self.carrera_repository = carrera_repository


    def get_carreras(self):
        return self.carrera_repository.get_carreras()