import sqlite3

def crear_tablas():
    # Establecemos la conexión con la base de datos (se creará el archivo si no existe)
    conexion = sqlite3.connect('sistema_ventas.db')
    cursor = conexion.cursor()

    # 1. Tabla de Productos (Calzado)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT,
            talla INTEGER NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # 2. Tabla de Ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos y tablas configuradas correctamente.")

if __name__ == "__main__":
    crear_tablas()
    