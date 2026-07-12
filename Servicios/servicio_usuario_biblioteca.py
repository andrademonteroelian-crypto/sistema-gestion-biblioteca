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
# Reglas de negocio y validación de formato para usuarios de la biblioteca.
# La GUI nunca valida nada por sí misma: siempre llama a esta capa, que a su
# vez llama al DAO. Traduce cualquier error a un único tipo de excepción.

import re

from Datos.usuario_biblioteca_dao import UsuarioBibliotecaDAO
from Dominio.usuario_biblioteca import UsuarioBiblioteca

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ErrorValidacion(Exception):
    """Excepción única para cualquier error de validación en la capa de Servicios."""
    pass


class ServicioUsuarioBiblioteca:
    """
    Orquesta el registro y el inicio de sesión de usuarios, validando
    todos los campos ANTES de tocar la base de datos.
    """

    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise ErrorValidacion("El nombre completo es obligatorio.")

    @staticmethod
    def validar_cedula(cedula):
        if not cedula or not cedula.strip():
            raise ErrorValidacion("La cédula es obligatoria.")
        if not cedula.isdigit() or len(cedula) != 10:
            raise ErrorValidacion("La cédula debe tener exactamente 10 dígitos numéricos.")

    @staticmethod
    def validar_correo(correo):
        if not correo or not correo.strip():
            raise ErrorValidacion("El correo electrónico es obligatorio.")
        if not _PATRON_CORREO.match(correo.strip()):
            raise ErrorValidacion("Ingrese un correo electrónico válido.")

    @staticmethod
    def validar_contrasena(contrasena, confirmar):
        if not contrasena:
            raise ErrorValidacion("La contraseña es obligatoria.")
        if len(contrasena) < 6:
            raise ErrorValidacion("La contraseña debe tener al menos 6 caracteres.")
        if not any(c.isalpha() for c in contrasena) or not any(c.isdigit() for c in contrasena):
            raise ErrorValidacion("La contraseña debe combinar al menos una letra y un número.")
        if not confirmar:
            raise ErrorValidacion("Debe confirmar la contraseña.")
        if contrasena != confirmar:
            raise ErrorValidacion("Las contraseñas no coinciden.")

    @staticmethod
    def registrar_usuario(nombre, cedula, correo, contrasena, confirmar_contrasena):
        """
        Valida todos los campos y, solo si todo pasa, guarda el usuario
        real en la base de datos a través del DAO.
        """
        nombre = (nombre or "").strip()
        cedula = (cedula or "").strip()
        correo = (correo or "").strip()

        ServicioUsuarioBiblioteca.validar_nombre(nombre)
        ServicioUsuarioBiblioteca.validar_cedula(cedula)
        ServicioUsuarioBiblioteca.validar_correo(correo)
        ServicioUsuarioBiblioteca.validar_contrasena(contrasena, confirmar_contrasena)

        try:
            usuario = UsuarioBiblioteca(
                nombre=nombre, id_usuario=cedula, email=correo,
                cedula=cedula, contrasena=contrasena
            )
        except ValueError as e:
            raise ErrorValidacion(str(e))

        resultado = UsuarioBibliotecaDAO.insertar(usuario)
        if resultado == 0:
            raise ErrorValidacion("Ya existe un usuario registrado con esa cédula o correo.")
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al guardar el usuario en la base de datos.")
        return usuario

    @staticmethod
    def iniciar_sesion(correo, contrasena):
        """
        Valida credenciales contra la base de datos. Lanza ErrorValidacion
        si el correo/contraseña están vacíos o no coinciden con ningún usuario.
        """
        correo = (correo or "").strip()
        if not correo:
            raise ErrorValidacion("Ingrese su correo electrónico.")
        if not contrasena:
            raise ErrorValidacion("Ingrese su contraseña.")

        usuario = UsuarioBibliotecaDAO.validar_credenciales(correo, contrasena)
        if usuario is None:
            raise ErrorValidacion("Correo o contraseña incorrectos.")
        return usuario

    @staticmethod
    def actualizar_usuario(cedula_original, nombre, cedula, correo, contrasena, confirmar_contrasena):
        """Valida y actualiza un usuario existente."""
        nombre = (nombre or "").strip()
        cedula = (cedula or "").strip()
        correo = (correo or "").strip()

        ServicioUsuarioBiblioteca.validar_nombre(nombre)
        ServicioUsuarioBiblioteca.validar_cedula(cedula)
        ServicioUsuarioBiblioteca.validar_correo(correo)
        ServicioUsuarioBiblioteca.validar_contrasena(contrasena, confirmar_contrasena)

        try:
            usuario_nuevo = UsuarioBiblioteca(
                nombre=nombre, id_usuario=cedula, email=correo,
                cedula=cedula, contrasena=contrasena
            )
        except ValueError as e:
            raise ErrorValidacion(str(e))

        resultado = UsuarioBibliotecaDAO.actualizar(cedula_original, usuario_nuevo)
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al actualizar el usuario.")
        return usuario_nuevo

    @staticmethod
    def eliminar_usuario(cedula):
        """Elimina un usuario existente por cédula."""
        resultado = UsuarioBibliotecaDAO.eliminar(cedula)
        if resultado == -1:
            raise ErrorValidacion("Ocurrió un error al eliminar el usuario.")
        return resultado

    @staticmethod
    def obtener_usuarios():
        """Devuelve todos los usuarios registrados, siempre desde la BD."""
        return UsuarioBibliotecaDAO.listar_todos()
