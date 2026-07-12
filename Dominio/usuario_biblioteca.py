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


class UsuarioBiblioteca:
    """
    Clase adicional que representa un usuario de la biblioteca.
    """

    def __init__(self, nombre, id_usuario, email, cedula, contrasena=""):
        """Constructor que recibe y guarda los datos del usuario."""
        self._nombre = nombre          # Guarda el nombre del usuario (privado)
        self._id_usuario = id_usuario  # Guarda el ID único (privado)
        self._email = email            # Guarda el correo electrónico (privado)
        self._cedula = cedula          # Guarda la cédula del usuario (privado)
        self._contrasena = contrasena  # Guarda la contraseña del usuario (privado)

    @property
    def nombre(self):
        """Devuelve el nombre guardado."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida que el nombre no esté vacío."""
        if valor == "":
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor

    @property
    def id_usuario(self):
        """Devuelve el ID guardado."""
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        """Valida que el ID no esté vacío."""
        if valor == "":
            raise ValueError("El ID no puede estar vacío")
        self._id_usuario = valor

    @property
    def email(self):
        """Devuelve el email guardado."""
        return self._email

    @email.setter
    def email(self, valor):
        """Valida que el email no esté vacío."""
        if valor == "":
            raise ValueError("El email no puede estar vacío")
        self._email = valor

    @property
    def cedula(self):
        """Devuelve la cédula guardada."""
        return self._cedula

    @cedula.setter
    def cedula(self, valor):
        """Valida que la cédula tenga exactamente 10 dígitos numéricos."""
        if valor == "":
            raise ValueError("La cédula no puede estar vacía")
        if not str(valor).isdigit() or len(str(valor)) != 10:
            raise ValueError("La cédula debe tener exactamente 10 dígitos numéricos")
        self._cedula = valor

    @property
    def contrasena(self):
        """Devuelve la contraseña guardada."""
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        """Valida que la contraseña tenga al menos 6 caracteres."""
        if valor == "" or valor is None:
            raise ValueError("La contraseña no puede estar vacía")
        if len(str(valor)) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self._contrasena = valor

    def __str__(self):
        """Devuelve string con los datos del usuario."""
        return f"Usuario: {self.nombre} | ID: {self.id_usuario} | Email: {self.email} | Cédula: {self.cedula}"