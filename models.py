import sqlite3

# 1. La "Entidad" Producto
class Producto:
    def __init__(self, id, nombre, categoria, precio, stock, talla):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria # También puedes llamarlo 'marca'
        self.precio = precio
        self.stock = stock
        self.talla = talla

# 2. El "Gestor" de la Base de Datos
class Inventario:
    def __init__(self):
        self.db_path = 'sistema_ventas.db'
        self._conectar_db()

    def _conectar_db(self):
        """Crea la tabla con todos los campos necesarios incluyendo TALLA."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           nombre TEXT NOT NULL, 
                           categoria TEXT, 
                           precio REAL NOT NULL, 
                           stock INTEGER NOT NULL,
                           talla TEXT)''')
        conn.commit()
        conn.close()

    def añadir_producto(self, nombre, categoria, precio, stock, talla):
        """Inserta un nuevo zapato en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO productos (nombre, categoria, precio, stock, talla) 
                          VALUES (?, ?, ?, ?, ?)''',
                       (nombre, categoria, precio, stock, talla))
        conn.commit()
        conn.close()

    def obtener_todos(self):
        """Retorna una lista de objetos tipo Producto."""
        lista_productos = []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        for row in rows:
            p = Producto(row['id'], row['nombre'], row['categoria'], 
                         row['precio'], row['stock'], row['talla'])
            lista_productos.append(p)
        conn.close()
        return lista_productos

    def eliminar_producto(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def actualizar_producto(self, id, nuevo_precio, nuevo_stock, nueva_talla):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''UPDATE productos 
                          SET precio = ?, stock = ?, talla = ? 
                          WHERE id = ?''',
                       (nuevo_precio, nuevo_stock, nueva_talla, id))
        conn.commit()
        conn.close()
        