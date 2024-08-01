#controllers/reabastecer_controller.py
from flask_restful import Resource, reqparse
from models.productos import Productos
from db import db

class ReabastecerController(Resource):
    def post_reabastecer(self, producto_id):
        parser = reqparse.RequestParser()
        parser.add_argument('cantidad', type=int, required=True)
        args = parser.parse_args()
        cantidad = args['cantidad']
        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        producto.reabastecer(cantidad)
        db.session.commit()
        return {'message': 'Producto reabastecido'}