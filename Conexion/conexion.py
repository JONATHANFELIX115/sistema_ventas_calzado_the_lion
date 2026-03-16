import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Establece la conexión con la base de datos MySQL en el puerto 3307."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='the_lion',
            port=3307  # <--- Este es el puerto específico que solicitaste
        )
        if conexion.is_connected():
            # print("Conexión establecida con éxito") # Opcional para depuración
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Bloque de prueba para verificar el puerto
if __name__ == "__main__":
    con = obtener_conexion()
    if con:
        print("¡Conexión exitosa a THE LION a través del puerto 3307!")
        con.close()
        