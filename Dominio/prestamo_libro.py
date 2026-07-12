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



from Dominio.servicio_biblioteca import ServicioBiblioteca


class PrestamoLibro(ServicioBiblioteca):
    """
    Clase hija para préstamo físico de libros.
    Hereda de ServicioBiblioteca.
    Regla: tiene multa por días de atraso.
    """

    COSTO_BASE = 5.0       # Precio base por préstamo físico
    MULTA_POR_DIA = 2.0    # Multa por cada día de atraso

    def __init__(self, codigo, titulo_recurso, fecha_prestamo, dias_prestamo, dias_atraso=0, cedula_usuario=""):
        """Llama al constructor de la clase padre y agrega su atributo propio."""
        super().__init__(codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario)
        self._dias_atraso = dias_atraso  # Guarda los días de atraso (atributo propio de esta hija)

    @property
    def dias_atraso(self):
        """Devuelve los días de atraso guardados."""
        return self._dias_atraso

    @dias_atraso.setter
    def dias_atraso(self, valor):
        """Valida que los días de atraso no sean negativos."""
        if valor < 0:
            raise ValueError("Los días de atraso no pueden ser negativos")
        self._dias_atraso = valor

    def calcular_costo(self):
        """Calcula el costo: base + multa por días de atraso."""
        multa = self.dias_atraso * self.MULTA_POR_DIA
        return self.COSTO_BASE + multa

    def mostrar_info(self):
        """Devuelve información del préstamo físico con costo y multa."""
        costo = self.calcular_costo()
        return f"Préstamo Físico -> {super().__str__()} | Atraso: {self.dias_atraso} días | Costo: ${costo:.2f}"

    def __str__(self):
        """Devuelve string con tipo, datos y costo calculado."""
        return self.mostrar_info()