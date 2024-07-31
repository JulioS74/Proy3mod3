CREATE DATABASE heladeria;
USE heladeria;

DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS ingredientes;
DROP TABLE IF EXISTS informacion;
DROP TABLE IF EXISTS user;

CREATE TABLE ingredientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio INT NOT NULL,
    calorias INT NOT NULL,
    inventario INT NOT NULL,
    es_vegetariano TINYINT(1) NOT NULL
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    ingrediente1_id INT,
    ingrediente2_id INT,
    ingrediente3_id INT,
    FOREIGN KEY (ingrediente1_id) REFERENCES ingredientes(id),
    FOREIGN KEY (ingrediente2_id) REFERENCES ingredientes(id),
    FOREIGN KEY (ingrediente3_id) REFERENCES ingredientes(id)
);

CREATE TABLE informacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(250) NOT NULL,
    telefono CHAR(20) NOT NULL
);

CREATE TABLE user(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_admin TINYINT(1) NOT NULL,
    is_empleado TINYINT(1) NOT NULL
);

INSERT INTO ingredientes (nombre, precio, calorias, inventario, es_vegetariano)
VALUES 
    ('Chispas de Chocolate', 4000, 50, 30, 1),
    ('Coco Rayado', 2500, 60, 20, 1),
    ('Dulce de Mora', 4500, 120, 10, 1),
    ('Crema de Leche', 1000, 110, 8, 0),
    ('Helado de Chocolate', 3000, 112, 52, 0),
    ('Helado de Fresa', 3500, 90, 84, 0),
    ('Helado de Vainilla', 3600, 80, 80, 0),
    ('Pulpa de Fresa', 4000, 60, 50, 1),
    ('Pulpa de Mora', 3500, 60, 50, 1),
    ('Leche Entera', 2500 ,40, 100, 0),
    ('Arequipe', 2000 ,130, 30, 0),
    ('Azucar', 1000 ,120, 60, 0);

INSERT INTO productos (nombre, precio, ingrediente1_id, ingrediente2_id, ingrediente3_id)
VALUES
    ('Copa', 8000, 7, 6, 3),
    ('Malteada', 10000, 5 , 4, 10),
    ('Vaso', 7000, 6, 2, 3),
    ('Jugo', 6000, 9, 10, 11);

INSERT INTO informacion (nombre, direccion, telefono)
VALUES
    ('Helados&Malteadas', 'Carrera 26 N° 84 -12', '315256984');

INSERT INTO user (username, password, is_admin, is_empleado)
VALUES
    ('Julio', '0810', 1, 0),
    ('Ana', '2684', 0, 0),
    ('Violeta', '3130', 0, 1);
