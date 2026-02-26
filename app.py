from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_the_lion_key" # Para poder usar mensajes flash

# Función auxiliar para conectar a la DB
def get_db_connection():
    conn = sqlite3.connect('sistema_ventas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=('GET', 'POST'))
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        talla = request.form['talla']
        precio = request.form['precio']
        stock = request.form['stock']

        if not nombre:
            flash('¡El nombre es obligatorio!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO productos (nombre, marca, talla, precio, stock) VALUES (?, ?, ?, ?, ?)',
                         (nombre, marca, talla, precio, stock))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('producto.html')

@app.route('/eliminar/<int:id>', methods=('POST',))
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado correctamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    