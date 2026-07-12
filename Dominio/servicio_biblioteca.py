# ============================================================
# PROYECTO POO - PARCIAL 1
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


class ServicioBiblioteca:
    """
    Clase base para todos los préstamos de la biblioteca.
    Define atributos comunes y métodos que las subclases deben implementar.
    """

    def __init__(self, codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario=""):
        """Constructor que recibe y guarda los datos del préstamo."""
        self._codigo = codigo                  # Guarda el código del préstamo (privado)
        self._titulo_recurso = titulo_recurso  # Guarda el título del libro o recurso (privado)
        self._fecha_prestamo = fecha_prestamo  # Guarda la fecha de inicio (privado)
        self._dias_prestamo = dias_prestamo    # Guarda la cantidad de días del préstamo (privado)
        self._cedula_usuario = cedula_usuario  # Cédula del usuario que pidió el préstamo (privado)

    # --- Propiedades con encapsulamiento ---

    @property
    def codigo(self):
        """Devuelve el código guardado."""
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        """Valida que el código no esté vacío antes de guardar."""
        if valor == "":
            raise ValueError("El código no puede estar vacío")
        self._codigo = valor

    @property
    def titulo_recurso(self):
        """Devuelve el título guardado."""
        return self._titulo_recurso

    @titulo_recurso.setter
    def titulo_recurso(self, valor):
        """Valida que el título no esté vacío antes de guardar."""
        if valor == "":
            raise ValueError("El título no puede estar vacío")
        self._titulo_recurso = valor

    @property
    def fecha_prestamo(self):
        """Devuelve la fecha guardada."""
        return self._fecha_prestamo

    @fecha_prestamo.setter
    def fecha_prestamo(self, valor):
        """Guarda la nueva fecha."""
        self._fecha_prestamo = valor

    @property
    def dias_prestamo(self):
        """Devuelve los días guardados."""
        return self._dias_prestamo

    @dias_prestamo.setter
    def dias_prestamo(self, valor):
        """Valida que los días sean mayores a cero antes de guardar."""
        if valor <= 0:
            raise ValueError("Los días deben ser mayores a cero")
        self._dias_prestamo = valor

    @property
    def cedula_usuario(self):
        """Devuelve la cédula del usuario que pidió el préstamo."""
        return self._cedula_usuario

    @cedula_usuario.setter
    def cedula_usuario(self, valor):
        """Valida que la cédula del usuario no esté vacía antes de guardar."""
        if valor == "" or valor is None:
            raise ValueError("Debe indicarse el usuario que solicita el préstamo")
        self._cedula_usuario = valor

    def calcular_costo(self):
        """Método abstracto: cada subclase define su propio cálculo de costo."""
        raise NotImplementedError("Debe implementarse en la subclase")

    def mostrar_info(self):
        """Método abstracto: cada subclase define su propia información."""
        raise NotImplementedError("Debe implementarse en la subclase")

    def __str__(self):
        """Devuelve string con los datos básicos del préstamo."""
        return f"Código: {self.codigo} | Título: {self.titulo_recurso} | Fecha: {self.fecha_prestamo} | Días: {self.dias_prestamo}"