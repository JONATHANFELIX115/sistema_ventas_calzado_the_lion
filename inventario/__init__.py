from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# 1. Creamos la aplicación de Flask
app = Flask(__name__)

# 2. Configuración de seguridad (Clave secreta)
# Cambia 'tu_clave_secreta_aqui' por algo difícil de adivinar
app.config['SECRET_KEY'] = 'mi_secreto_super_seguro_123'

# 3. Inicializamos las herramientas de seguridad y login
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Configuramos la ruta hacia donde se redirige si no hay sesión iniciada
login_manager.login_view = 'login'
login_manager.login_message = "Inicia sesión para acceder."
login_manager.login_message_category = "info"

# 4. Importamos las rutas (esto debe ir al FINAL para evitar errores)
# Nota: Si tu archivo principal de rutas se llama productos.py, ponlo aquí
# from inventario import productos
