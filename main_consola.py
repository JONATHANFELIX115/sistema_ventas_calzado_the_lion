import sqlite3
from models import crear_tablas

def mostrar_menu():
    print("\n--- SISTEMA DE VENTAS DE CALZADO ---")
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

    conexion = sqlite3.connect('sistema_ventas.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, marca, talla, precio, stock)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, marca, talla, precio, stock))
    conexion.commit()
    conexion.close()
    print("¡Producto agregado con éxito!")

def ver_inventario():
    conexion = sqlite3.connect('sistema_ventas.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    
    print("\n--- INVENTARIO ACTUAL ---")
    for p in productos:
        print(f"ID: {p[0]} | {p[1]} ({p[2]}) - Talla: {p[3]} - Precio: ${p[4]} - Stock: {p[5]}")
    conexion.close()

def main():
    # Aseguramos que las tablas existan al iniciar
    crear_tablas()
    
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
    