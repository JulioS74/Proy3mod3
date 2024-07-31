#models/productos.py
from db import db
from models.ingredientes import Ingredientes

class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    ingrediente1_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    ingrediente2_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))
    ingrediente3_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'))

    ingrediente1 = db.relationship('Ingredientes', foreign_keys=[ingrediente1_id])
    ingrediente2 = db.relationship('Ingredientes', foreign_keys=[ingrediente2_id])
    ingrediente3 = db.relationship('Ingredientes', foreign_keys=[ingrediente3_id])

    def __init__(self, nombre, precio, ingrediente1_id, ingrediente2_id=None, ingrediente3_id=None):
        self.nombre = nombre
        self.precio = precio
        self.ingrediente1_id = ingrediente1_id
        self.ingrediente2_id = ingrediente2_id
        self.ingrediente3_id = ingrediente3_id

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'ingrediente1_id': self.ingrediente1_id,
            'ingrediente2_id': self.ingrediente2_id,
            'ingrediente3_id': self.ingrediente3_id
        }

    def get_calorias(self):
        calorias = 0
        if self.ingrediente1:
            calorias += self.ingrediente1.calorias
        if self.ingrediente2:
            calorias += self.ingrediente2.calorias
        if self.ingrediente3:
            calorias += self.ingrediente3.calorias
        return calorias

    def get_rentabilidad(self):
        costo_produccion = self.get_costo_de_produccion()
        if costo_produccion == 0:
            return None
        return self.precio / costo_produccion

    def get_costo_de_produccion(self):
        costo = 0
        if self.ingrediente1:
            costo += self.ingrediente1.precio
        if self.ingrediente2:
            costo += self.ingrediente2.precio
        if self.ingrediente3:
            costo += self.ingrediente3.precio
        return costo

    def vender(self):
        if self.ingrediente1 and self.ingrediente1.inventario > 0:
            self.ingrediente1.inventario -= 1
        else:
            return False
        if self.ingrediente2 and self.ingrediente2.inventario > 0:
            self.ingrediente2.inventario -= 1
        else:
            return False
        if self.ingrediente3 and self.ingrediente3.inventario > 0:
            self.ingrediente3.inventario -= 1
        else:
            return False
        return True

    def reabastecer(self, cantidad):
        if self.ingrediente1:
            self.ingrediente1.reabastecer(cantidad)
        if self.ingrediente2:
            self.ingrediente2.reabastecer(cantidad)
        if self.ingrediente3:
            self.ingrediente3.reabastecer(cantidad)

    def renovar_inventario(self):
        if self.ingrediente1:
            self.ingrediente1.renovar_inventario()
        if self.ingrediente2:
            self.ingrediente2.renovar_inventario()
        if self.ingrediente3:
            self.ingrediente3.renovar_inventario()