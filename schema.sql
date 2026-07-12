-- Proyecto Segundo Parcial - GUI con Base de Datos
-- Asignatura: Programación Orientada a Objetos
-- Tema: Sistema de Gestión de Servicios de Biblioteca
-- Integrantes:
-- - Elian Andrade
-- - Toala Moserrate Juan
-- - Nacipucha Suarez Nathaly
-- - Flore Lopez Eylen
-- - Zambrano Correa Lisseth
-- - Mazzini Zambrano Jennifer
--
-- Script SQL de evidencia con la estructura de las tablas usadas por el sistema.
-- NOTA: la aplicación crea la base de datos y estas tablas automáticamente
-- al arrancar (ver Datos/conexion.py, Datos/usuario_biblioteca_dao.py y
-- Datos/prestamo_dao.py, métodos crear_tabla_si_no_existe). Este script
-- se entrega como evidencia y NO es requerido para ejecutar la app.
--
-- La conexión usa autenticación de Windows (Trusted_Connection=yes),
-- servidor ELIANANDRADE\SQLANDRADEELIANM, base de datos "Biblioteca".
--
-- Versión escrita para SQL Server. Si se ejecuta sobre SQLite, cambiar:
--   VARCHAR(n) -> TEXT, INT -> INTEGER

-- ============================================================
-- Tabla: usuarios_biblioteca
-- Usuarios que pueden registrarse e iniciar sesión en el sistema.
-- ============================================================
USE Biblioteca;
GO
CREATE TABLE usuarios_biblioteca (
    cedula      VARCHAR(10)  PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    correo      VARCHAR(150) NOT NULL,
    contrasena  VARCHAR(100) NOT NULL
);

-- ============================================================
-- Tabla: prestamos
-- Guarda tanto PrestamoLibro como PrestamoDigital (polimorfismo).
-- El campo "tipo" indica cuál de los dos es cada fila:
--   'LIBRO'   -> usa dias_atraso  (tipo_recurso queda NULL)
--   'DIGITAL' -> usa tipo_recurso (dias_atraso queda NULL)
-- ============================================================
CREATE TABLE prestamos (
    codigo          VARCHAR(20)  PRIMARY KEY,
    tipo            VARCHAR(10)  NOT NULL,
    titulo_recurso  VARCHAR(150) NOT NULL,
    fecha_prestamo  VARCHAR(20)  NOT NULL,
    dias_prestamo   INT          NOT NULL,
    cedula_usuario  VARCHAR(10)  NOT NULL,
    dias_atraso     INT          NULL,
    tipo_recurso    VARCHAR(10)  NULL,

    CONSTRAINT fk_prestamos_usuario FOREIGN KEY (cedula_usuario)
        REFERENCES usuarios_biblioteca (cedula)
);
