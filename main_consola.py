# 1. Cambiamos la importación para usar tu MySQL
from Conexion.conexion import obtener_conexion

def mostrar_menu():
    print("\n--- SISTEMA DE VENTAS DE CALZADO (MYSQL - THE LION) ---")
    print("1. Agregar nuevo producto")
    print("2. Ver inventario")
    print("3. Registrar una venta")
    print("4. Salir")
    return input("Seleccione una opción: ")

def agregar_producto():
    nombre = input("Nombre del calzado: ")
    marca = input("Marca: ")
    talla = int(input("Talla: "))
    precio = float(input("Precio: "))
    stock = int(input("Cantidad en stock: "))

    # 2. Usamos la conexión a MySQL
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        # En MySQL se usa %s en lugar de ?
        sql = '''
            INSERT INTO productos (nombre, marca, talla, precio, stock)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (nombre, marca, talla, precio, stock))
        conexion.commit()
        conexion.close()
        print("¡Producto agregado con éxito en MySQL!")
    else:
        print("Error: No se pudo conectar a la base de datos.")

def ver_inventario():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        
        print("\n--- INVENTARIO ACTUAL DESDE MYSQL ---")
        for p in productos:
            # Ajustamos los índices según tu tabla de phpMyAdmin
            print(f"ID: {p[0]} | {p[1]} ({p[2]}) - Talla: {p[3]} - Precio: ${p[4]} - Stock: {p[5]}")
        conexion.close()
    else:
        print("Error de conexión.")

def main():
    # Nota: Ya no llamamos a crear_tablas() de SQLite porque
    # tus tablas ya existen físicamente en phpMyAdmin.
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            ver_inventario()
        elif opcion == "3":
            print("Función de venta en desarrollo...")
        elif opcion == "4":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
    