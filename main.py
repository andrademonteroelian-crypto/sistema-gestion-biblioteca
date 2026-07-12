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
# Punto de entrada único del sistema. Crea las tablas necesarias (si no
# existen, contra SQL Server o SQLite de respaldo) y abre la ventana de
# Login, que es la puerta de entrada obligatoria antes de la ventana
# principal del Gestor de Biblioteca.
#
# Ejecutar siempre desde la raíz del proyecto:
#     python main.py

import sys

from PySide6.QtWidgets import QApplication

from Datos.usuario_biblioteca_dao import UsuarioBibliotecaDAO
from Datos.prestamo_dao import PrestamoDAO
from GUI.ventana_login import VentanaLogin


def main():
    # Crea las tablas necesarias una sola vez al arrancar (idempotente).
    UsuarioBibliotecaDAO.crear_tabla_si_no_existe()
    PrestamoDAO.crear_tabla_si_no_existe()

    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
