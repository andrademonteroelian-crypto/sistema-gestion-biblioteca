# ============================================================
# PROYECTO POO - PARCIAL 2
# GRUPO 1: Sistema de Gestión de Servicios de Biblioteca
# Jornada: Matutina
# Integrantes:
# - [ELIAN ANDRADE] (Jornada Vespertina)
# - [TOALA MOSERRATE JUAN]
# - [NACIPUCHA SUAREZ NATHALY]
# - [FLORE LOPEZ EYLEN]
# - [ZAMBRANO CORREA LISSETH]
# - [MAZZINI ZAMBRANO JENNIFER]
# ============================================================
# Capa: DATOS
# DAO (Data Access Object) para la entidad UsuarioBiblioteca.
# Es la única clase que ejecuta SQL directamente sobre la tabla de usuarios.
# Nunca conoce la GUI, solo recibe/devuelve objetos de Dominio.

from Datos import proveedor_bd
from Dominio.usuario_biblioteca import UsuarioBiblioteca


class UsuarioBibliotecaDAO:
    """
    DAO estático para insertar, buscar, actualizar, eliminar y listar
    usuarios de la biblioteca, contra SQL Server o SQLite (transparente).
    """

    @staticmethod
    def crear_tabla_si_no_existe():
        """Crea la tabla usuarios_biblioteca si todavía no existe."""
        cursor = proveedor_bd.obtener_cursor()
        if proveedor_bd.usando_sql_server():
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='usuarios_biblioteca' AND xtype='U')
                CREATE TABLE usuarios_biblioteca (
                    cedula VARCHAR(10) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(100) NOT NULL,
                    contrasena VARCHAR(100) NOT NULL
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios_biblioteca (
                    cedula VARCHAR(10) PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(100) NOT NULL,
                    contrasena VARCHAR(100) NOT NULL
                )
            """)
        proveedor_bd.confirmar_cambios()

    @staticmethod
    def insertar(usuario):
        """
        Inserta un nuevo usuario. Devuelve:
        1  -> éxito
        0  -> ya existe un usuario con esa cédula o correo (duplicado)
        -1 -> error inesperado
        """
        if UsuarioBibliotecaDAO.buscar_por_cedula(usuario.cedula) is not None:
            return 0
        if UsuarioBibliotecaDAO.buscar_por_correo(usuario.email) is not None:
            return 0
        try:
            cursor = proveedor_bd.obtener_cursor()
            cursor.execute(
                "INSERT INTO usuarios_biblioteca (cedula, nombre, correo, contrasena) VALUES (?,?,?,?)",
                (usuario.cedula, usuario.nombre, usuario.email, usuario.contrasena)
            )
            proveedor_bd.confirmar_cambios()
            return 1
        except Exception as e:
            print(e)
            proveedor_bd.deshacer_cambios()
            return -1

    @staticmethod
    def buscar_por_cedula(cedula):
        """Devuelve un UsuarioBiblioteca reconstruido, o None si no existe."""
        cursor = proveedor_bd.obtener_cursor()
        cursor.execute("SELECT cedula, nombre, correo, contrasena FROM usuarios_biblioteca WHERE cedula = ?", (cedula,))
        fila = cursor.fetchone()
        return UsuarioBibliotecaDAO._fila_a_objeto(fila) if fila else None

    @staticmethod
    def buscar_por_correo(correo):
        """Devuelve un UsuarioBiblioteca reconstruido, o None si no existe."""
        cursor = proveedor_bd.obtener_cursor()
        cursor.execute("SELECT cedula, nombre, correo, contrasena FROM usuarios_biblioteca WHERE correo = ?", (correo,))
        fila = cursor.fetchone()
        return UsuarioBibliotecaDAO._fila_a_objeto(fila) if fila else None

    @staticmethod
    def validar_credenciales(correo, contrasena):
        """Devuelve el UsuarioBiblioteca si correo+contraseña coinciden en la BD, o None."""
        usuario = UsuarioBibliotecaDAO.buscar_por_correo(correo)
        if usuario is not None and usuario.contrasena == contrasena:
            return usuario
        return None

    @staticmethod
    def actualizar(cedula_original, usuario_nuevo):
        """Actualiza un usuario existente. Usa la cédula ORIGINAL en el WHERE."""
        try:
            cursor = proveedor_bd.obtener_cursor()
            cursor.execute(
                "UPDATE usuarios_biblioteca SET cedula = ?, nombre = ?, correo = ?, contrasena = ? WHERE cedula = ?",
                (usuario_nuevo.cedula, usuario_nuevo.nombre, usuario_nuevo.email,
                 usuario_nuevo.contrasena, cedula_original)
            )
            proveedor_bd.confirmar_cambios()
            return 1
        except Exception as e:
            print(e)
            proveedor_bd.deshacer_cambios()
            return -1

    @staticmethod
    def eliminar(cedula):
        """Elimina un usuario por cédula."""
        try:
            cursor = proveedor_bd.obtener_cursor()
            cursor.execute("DELETE FROM usuarios_biblioteca WHERE cedula = ?", (cedula,))
            proveedor_bd.confirmar_cambios()
            return 1
        except Exception as e:
            print(e)
            proveedor_bd.deshacer_cambios()
            return -1

    @staticmethod
    def listar_todos():
        """Devuelve una lista de objetos UsuarioBiblioteca (nunca tuplas crudas)."""
        cursor = proveedor_bd.obtener_cursor()
        cursor.execute("SELECT cedula, nombre, correo, contrasena FROM usuarios_biblioteca")
        filas = cursor.fetchall()
        return [UsuarioBibliotecaDAO._fila_a_objeto(f) for f in filas]

    @staticmethod
    def _fila_a_objeto(fila):
        """Reconstruye un UsuarioBiblioteca a partir de una fila de la BD."""
        cedula, nombre, correo, contrasena = fila
        return UsuarioBiblioteca(nombre=nombre, id_usuario=cedula, email=correo,
                                  cedula=cedula, contrasena=contrasena)
