import sqlite3
import json
import csv

def conectar():
    return sqlite3.connect('sistema_ventas.db')

def guardar_producto(nombre, precio, stock, talla):
    try:
        # --- 1. GUARDAR EN BASE DE DATOS (Principal) ---
        conexion = conectar()
        cursor = conexion.cursor()
        
        sentencia = "INSERT INTO productos (nombre, precio, stock, talla) VALUES (?, ?, ?, ?)"
        cursor.execute(sentencia, (nombre, precio, stock, talla))
        
        conexion.commit()
        conexion.close()
        
        # --- 2. RESPALDO EN ARCHIVOS (Opcional pero útil) ---
        respaldar_en_archivos(nombre, precio, stock, talla)
        
        print(f"✅ ¡Producto '{nombre}' guardado y respaldado con éxito!")

    except Exception as e:
        print(f"❌ Error al guardar: {e}")

def respaldar_en_archivos(nombre, precio, stock, talla):
    """Función auxiliar para mantener tus archivos de data/ actualizados."""
    # Guardar en TXT
    with open('data/datos.txt', 'a', encoding='utf-8') as f:
        f.write(f"Producto: {nombre} | Precio: {precio} | Stock: {stock} | Talla: {talla}\n")

    # Guardar en CSV
    with open('data/datos.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, precio, stock, talla])
        