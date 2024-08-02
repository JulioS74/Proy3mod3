from flask_restful import Resource, reqparse
from models.productos import Productos
from db import db

class ReabastecerController(Resource):
    def post(self, producto_id,reabastecer ):
        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        producto.reabastecer(reabastecer)
        db.session.commit()
        return {'message': 'Producto reabastecido'}
