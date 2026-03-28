-- Script de Base de Datos - Sistemas Ventas Calzado The Lion
-- Este archivo crea la base, la tabla de usuarios y la de productos

CREATE DATABASE IF NOT EXISTS sistemas_ventas_calzado_the_lion;
USE sistemas_ventas_calzado_the_lion;

-- 1. Estructura para el Login (Tu avance actual)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- 2. Estructura para el Inventario (Lo que pide el docente)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- 3. Datos de prueba para que el docente vea contenido de una vez
INSERT INTO productos (nombre, marca, precio, stock) VALUES 
('Air Max 270', 'Nike', 120.00, 15),
('UltraBoost', 'Adidas', 180.00, 10),
('Classic Leather', 'Reebok', 75.00, 20);



