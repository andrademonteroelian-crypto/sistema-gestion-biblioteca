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


class PrestamoDigital(ServicioBiblioteca):
    """
    Clase hija para préstamo digital de recursos.
    Hereda de ServicioBiblioteca.
    Regla: costo según tiempo de acceso o tipo de recurso.
    """

    COSTO_POR_DIA_EBOOK = 1.5   # Precio por día de e-book
    COSTO_POR_DIA_VIDEO = 3.0    # Precio por día de video

    def __init__(self, codigo, titulo_recurso, fecha_prestamo, dias_prestamo, tipo_recurso="ebook", cedula_usuario=""):
        """Llama al constructor de la clase padre y agrega su atributo propio."""
        super().__init__(codigo, titulo_recurso, fecha_prestamo, dias_prestamo, cedula_usuario)
        self._tipo_recurso = tipo_recurso  # Guarda el tipo de recurso: "ebook" o "video"

    @property
    def tipo_recurso(self):
        """Devuelve el tipo de recurso guardado."""
        return self._tipo_recurso

    @tipo_recurso.setter
    def tipo_recurso(self, valor):
        """Valida que el tipo sea solo 'ebook' o 'video'."""
        if valor not in ["ebook", "video"]:
            raise ValueError("El tipo debe ser 'ebook' o 'video'")
        self._tipo_recurso = valor

    def calcular_costo(self):
        """Calcula el costo según el tipo de recurso."""
        if self.tipo_recurso == "ebook":
            return self.dias_prestamo * self.COSTO_POR_DIA_EBOOK
        return self.dias_prestamo * self.COSTO_POR_DIA_VIDEO

    def mostrar_info(self):
        """Devuelve información del préstamo digital con tipo y costo."""
        costo = self.calcular_costo()
        return f"Préstamo Digital -> {super().__str__()} | Tipo: {self.tipo_recurso} | Costo: ${costo:.2f}"

    def __str__(self):
        """Devuelve string con tipo, datos y costo calculado."""
        return self.mostrar_info()