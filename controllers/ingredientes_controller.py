#controllers/ingredientes_controller.py
from flask_restful import Resource, reqparse
from models.ingredientes import Ingredientes
from db import db

class IngredientesController(Resource):
    
    def get(self, ingrediente_id=None, nombre=None, sano=None):
        if ingrediente_id:
            ingrediente = Ingredientes.query.get(ingrediente_id)
            if ingrediente:
                return ingrediente.json()
            return {'message': 'Ingrediente no encontrado'}, 404

        if nombre:
            ingrediente = Ingredientes.query.filter_by(nombre=nombre).first()
            if ingrediente:
                return ingrediente.json()
            return {'message': 'Ingrediente no encontrado'}, 404

        if sano is not None:
            ingrediente = Ingredientes.query.get(sano)
            if ingrediente:
                return {'es_saludable': ingrediente.es_saludable()}
            return {'message': 'Ingrediente no encontrado'}, 404

        ingredientes = Ingredientes.query.all()
        return [ingrediente.json() for ingrediente in ingredientes]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str, required=True)
        parser.add_argument('precio', type=int, required=True)
        parser.add_argument('calorias', type=int, required=True)
        parser.add_argument('inventario', type=int, required=True)
        parser.add_argument('es_vegetariano', type=bool, required=True)
        data = parser.parse_args()

        ingrediente = Ingredientes(
            nombre=data['nombre'],
            precio=data['precio'],
            calorias=data['calorias'],
            inventario=data['inventario'],
            es_vegetariano=data['es_vegetariano']
        )
        db.session.add(ingrediente)
        db.session.commit()
        return ingrediente.json(), 201

    def put(self, ingrediente_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre', type=str)
        parser.add_argument('precio', type=int)
        parser.add_argument('calorias', type=int)
        parser.add_argument('inventario', type=int)
        parser.add_argument('es_vegetariano', type=bool)
        data = parser.parse_args()

        ingrediente = Ingredientes.query.get(ingrediente_id)
        if not ingrediente:
            return {'message': 'Ingrediente no encontrado'}, 404

        if data['nombre']:
            ingrediente.nombre = data['nombre']
        if data['precio']:
            ingrediente.precio = data['precio']
        if data['calorias']:
            ingrediente.calorias = data['calorias']
        if data['inventario']:
            ingrediente.inventario = data['inventario']
        if data['es_vegetariano'] is not None:
            ingrediente.es_vegetariano = data['es_vegetariano']

        db.session.commit()
        return ingrediente.json()

    def delete(self, ingrediente_id):
        ingrediente = Ingredientes.query.get(ingrediente_id)
        if not ingrediente:
            return {'message': 'Ingrediente no encontrado'}, 404

        db.session.delete(ingrediente)
        db.session.commit()
        return {'message': 'Ingrediente eliminado'}
