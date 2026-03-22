from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario  # Muy importante: Flask-Login necesita 'id' para funcionar
        self.nombre = nombre
        self.email = email
        self.password = password

    # Esta pequeña clase es como el carnet de identidad 
    # del usuario dentro de tu sistema.
    