from flask import Flask, render_template, request, redirect, url_for
from models import Inventario # Importamos nuestra clase

app = Flask(__name__)

# Instanciamos el objeto único de Inventario (POO)
mi_inventario = Inventario()

@app.route('/')
def index():
    # Usamos el método de la clase para obtener la colección de objetos
    productos = mi_inventario.obtener_todos()
    return render_template('index.html', productos=productos)

@app.route('/agregar_web', methods=['POST'])
def agregar_web():
    nombre = request.form.get('nombre')
    categoria = request.form.get('categoria')
    precio = float(request.form.get('precio'))
    stock = int(request.form.get('stock'))
    
    # Llamamos al método de la clase
    mi_inventario.añadir_producto(nombre, categoria, precio, stock)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Llamamos al método de la clase
    mi_inventario.eliminar_producto(id)
    return redirect(url_for('index'))
@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query')
    if query:
        # Usamos el método de búsqueda de la clase Inventario
        resultados = mi_inventario.buscar_por_nombre(query)
    else:
        resultados = []
    return render_template('index.html', productos=resultados, busqueda=True) 
if __name__ == '__main__':
    app.run(debug=True)
