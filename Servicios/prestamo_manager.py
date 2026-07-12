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
# Capa: SERVICIOS
# Orquesta la creación, edición, eliminación y consulta de préstamos
# (físicos y digitales). Traduce cualquier ValueError del Dominio a
# ErrorValidacion, y siempre guarda/lee a través del DAO — nunca en listas
# de Python que se pierdan al cerrar la app.

from Datos.prestamo_dao import PrestamoDAO
from Dominio.prestamo_libro import PrestamoLibro
from Dominio.prestamo_digital import PrestamoDigital
from Servicios.servicio_usuario_biblioteca import ErrorValidacion


class PrestamoManager:
    """
    Capa de negocio para préstamos de libros físicos y digitales.
    La GUI solo llama a estos métodos; nunca construye SQL ni objetos
    de Dominio directamente.
    """

    @staticmethod
    def _validar_comunes(codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario):
        if not codigo or not str(codigo).strip():
            raise ErrorValidacion("El código del préstamo es obligatorio.")
        if not titulo_recurso or not titulo_recurso.strip():
            raise ErrorValidacion("El título del recurso es obligatorio.")
        if not fecha_prestamo or not str(fecha_prestamo).strip():
            raise ErrorValidacion("La fecha de préstamo es obligatoria.")
        if not cedula_usuario or not str(cedula_usuario).strip():
            raise ErrorValidacion("Debe seleccionar el usuario que solicita el préstamo.")
        try:
            dias_prestamo = int(dias_prestamo)
        except (TypeError, ValueError):
            raise ErrorValidacion("Los días de préstamo deben ser un número entero.")
        if dias_prestamo <= 0:
            raise ErrorValidacion("Los días de préstamo deben ser mayores a cero.")
        return dias_prestamo

    @staticmethod
    def crear_prestamo_libro(codigo, titulo_recurso, fecha_prestamo, dias_prestamo, dias_atraso, cedula_usuario):
        """Valida y crea un préstamo de libro físico, persistido en la BD."""
        dias_prestamo = PrestamoManager._validar_comunes(
            codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario
        )
        try:
            dias_atraso = int(dias_atraso) if str(dias_atraso).strip() != "" else 0
        except (TypeError, ValueError):
            raise ErrorValidacion("Los días de atraso deben ser un número entero.")
        if dias_atraso < 0:
            raise ErrorValidacion("Los días de atraso no pueden ser negativos.")

        try:
            prestamo = PrestamoLibro(
                codigo=codigo.strip(), titulo_recurso=titulo_recurso.strip(),
                fecha_prestamo=str(fecha_prestamo).strip(), dias_prestamo=dias_prestamo,
                dias_atraso=dias_atraso, cedula_usuario=cedula_usuario.strip()
            )
        except ValueError as e:
            raise ErrorValidacion(str(e))

        resultado = PrestamoDAO.insertar(prestamo)
        if resultado == 0:
            raise ErrorValidacion("Ya existe un préstamo registrado con ese código.")
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al guardar el préstamo en la base de datos.")
        return prestamo

    @staticmethod
    def crear_prestamo_digital(codigo, titulo_recurso, fecha_prestamo, dias_prestamo, tipo_recurso, cedula_usuario):
        """Valida y crea un préstamo digital, persistido en la BD."""
        dias_prestamo = PrestamoManager._validar_comunes(
            codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario
        )
        if tipo_recurso not in ("ebook", "video"):
            raise ErrorValidacion("El tipo de recurso debe ser 'ebook' o 'video'.")

        try:
            prestamo = PrestamoDigital(
                codigo=codigo.strip(), titulo_recurso=titulo_recurso.strip(),
                fecha_prestamo=str(fecha_prestamo).strip(), dias_prestamo=dias_prestamo,
                tipo_recurso=tipo_recurso, cedula_usuario=cedula_usuario.strip()
            )
        except ValueError as e:
            raise ErrorValidacion(str(e))

        resultado = PrestamoDAO.insertar(prestamo)
        if resultado == 0:
            raise ErrorValidacion("Ya existe un préstamo registrado con ese código.")
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al guardar el préstamo en la base de datos.")
        return prestamo

    @staticmethod
    def actualizar_prestamo_libro(codigo_original, codigo, titulo_recurso, fecha_prestamo,
                                   dias_prestamo, dias_atraso, cedula_usuario):
        """Valida y actualiza un préstamo de libro existente."""
        dias_prestamo = PrestamoManager._validar_comunes(
            codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario
        )
        try:
            dias_atraso = int(dias_atraso) if str(dias_atraso).strip() != "" else 0
        except (TypeError, ValueError):
            raise ErrorValidacion("Los días de atraso deben ser un número entero.")
        if dias_atraso < 0:
            raise ErrorValidacion("Los días de atraso no pueden ser negativos.")

        try:
            prestamo = PrestamoLibro(
                codigo=codigo.strip(), titulo_recurso=titulo_recurso.strip(),
                fecha_prestamo=str(fecha_prestamo).strip(), dias_prestamo=dias_prestamo,
                dias_atraso=dias_atraso, cedula_usuario=cedula_usuario.strip()
            )
        except ValueError as e:
            raise ErrorValidacion(str(e))

        resultado = PrestamoDAO.actualizar(codigo_original, prestamo)
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al actualizar el préstamo.")
        return prestamo

    @staticmethod
    def actualizar_prestamo_digital(codigo_original, codigo, titulo_recurso, fecha_prestamo,
                                     dias_prestamo, tipo_recurso, cedula_usuario):
        """Valida y actualiza un préstamo digital existente."""
        dias_prestamo = PrestamoManager._validar_comunes(
            codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario
        )
        if tipo_recurso not in ("ebook", "video"):
            raise ErrorValidacion("El tipo de recurso debe ser 'ebook' o 'video'.")

        try:
            prestamo = PrestamoDigital(
                codigo=codigo.strip(), titulo_recurso=titulo_recurso.strip(),
                fecha_prestamo=str(fecha_prestamo).strip(), dias_prestamo=dias_prestamo,
                tipo_recurso=tipo_recurso, cedula_usuario=cedula_usuario.strip()
            )
        except ValueError as e:
            raise ErrorValidacion(str(e))

        resultado = PrestamoDAO.actualizar(codigo_original, prestamo)
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al actualizar el préstamo.")
        return prestamo

    @staticmethod
    def eliminar_prestamo(codigo):
        """Elimina un préstamo existente por código."""
        resultado = PrestamoDAO.eliminar(codigo)
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al eliminar el préstamo.")
        return resultado

    @staticmethod
    def obtener_prestamos():
        """Devuelve todos los préstamos, siempre consultando la BD."""
        return PrestamoDAO.listar_todos()
