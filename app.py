from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv

app = Flask(__name__)

# --- 1. CONFIGURACIÓN PARA MYSQL (XAMPP Puerto 3307) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/the_lion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 2. MODELO DE DATOS ---
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=True) 
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    talla = db.Column(db.Integer, nullable=False)

# --- 3. GUARDADO EN ARCHIVOS ---
def guardar_en_archivos(p):
    data_dir = "inventario/data/"
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    prod_dict = {'nombre': p.nombre, 'precio': p.precio, 'stock': p.stock, 'talla': p.talla}
    
    with open(data_dir + "datos.txt", "a") as f: f.write(f"{p.nombre} - Talla: {p.talla}\n")
    json_file = data_dir + "datos.json"
    lista = []
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, "r") as f: lista = json.load(f)
    lista.append(prod_dict)
    with open(json_file, "w") as f: json.dump(lista, f, indent=4)
    with open(data_dir + "datos.csv", "a", newline='') as f:
        csv.writer(f).writerow([p.nombre, p.precio, p.stock, p.talla])

# --- 4. RUTAS (CRUD COMPLETO) ---

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nuevo = Producto(
        nombre=request.form.get('nombre'),
        marca=request.form.get('marca'),
        precio=float(request.form.get('precio')),
        stock=int(request.form.get('stock')),
        talla=int(request.form.get('talla'))
    )
    db.session.add(nuevo)
    db.session.commit()
    guardar_en_archivos(nuevo)
    return redirect(url_for('index'))

# NUEVA RUTA: Ver el formulario de edición
@app.route('/editar/<int:id>')
def editar(id):
    producto = Producto.query.get_or_404(id)
    return render_template('editar.html', producto=producto)

# NUEVA RUTA: Guardar los cambios del producto
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    p = Producto.query.get_or_404(id)
    p.nombre = request.form.get('nombre')
    p.marca = request.form.get('marca')
    p.talla = int(request.form.get('talla'))
    p.precio = float(request.form.get('precio'))
    p.stock = int(request.form.get('stock'))
    
    db.session.commit()
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
        db.create_all()
    app.run(debug=True)
    