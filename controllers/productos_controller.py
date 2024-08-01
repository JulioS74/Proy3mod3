#controllers/productos_controller.py
from flask_restful import Resource, reqparse
from models.productos import Productos
from db import db

class ProductosController(Resource):
    
    # Método GET para obtener productos
    def get(self, producto_id=None, nombre=None, calorias=None, rentabilidad=None, costoproduccion=None):
        if producto_id:
            producto = Productos.query.get(producto_id)
            if producto:
                return producto.json()
            return {'message': 'Producto no encontrado'}, 404

        if nombre:
            producto = Productos.query.filter_by(nombre=nombre).first()
            if producto:
                return producto.json()
            return {'message': 'Producto no encontrado'}, 404

        if calorias is not None:
            producto = Productos.query.get(calorias)
            if producto:
                return {'calorias': producto.get_calorias()}
            return {'message': 'Producto no encontrado'}, 404

        if rentabilidad is not None:
            producto = Productos.query.get(rentabilidad)
            if producto:
                return {'rentabilidad': producto.get_rentabilidad()}
            return {'message': 'Producto no encontrado'}, 404

        if costoproduccion is not None:
            producto = Productos.query.get(costoproduccion)
            if producto:
                return {'costo_produccion': producto.get_costo_de_produccion()}
            return {'message': 'Producto no encontrado'}, 404

        productos = Productos.query.all()
        return [producto.json() for producto in productos]
    
    # Método PUT para actualizar un producto
    def put(self, producto_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str)
        parser.add_argument('precio', type=int)
        parser.add_argument('ingrediente1_id', type=int)
        parser.add_argument('ingrediente2_id', type=int)
        parser.add_argument('ingrediente3_id', type=int)
        data = parser.parse_args()

        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        if data['nombre']:
            producto.nombre = data['nombre']
        if data['precio']:
            producto.precio = data['precio']
        if data['ingrediente1_id']:
            producto.ingrediente1_id = data['ingrediente1_id']
        if data['ingrediente2_id']:
            producto.ingrediente2_id = data['ingrediente2_id']
        if data['ingrediente3_id']:
            producto.ingrediente3_id = data['ingrediente3_id']

        db.session.commit()
        return producto.json()
    
    # Método DELETE para eliminar un producto    
    def delete(self, producto_id):
        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        db.session.delete(producto)
        db.session.commit()
        return {'message': 'Producto eliminado'}    
    

    # Método POST para renovar el inventario del producto
    def put(self, producto_id):
        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        producto.renovar_inventario()
        db.session.commit()
        return {'message': 'Inventario renovado'}

    # Método POST para vender un producto
    def post(self, producto_id):
        producto = Productos.query.get(producto_id)
        if not producto:
            return {'message': 'Producto no encontrado'}, 404

        if producto.vender():
            db.session.commit()
            return {'message': 'Producto vendido'}
        return {'message': 'No hay suficiente inventario'}, 400