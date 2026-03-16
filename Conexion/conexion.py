import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='the_lion',
            port=3307
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

if __name__ == "__main__":
    con = obtener_conexion()
    if con:
        print("Conexión exitosa a 'the_lion' en el puerto 3307")
        con.close()
        