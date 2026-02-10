from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'Bienvenido a Almacén The Lion – Sistema de Venta de Calzado'

@app.route('/producto/<nombre>')
def producto(nombre):
    return f'Producto: {nombre} – Disponible en Almacén The Lion'

if __name__ == '__main__':
    app.run(debug=True)

