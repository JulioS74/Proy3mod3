from flask_restful import Resource
from models.productos import Productos
from db import db

class RenovarController(Resource):
    def post(self, producto_id):
        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404
        
        producto.renovar_inventario()
        db.session.commit()
        return {'message': 'Inventario renovado'}