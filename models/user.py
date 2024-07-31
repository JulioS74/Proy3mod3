#user.py
from flask_login import UserMixin
from db import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_empleado = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, username, password, is_admin, is_empleado):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_empleado = is_empleado

    def is_admin_user(self):
        return self.is_admin

    def is_empleado_user(self):
        return self.is_empleado

    def is_cliente_registrado(self):
        return not self.is_admin and not self.is_empleado

    def is_user_anonimo(self):
        # Un usuario anónimo es aquel que no está autenticado.
        return not self.is_admin and not self.is_empleado and not self.is_cliente_registrado