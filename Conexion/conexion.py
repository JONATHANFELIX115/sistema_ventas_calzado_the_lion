import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """
    Establece la conexión usando mysql.connector siguiendo la instrucción A.
    """
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  
            # Actualizado según la instrucción A:
            database='sistemas_ventas_calzado_the_lion', 
            port=3307
        )
        
        if conexion.is_connected():
            return conexion

    except Error as e:
        print(f"Error crítico al conectar: {e}")
        return None

if __name__ == "__main__":
    con = obtener_conexion()
    if con:
        print("✅ Conexión exitosa a 'sistemas_ventas_calzado_the_lion'")
        con.close()
    else:
        print("❌ Error de conexión.")  
        