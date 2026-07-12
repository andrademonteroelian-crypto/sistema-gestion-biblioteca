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
class GestorBiblioteca:
    """
    Clase adicional que gestiona los servicios de la biblioteca.
    Contiene los 2 métodos polimórficos.
    """

    def __init__(self, nombre_biblioteca):
        """Crea el gestor con lista vacía de servicios."""
        self._nombre_biblioteca = nombre_biblioteca  # Guarda el nombre de la biblioteca
        self._servicios = []                          # Crea lista vacía para guardar préstamos

    @property
    def nombre_biblioteca(self):
        """Devuelve el nombre de la biblioteca."""
        return self._nombre_biblioteca

    @nombre_biblioteca.setter
    def nombre_biblioteca(self, valor):
        """Valida que el nombre no esté vacío."""
        if valor == "":
            raise ValueError("El nombre no puede estar vacío")
        self._nombre_biblioteca = valor

    @property
    def servicios(self):
        """Devuelve la lista de servicios guardados."""
        return self._servicios

    def agregar_servicio(self, servicio):
        """Recibe un objeto y lo guarda en la lista."""
        self._servicios.append(servicio)

    def calcular_costo_total(self):
        """
        Método polimórfico 1: recorre lista y suma costos de cada servicio.
        Demuestra polimorfismo: no pregunta el tipo, solo llama calcular_costo().
        """
        total = 0  # Variable para acumular la suma
        for servicio in self.servicios:  # Recorre cada servicio de la lista
            total += servicio.calcular_costo()  # Suma el costo del servicio actual
        return total  # Devuelve el total acumulado

    def generar_reporte(self):
        """
        Método polimórfico 2: recorre lista y muestra info de cada servicio.
        Demuestra polimorfismo: no pregunta el tipo, solo llama mostrar_info().
        """
        print(f"\n--- REPORTE: {self.nombre_biblioteca} ---")
        for servicio in self.servicios:  # Recorre cada servicio de la lista
            print(servicio.mostrar_info())  # Muestra la info del servicio actual
        print("--- FIN ---")

    def __str__(self):
        """Devuelve string con nombre y cantidad de servicios."""
        return f"Gestor: {self.nombre_biblioteca} | Servicios: {len(self.servicios)}"