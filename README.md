Informe Técnico: Sistema de Gestión de Inventario "The Lion"
1. Introducción

Este proyecto consiste en un sistema avanzado de gestión de inventarios para la tienda de calzado "The Lion". El objetivo principal es integrar los pilares de la Programación Orientada a Objetos (POO) con persistencia de datos en SQLite y el uso eficiente de colecciones en Python para optimizar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
2. Estructura de Clases (POO)

Se han implementado dos clases principales que encapsulan la lógica de negocio:

    Clase Producto: Representa la entidad individual de calzado. Contiene atributos como ID, nombre, categoría, precio y stock. Incluye métodos para actualizar precio y stock, cumpliendo con los requisitos de métodos de acceso y modificación.

    Clase Inventario: Es el controlador central que gestiona la interacción entre la base de datos SQLite y la colección en memoria.

3. Implementación y Uso de Colecciones

Se seleccionó el Diccionario (dict) como la colección principal para cumplir con el manejo eficiente de ítems:

    Búsqueda Rápida: El diccionario utiliza el ID del producto como clave, permitiendo búsquedas con una complejidad de O(1).

    Gestión de Memoria: Al cargar los datos de SQLite en el productos_dict, el sistema evita realizar consultas constantes al disco, mejorando la velocidad de respuesta tanto en la consola como en la interfaz web.

4. Persistencia con SQLite

El almacenamiento se realiza en una base de datos local llamada the_lion_inventory.db.

    Tabla calzado: Almacena de forma permanente la información (ID, nombre, categoría, precio, stock).

    Conectividad: Se utiliza el módulo sqlite3. Cada operación CRUD actualiza la base de datos y sincroniza inmediatamente la colección en memoria para garantizar la integridad de los datos.

5. Operaciones CRUD e Interfaz

El sistema ofrece dos interfaces funcionales:

    Menú de Consola (main_consola.py): Interfaz interactiva para administrar el inventario directamente desde la terminal.

    Interfaz Web (Flask): Aplicación renderizada que permite la gestión visual y amigable del inventario.

6. Instrucciones de Ejecución

    Activar el entorno virtual: .\venv\Scripts\activate

    Instalar dependencias: pip install -r requirements.txt

    Ejecutar servidor web: python app.py

7. Enlaces del Proyecto

    Repositorio GitHub: https://github.com/JONATHANFELIX115/sistema_ventas_calzado_the_lion

    Aplicativo en la Nube: https://sistema-ventas-calzado-the-lion-2.onrender.com

8. Conclusiones y Aprendizajes

    Dominio de POO: Se aplicó la encapsulación y abstracción para crear un código mantenible.

    Eficiencia: El uso de diccionarios demostró ser superior a las listas para búsquedas por ID único.

    Despliegue Real: Se logró configurar un entorno de producción en Render utilizando gunicorn y manejando correctamente las dependencias. 