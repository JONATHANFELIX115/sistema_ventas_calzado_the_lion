import sqlite3

# Clase Producto: Define los atributos de cada zapato
class Producto:
    def __init__(self, id, nombre, categoria, precio, stock):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

# Clase Inventario: Gestiona la lógica y la conexión a SQLite
class Inventario:
    def __init__(self):
        self.db_path = 'sistema_ventas.db'
        self._conectar_db()

    # Método privado para crear la tabla si no existe
    def _conectar_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           nombre TEXT, 
                           marca TEXT, 
                           precio REAL, 
                           stock INTEGER)''')
        conn.commit()
        conn.close()

    # READ: Retorna una LISTA (Colección) de objetos tipo Producto
    def obtener_todos(self):
        lista_productos = []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        for row in rows:
            # Creamos el objeto y lo añadimos a la lista
            p = Producto(row['id'], row['nombre'], row['marca'], row['precio'], row['stock'])
            lista_productos.append(p)
        conn.close()
        return lista_productos

    # CREATE: Añade un nuevo ítem
    def añadir_producto(self, nombre, categoria, precio, stock):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (nombre, marca, precio, stock) VALUES (?, ?, ?, ?)',
                       (nombre, categoria, precio, stock))
        conn.commit()
        conn.close()

    # DELETE: Elimina por ID
    def eliminar_producto(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        conn.close() 
        # UPDATE: Actualizar stock o precio
    def actualizar_producto(self, id, nuevo_precio, nuevo_stock):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET precio = ?, stock = ? WHERE id = ?',
                       (nuevo_precio, nuevo_stock, id))
        conn.commit()
        conn.close()

    # SEARCH: Buscar por nombre y devolver una LISTA (Colección)
    def buscar_por_nombre(self, nombre_buscado):
        lista_resultados = []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Usamos LIKE para búsquedas parciales
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre_buscado + '%',))
        rows = cursor.fetchall()
        for row in rows:
            p = Producto(row['id'], row['nombre'], row['marca'], row['precio'], row['stock'])
            lista_resultados.append(p)
        conn.close()
        return lista_resultados 