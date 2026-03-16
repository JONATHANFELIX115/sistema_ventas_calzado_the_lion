from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv

app = Flask(__name__)

# --- 1. CONFIGURACIÓN PARA MYSQL (XAMPP Puerto 3307) ---
# Cambiamos SQLite por MySQL
# usuario: root | contraseña: (vacía) | host: localhost | puerto: 3307 | base de datos: the_lion
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/the_lion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 2. MODELO DE DATOS ---
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    # Agregué 'marca' porque vi que la tienes en tu tabla de phpMyAdmin
    marca = db.Column(db.String(100), nullable=True) 
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    talla = db.Column(db.Integer, nullable=False)

# --- 3. GUARDADO EN ARCHIVOS (Se mantiene exactamente igual) ---
def guardar_en_archivos(p):
    data_dir = "inventario/data/"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    prod_dict = {'nombre': p.nombre, 'precio': p.precio, 'stock': p.stock, 'talla': p.talla}

    with open(data_dir + "datos.txt", "a") as f:
        f.write(f"{p.nombre} - Talla: {p.talla}\n")
    
    json_file = data_dir + "datos.json"
    lista = []
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, "r") as f: lista = json.load(f)
    lista.append(prod_dict)
    with open(json_file, "w") as f: json.dump(lista, f, indent=4)
    
    with open(data_dir + "datos.csv", "a", newline='') as f:
        csv.writer(f).writerow([p.nombre, p.precio, p.stock, p.talla])

# --- 4. RUTAS ---

@app.route('/')
def index():
    # Ahora trae los datos de MySQL en lugar de SQLite
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nuevo = Producto(
        nombre=request.form.get('nombre'),
        marca=request.form.get('marca'), # Se captura del formulario
        precio=float(request.form.get('precio')),
        stock=int(request.form.get('stock')),
        talla=int(request.form.get('talla'))
    )
    db.session.add(nuevo)
    db.session.commit()
    guardar_en_archivos(nuevo) # Sigue funcionando para tus reportes
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    p = Producto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/buscar')
def buscar():
    q = request.args.get('query')
    res = Producto.query.filter(Producto.nombre.contains(q)).all() if q else []
    return render_template('index.html', productos=res, busqueda=True)

if __name__ == '__main__':
    with app.app_context():
        # Crea las tablas en MySQL si no existen
        db.create_all()
    app.run(debug=True)
    