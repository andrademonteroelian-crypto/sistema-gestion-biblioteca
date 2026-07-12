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
# Decide en tiempo de ejecución si el programa trabaja contra SQL Server
# (clase Conexion) o contra una base de datos SQLite local (archivo
# biblioteca.db junto al proyecto), para que la app NUNCA truene por falta
# de conexión: se intenta SQL Server una sola vez al arrancar; si falla, se
# usa SQLite automáticamente. El resto del programa (los DAO) no necesita
# saber cuál de las dos se está usando: solo pide "dame un cursor".

import os
import sqlite3

from Datos.conexion import Conexion

_DIRECTORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RUTA_SQLITE = os.path.join(_DIRECTORIO_BASE, "biblioteca.db")

_usando_sql_server = None
_conexion_sqlite = None


def _intentar_sql_server():
    """Intenta conectar a SQL Server. Devuelve True/False sin tronar el programa."""
    try:
        Conexion.obtener_conexion()
        return True
    except SystemExit:
        return False
    except Exception:
        return False


def usando_sql_server():
    global _usando_sql_server
    if _usando_sql_server is None:
        _usando_sql_server = _intentar_sql_server()
        if _usando_sql_server:
            print("[BD] Conectado a SQL Server (" + Conexion._SERVIDOR + ").")
        else:
            print("[BD] No se pudo conectar a SQL Server. Usando base de datos local (SQLite).")
    return _usando_sql_server


def obtener_cursor():
    if usando_sql_server():
        return Conexion.obtener_cursor()
    return _obtener_conexion_sqlite().cursor()


def confirmar_cambios():
    if usando_sql_server():
        Conexion.obtener_conexion().commit()
    else:
        _obtener_conexion_sqlite().commit()


def deshacer_cambios():
    if usando_sql_server():
        Conexion.obtener_conexion().rollback()
    else:
        _obtener_conexion_sqlite().rollback()


def marcador_parametro():
    """SQL Server (pyodbc) y SQLite usan el mismo marcador '?', así que las
    mismas consultas sirven para ambos motores sin cambiar nada."""
    return "?"


def _obtener_conexion_sqlite():
    global _conexion_sqlite
    if _conexion_sqlite is None:
        _conexion_sqlite = sqlite3.connect(_RUTA_SQLITE)
    return _conexion_sqlite
