#app.py
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from dotenv import load_dotenv
import os

from db import db
from models.users import Users
from models.productos import Productos
from models.ingredientes import Ingredientes
from models.informacion import Informacion
from controllers.productos_controller import ProductosController
from controllers.ingredientes_controller import IngredientesController
from controllers.informacion_controller import InformacionController
from controllers.reabastecer_controller import ReabastecerController
from controllers.renovar_controller import RenovarController

# Cargar variables de entorno desde .env
load_dotenv()
#def crear_app():
# Crear la aplicación Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}/{os.getenv("SCHEMA_DB")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.urandom(24).hex()

db.init_app(app)  # Inicializar la base de datos
api = Api(app)  # Inicializar Flask-RESTful
login_manager = LoginManager(app)  # Inicializar Flask-Login
login_manager.login_view = "login"  # Vista de login para redirección

# Configurar la carga del usuario en Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# Ruta principal
@app.route("/")
def main():
    return render_template("home.html")

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user, remember=True)
            if user.is_admin_user():
                return redirect(url_for("listar_productos"))  # Redirigir a la sección de productos para administradores
            elif user.is_empleado_user():
                return redirect(url_for("listar_ingredientes"))  # Redirigir a la sección de ingredientes para empleados
            elif user.is_cliente_registrado():
                return redirect(url_for("listar_productos"))  # Redirigir a la sección de productos para clientes registrados
            else:
                return redirect(url_for("main"))  # Redirigir a la página principal para usuarios anónimos
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos.")

# Ruta para mostrar la información de la heladería
@app.route("/informacion")
@login_required
def informacion_heladeria():
    if current_user.is_admin_user() or current_user.is_empleado_user():
        informacion = Informacion.query.all()
        return render_template("informacion.html", informacion=informacion)
    else:
        abort(403)  # Acceso no autorizado

# Ruta para mostrar la lista de productos
@app.route("/productos")
def listar_productos():
    productos = Productos.query.all()

    # Calcula la rentabilidad solo si el usuario es un administrador
    rentabilidad = None
    if current_user.is_authenticated and current_user.is_admin_user():
        total_ingresos = sum([producto.precio for producto in productos])
        total_costos = sum([
            (producto.ingrediente1.precio if producto.ingrediente1 else 0) +
            (producto.ingrediente2.precio if producto.ingrediente2 else 0) +
            (producto.ingrediente3.precio if producto.ingrediente3 else 0)
            for producto in productos
        ])
        rentabilidad = total_ingresos - total_costos

    return render_template("productos.html", productos=productos, rentabilidad=rentabilidad)

# Ruta para mostrar la lista de ingredientes
@app.route("/ingredientes")
@login_required
def listar_ingredientes():
    if current_user.is_admin_user() or current_user.is_empleado_user():
        ingredientes = Ingredientes.query.all()
        return render_template("ingredientes.html", ingredientes=ingredientes)
    else:
        abort(403)  # Acceso no autorizado

# Ruta para mostrar la página de detalle de un producto
@app.route("/producto/<int:producto_id>")
def detalle_producto(producto_id):
    producto = Productos.query.get(producto_id)
    if not producto:
        abort(404)  # Producto no encontrado
    return render_template("detalle_producto.html", producto=producto)

# Ruta para mostrar la página de detalle de un ingrediente
@app.route("/ingrediente/<int:ingrediente_id>")
def detalle_ingrediente(ingrediente_id):
    ingrediente = Ingredientes.query.get(ingrediente_id)
    if not ingrediente:
        abort(404)  # Ingrediente no encontrado
    return render_template("detalle_ingrediente.html", ingrediente=ingrediente)

# Ruta para logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main"))

# Ruta para comprar un producto
@app.route("/comprar/<int:producto_id>", methods=["POST"])
@login_required
def comprar_producto(producto_id):
    producto = Productos.query.get(producto_id)
    if not producto:
        abort(404)  # Producto no encontrado

    ingredientes = [
        producto.ingrediente1,
        producto.ingrediente2,
        producto.ingrediente3
    ]
    # Verificar si hay suficiente inventario para todos los ingredientes
    for ingrediente in ingredientes:
        if ingrediente and ingrediente.inventario <= 0:
            flash(f"No hay suficiente inventario de {ingrediente.nombre}.", "error")
            return redirect(url_for("detalle_producto", producto_id=producto_id))

    # Reducir inventario de ingredientes
    for ingrediente in ingredientes:
        if ingrediente:
            ingrediente.inventario -= 1

    db.session.commit()
    flash(f"Has comprado {producto.nombre}. ¡Gracias por tu compra!", "success")
    return redirect(url_for("listar_productos"))

# Registro de los controladores de la API
api.add_resource(ProductosController, 
    '/api/productos', 
    '/api/productos/<int:producto_id>', 
    '/api/productos/nombre/<string:nombre>', 
    '/api/productos/calorias/<int:calorias>',
    '/api/productos/rentabilidad/<int:rentabilidad>', 
    '/api/productos/costoproduccion/<int:costoproduccion>',
    '/api/productos/vender/<int:producto_id>')

api.add_resource(IngredientesController, 
    '/api/ingredientes', 
    '/api/ingredientes/<int:ingrediente_id>', 
    '/api/ingredientes/nombre/<string:nombre>', 
    '/api/ingredientes/sano/<int:sano>')

api.add_resource(InformacionController, 
    '/api/informacion', 
    '/api/informacion/<int:informacion_id>')

api.add_resource(ReabastecerController,
    '/api/productos/reabastecer/<int:producto_id>/<int:reabastecer>')

api.add_resource(RenovarController,
    '/api/productos/renovar/<int:producto_id>')

if __name__ == "__main__":
    app.run(debug=True)
