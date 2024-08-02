#models/informacion.py
from db import db

class Informacion(db.Model):
    __tablename__ = 'informacion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(250), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
