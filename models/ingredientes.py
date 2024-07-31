#models/ingredientes.py
from db import db

class Ingredientes(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, nullable=False)

    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano):
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.inventario = inventario
        self.es_vegetariano = es_vegetariano

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'calorias': self.calorias,
            'inventario': self.inventario,
            'es_vegetariano': self.es_vegetariano
        }

    def es_saludable(self):
        return self.calorias < 100 and self.es_vegetariano

    def reabastecer(self, cantidad):
        self.inventario += cantidad

    def renovar_inventario(self):
        self.inventario = 100
