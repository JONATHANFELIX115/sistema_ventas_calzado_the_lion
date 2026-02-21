from flask import Flask, render_template # Importamos render_template 

app = Flask(__name__)

@app.route('/')
def inicio():
    # Renderizamos el archivo index.html en lugar de solo texto 
    return render_template('index.html')

@app.route('/producto/<nombre>')
def producto(nombre):
    # Pasamos la variable 'nombre' a la plantilla producto.html 
    return render_template('producto.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
    