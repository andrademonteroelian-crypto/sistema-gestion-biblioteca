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
# Clase que permite abrir la conexión a la base de datos y abrir el cursor.

import sys

import pyodbc as bd


class Conexion:
    """
    Clase que permite abrir conexión a la BBDD y abrir cursor.

    Usa autenticación de Windows (Trusted_Connection), ya que en esta
    laptop SQL Server está configurado así (usuario de Windows
    ELIANANDRADE\\SQLANDRADEELIANM). No hace falta usuario ni contraseña
    de SQL Server: Windows valida automáticamente con la sesión activa.
    """
    _SERVIDOR = r'ELIANANDRADE\SQLANDRADEELIANM'
    _BBDD = 'Biblioteca'
    _conexion = None
    _cursor = None

    @classmethod
    def _crear_bd_si_no_existe(cls):
        """
        Se conecta primero a 'master' (que siempre existe) y crea la base
        de datos 'Biblioteca' si todavía no existe, antes de conectarse
        a ella directamente.
        """
        conexion_master = bd.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
            cls._SERVIDOR + ';DATABASE=master;Trusted_Connection=yes;TrustServerCertificate=yes',
            timeout=3,
            autocommit=True,
        )
        cursor = conexion_master.cursor()
        cursor.execute(
            "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = ?) "
            "CREATE DATABASE " + cls._BBDD,
            (cls._BBDD,)
        )
        conexion_master.close()

    @classmethod
    def obtener_conexion(cls):
        if cls._conexion is None:
            try:
                cls._crear_bd_si_no_existe()
                cls._conexion = bd.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                    cls._SERVIDOR + ';DATABASE=' + cls._BBDD +
                    ';Trusted_Connection=yes;TrustServerCertificate=yes',
                    timeout=3,
                )
                return cls._conexion
            except Exception as e:
                print(e)
                sys.exit()
        else:
            return cls._conexion

    @classmethod
    def obtener_cursor(cls):
        if cls._cursor is None:
            try:
                cls._cursor = cls.obtener_conexion().cursor()
                return cls._cursor
            except Exception as e:
                print(e)
                sys.exit()
        else:
            return cls._cursor


if __name__ == '__main__':
    print(Conexion.obtener_conexion())
    print(Conexion.obtener_cursor())
