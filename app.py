from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import json
import csv

app = Flask(__name__)

# --- 1. CONFIGURACIÓN ---
# Conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/the_lion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clavedeseguridad_the_lion_2026'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Configuración del Guardián de Sesiones
login_manager.login_view = 'login' 
login_manager.login_message = "Por favor, inicia sesión para acceder al sistema."
login_manager.login_message_category = "info"

# --- 2. MODELOS DE DATOS ---

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=True) 
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    talla = db.Column(db.Integer, nullable=False)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    # id_usuario mapeado a 'id' para compatibilidad con flask-login
    id = db.Column('id_usuario', db.Integer, primary_key=True) 
    nombre = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- 3. FUNCIONES DE APOYO (Persistencia) ---

def guardar_en_archivos(p):
    data_dir = "inventario/data/"
    if not os.path.exists(data_dir): 
        os.makedirs(data_dir)
    
    prod_dict = {'nombre': p.nombre, 'precio': p.precio, 'stock': p.stock, 'talla': p.talla}
    
    # TXT
    with open(os.path.join(data_dir, "datos.txt"), "a") as f: 
        f.write(f"{p.nombre} - Talla: {p.talla}\n")
    
    # JSON
    json_file = os.path.join(data_dir, "datos.json")
    lista = []
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        try:
            with open(json_file, "r") as f: 
                lista = json.load(f)
        except json.JSONDecodeError:
            lista = []
    lista.append(prod_dict)
    with open(json_file, "w") as f: 
        json.dump(lista, f, indent=4)
    
    # CSV
    with open(os.path.join(data_dir, "datos.csv"), "a", newline='') as f:
        csv.writer(f).writerow([p.nombre, p.precio, p.stock, p.talla])

# --- 4. RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('mail')
        clave = request.form.get('password')
        usuario = Usuario.query.filter_by(mail=email).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, clave):
            login_user(usuario)
            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        nuevo_usuario = Usuario(
            nombre=request.form.get('nombre'),
            mail=request.form.get('mail'),
            password=hashed_password
        )
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Error: El correo electrónico ya existe.', 'warning')
    return render_template('registrar.html')

# --- 5. RUTAS DEL INVENTARIO (CRUD TOTALMENTE PROTEGIDO) ---

@app.route('/')
@login_required # <--- PROTEGIDO
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
@login_required # <--- PROTEGIDO
def agregar_producto():
    try:
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
        flash('Producto agregado correctamente.', 'success')
    except:
        db.session.rollback()
        flash('Error al agregar el producto.', 'danger')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
@login_required # <--- PROTEGIDO
def editar(id):
    producto = Producto.query.get_or_404(id)
    return render_template('editar.html', producto=producto)

@app.route('/actualizar/<int:id>', methods=['POST'])
@login_required # <--- PROTEGIDO
def actualizar(id):
    p = Producto.query.get_or_404(id)
    try:
        p.nombre = request.form.get('nombre')
        p.marca = request.form.get('marca')
        p.talla = int(request.form.get('talla'))
        p.precio = float(request.form.get('precio'))
        p.stock = int(request.form.get('stock'))
        db.session.commit()
        flash('Producto actualizado.', 'success')
    except:
        db.session.rollback()
        flash('Error al actualizar.', 'danger')
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
@login_required # <--- PROTEGIDO
def eliminar(id):
    p = Producto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Producto eliminado.', 'info')
    return redirect(url_for('index'))

# --- 6. EJECUCIÓN ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
    from flask import Flask, render_template, redirect, url_for, make_response
from services.producto_service import ProductoService, generar_pdf_productos
from forms.producto_form import ProductoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

@app.route('/productos')
def listar_productos():
    productos = ProductoService.listar_todos()
    return render_template('productos/index.html', productos=productos)

@app.route('/productos/reporte')
def reporte_pdf():
    productos = ProductoService.listar_todos()
    pdf_content = generar_pdf_productos(productos)
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_inventario.pdf'
    return response

# Aquí agregarías las rutas de crear, editar y eliminar usando ProductoService
