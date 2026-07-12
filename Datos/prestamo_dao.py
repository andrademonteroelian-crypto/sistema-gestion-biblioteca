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
# DAO para PrestamoLibro y PrestamoDigital. Usa UNA sola tabla ("prestamos")
# con una columna "tipo" ('LIBRO' / 'DIGITAL') para distinguir el subtipo,
# igual que el patrón de referencia (servicio_academico_dao.py). Las columnas
# propias de cada subtipo (dias_atraso / tipo_recurso) quedan NULL cuando
# no aplican.

from Datos import proveedor_bd
from Dominio.prestamo_libro import PrestamoLibro
from Dominio.prestamo_digital import PrestamoDigital


class PrestamoDAO:
    """
    DAO estático para insertar, buscar, actualizar, eliminar y listar
    préstamos (físicos y digitales), contra SQL Server o SQLite.
    """

    @staticmethod
    def crear_tabla_si_no_existe():
        cursor = proveedor_bd.obtener_cursor()
        if proveedor_bd.usando_sql_server():
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='prestamos' AND xtype='U')
                CREATE TABLE prestamos (
                    codigo VARCHAR(20) PRIMARY KEY,
                    tipo VARCHAR(10) NOT NULL,
                    titulo_recurso VARCHAR(150) NOT NULL,
                    fecha_prestamo VARCHAR(20) NOT NULL,
                    dias_prestamo INT NOT NULL,
                    cedula_usuario VARCHAR(10) NOT NULL,
                    dias_atraso INT NULL,
                    tipo_recurso VARCHAR(10) NULL
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prestamos (
                    codigo VARCHAR(20) PRIMARY KEY,
                    tipo VARCHAR(10) NOT NULL,
                    titulo_recurso VARCHAR(150) NOT NULL,
                    fecha_prestamo VARCHAR(20) NOT NULL,
                    dias_prestamo INT NOT NULL,
                    cedula_usuario VARCHAR(10) NOT NULL,
                    dias_atraso INT NULL,
                    tipo_recurso VARCHAR(10) NULL
                )
            """)
        proveedor_bd.confirmar_cambios()

    @staticmethod
    def insertar(prestamo):
        """
        Inserta un préstamo (PrestamoLibro o PrestamoDigital, detectado por tipo).
        Devuelve 1 éxito, 0 código duplicado, -1 error.
        """
        if PrestamoDAO.buscar_por_codigo(prestamo.codigo) is not None:
            return 0
        try:
            cursor = proveedor_bd.obtener_cursor()
            if isinstance(prestamo, PrestamoLibro):
                cursor.execute(
                    """INSERT INTO prestamos
                       (codigo, tipo, titulo_recurso, fecha_prestamo, dias_prestamo,
                        cedula_usuario, dias_atraso, tipo_recurso)
                       VALUES (?,?,?,?,?,?,?,NULL)""",
                    (prestamo.codigo, 'LIBRO', prestamo.titulo_recurso, prestamo.fecha_prestamo,
                     prestamo.dias_prestamo, prestamo.cedula_usuario, prestamo.dias_atraso)
                )
            elif isinstance(prestamo, PrestamoDigital):
                cursor.execute(
                    """INSERT INTO prestamos
                       (codigo, tipo, titulo_recurso, fecha_prestamo, dias_prestamo,
                        cedula_usuario, dias_atraso, tipo_recurso)
                       VALUES (?,?,?,?,?,?,NULL,?)""",
                    (prestamo.codigo, 'DIGITAL', prestamo.titulo_recurso, prestamo.fecha_prestamo,
                     prestamo.dias_prestamo, prestamo.cedula_usuario, prestamo.tipo_recurso)
                )
            else:
                return -1
            proveedor_bd.confirmar_cambios()
            return 1
        except Exception as e:
            print(e)
            proveedor_bd.deshacer_cambios()
            return -1

    @staticmethod
    def buscar_por_codigo(codigo):
        """Devuelve un PrestamoLibro/PrestamoDigital reconstruido, o None."""
        cursor = proveedor_bd.obtener_cursor()
        cursor.execute(
            """SELECT codigo, tipo, titulo_recurso, fecha_prestamo, dias_prestamo,
                      cedula_usuario, dias_atraso, tipo_recurso
               FROM prestamos WHERE codigo = ?""",
            (codigo,)
        )
        fila = cursor.fetchone()
        return PrestamoDAO._fila_a_objeto(fila) if fila else None

    @staticmethod
    def actualizar(codigo_original, prestamo_nuevo):
        """Actualiza un préstamo existente. Usa el código ORIGINAL en el WHERE."""
        try:
            cursor = proveedor_bd.obtener_cursor()
            if isinstance(prestamo_nuevo, PrestamoLibro):
                cursor.execute(
                    """UPDATE prestamos SET codigo=?, tipo='LIBRO', titulo_recurso=?, fecha_prestamo=?,
                       dias_prestamo=?, cedula_usuario=?, dias_atraso=?, tipo_recurso=NULL
                       WHERE codigo = ?""",
                    (prestamo_nuevo.codigo, prestamo_nuevo.titulo_recurso, prestamo_nuevo.fecha_prestamo,
                     prestamo_nuevo.dias_prestamo, prestamo_nuevo.cedula_usuario,
                     prestamo_nuevo.dias_atraso, codigo_original)
                )
            elif isinstance(prestamo_nuevo, PrestamoDigital):
                cursor.execute(
                    """UPDATE prestamos SET codigo=?, tipo='DIGITAL', titulo_recurso=?, fecha_prestamo=?,
                       dias_prestamo=?, cedula_usuario=?, dias_atraso=NULL, tipo_recurso=?
                       WHERE codigo = ?""",
                    (prestamo_nuevo.codigo, prestamo_nuevo.titulo_recurso, prestamo_nuevo.fecha_prestamo,
                     prestamo_nuevo.dias_prestamo, prestamo_nuevo.cedula_usuario,
                     prestamo_nuevo.tipo_recurso, codigo_original)
                )
            else:
                return -1
            proveedor_bd.confirmar_cambios()
            return 1
        except Exception as e:
            print(e)
            proveedor_bd.deshacer_cambios()
            return -1

    @staticmethod
    def eliminar(codigo):
        """Elimina un préstamo por código."""
        try:
            cursor = proveedor_bd.obtener_cursor()
            cursor.execute("DELETE FROM prestamos WHERE codigo = ?", (codigo,))
            proveedor_bd.confirmar_cambios()
            return 1
        except Exception as e:
            print(e)
            proveedor_bd.deshacer_cambios()
            return -1

    @staticmethod
    def listar_todos():
        """Devuelve una lista de objetos PrestamoLibro/PrestamoDigital (todos los préstamos)."""
        cursor = proveedor_bd.obtener_cursor()
        cursor.execute(
            """SELECT codigo, tipo, titulo_recurso, fecha_prestamo, dias_prestamo,
                      cedula_usuario, dias_atraso, tipo_recurso
               FROM prestamos"""
        )
        filas = cursor.fetchall()
        return [PrestamoDAO._fila_a_objeto(f) for f in filas]

    @staticmethod
    def listar_por_usuario(cedula_usuario):
        """Devuelve solo los préstamos que pertenecen a un usuario dado."""
        cursor = proveedor_bd.obtener_cursor()
        cursor.execute(
            """SELECT codigo, tipo, titulo_recurso, fecha_prestamo, dias_prestamo,
                      cedula_usuario, dias_atraso, tipo_recurso
               FROM prestamos WHERE cedula_usuario = ?""",
            (cedula_usuario,)
        )
        filas = cursor.fetchall()
        return [PrestamoDAO._fila_a_objeto(f) for f in filas]

    @staticmethod
    def _fila_a_objeto(fila):
        """
        Reconstruye un objeto de Dominio a partir de una fila de la BD.
        Decide si arma un PrestamoLibro o un PrestamoDigital según la columna 'tipo'.
        """
        codigo, tipo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario, dias_atraso, tipo_recurso = fila
        if tipo == 'LIBRO':
            return PrestamoLibro(
                codigo=codigo, titulo_recurso=titulo_recurso, fecha_prestamo=fecha_prestamo,
                dias_prestamo=dias_prestamo, dias_atraso=dias_atraso or 0, cedula_usuario=cedula_usuario
            )
        else:
            return PrestamoDigital(
                codigo=codigo, titulo_recurso=titulo_recurso, fecha_prestamo=fecha_prestamo,
                dias_prestamo=dias_prestamo, tipo_recurso=tipo_recurso or "ebook", cedula_usuario=cedula_usuario
            )
