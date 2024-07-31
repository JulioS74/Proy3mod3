from flask_restful import Resource
from models.informacion import Informacion

class InformacionController(Resource):
    def get(self):
        informacion = Informacion.query.all()
        return [info.to_dict() for info in informacion], 200
