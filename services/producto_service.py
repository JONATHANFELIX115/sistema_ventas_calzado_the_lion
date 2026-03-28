from conexion.conexion import obtener_conexion

class ProductoService:
    @staticmethod
    def listar_todos():
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        db.close()
        return productos

    @staticmethod
    def crear(nombre, precio, stock, marca):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock, marca) VALUES (%s, %s, %s, %s)", 
                       (nombre, precio, stock, marca))
        db.commit()
        db.close()

    @staticmethod
    def eliminar(id_producto):
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        db.commit()
        db.close()
        from fpdf import FPDF

def generar_pdf_productos(productos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Reporte de Inventario - The Lion", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(80, 10, "Producto", 1)
    pdf.cell(40, 10, "Marca", 1)
    pdf.cell(30, 10, "Precio", 1)
    pdf.cell(30, 10, "Stock", 1)
    pdf.ln()

    pdf.set_font("Arial", '', 12)
    for p in productos:
        pdf.cell(80, 10, str(p['nombre']), 1)
        pdf.cell(40, 10, str(p['marca']), 1)
        pdf.cell(30, 10, f"${p['precio']}", 1)
        pdf.cell(30, 10, str(p['stock']), 1)
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')
