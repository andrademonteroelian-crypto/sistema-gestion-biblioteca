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
# Capa: GUI
# Ventana de Login/Registro. Es la puerta de entrada del sistema: valida
# credenciales contra la base de datos (vía Servicios) y, si el login es
# exitoso, abre la ventana principal del Gestor de Biblioteca.
# Esta capa SOLO arma widgets y llama a Servicios; nunca valida por sí sola
# ni ejecuta SQL directo.

from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from Servicios.servicio_usuario_biblioteca import ServicioUsuarioBiblioteca, ErrorValidacion


ESTILO_BTN_PRINCIPAL = (
    "QPushButton { background-color: #2c6fad; color: white; border-radius: 8px; "
    "padding: 12px; font-size: 13px; } "
    "QPushButton:hover { background-color: #1a4f80; }"
)
ESTILO_BTN_SECUNDARIO = (
    "QPushButton { background-color: #7f8c8d; color: white; border-radius: 8px; "
    "padding: 12px; font-size: 13px; } "
    "QPushButton:hover { background-color: #5d6d6e; }"
)
ESTILO_INPUT = (
    "QLineEdit { border: 1px solid #bdc3c7; border-radius: 6px; padding: 8px; "
    "font-size: 13px; } "
    "QLineEdit:focus { border: 2px solid #2c6fad; }"
)


class VentanaLogin(QMainWindow):
    """
    Ventana inicial del sistema: pestañas "Iniciar sesión" y "Registrarse".
    Al iniciar sesión con éxito, abre VentanaPrincipal y se cierra a sí misma.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Biblioteca — Acceso")
        self.setMinimumSize(460, 480)
        self.ventana_principal = None
        self._construir_ui()

    def _construir_ui(self):
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(30, 26, 30, 26)
        layout.setSpacing(14)

        lbl_titulo = QLabel("📚  Biblioteca")
        lbl_titulo.setFont(QFont("Arial", 20, QFont.Bold))
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        lbl_sub = QLabel("Sistema de Gestión de Servicios")
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setStyleSheet("color: gray;")
        layout.addWidget(lbl_sub)

        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        layout.addWidget(linea)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._crear_tab_login(), "Iniciar sesión")
        self.tabs.addTab(self._crear_tab_registro(), "Registrarse")
        layout.addWidget(self.tabs)

    # ---------------------------------------------------------
    # PESTAÑA: INICIAR SESIÓN
    # ---------------------------------------------------------
    def _crear_tab_login(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(10)

        self.login_correo = QLineEdit()
        self.login_correo.setPlaceholderText("correo@ejemplo.com")
        self.login_correo.setStyleSheet(ESTILO_INPUT)
        self.login_correo.setMinimumHeight(38)
        form.addRow("Correo *", self.login_correo)

        self.login_contrasena = QLineEdit()
        self.login_contrasena.setPlaceholderText("Contraseña")
        self.login_contrasena.setEchoMode(QLineEdit.Password)
        self.login_contrasena.setStyleSheet(ESTILO_INPUT)
        self.login_contrasena.setMinimumHeight(38)
        form.addRow("Contraseña *", self.login_contrasena)

        layout.addLayout(form)

        botones = QHBoxLayout()
        btn_limpiar = QPushButton("🧹  Limpiar")
        btn_limpiar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_limpiar.setMinimumHeight(40)
        btn_limpiar.clicked.connect(self._limpiar_login)

        btn_ingresar = QPushButton("✔  Iniciar sesión")
        btn_ingresar.setStyleSheet(ESTILO_BTN_PRINCIPAL)
        btn_ingresar.setMinimumHeight(40)
        btn_ingresar.clicked.connect(self._iniciar_sesion)

        botones.addWidget(btn_limpiar)
        botones.addWidget(btn_ingresar)
        layout.addLayout(botones)
        layout.addStretch()

        return tab

    def _limpiar_login(self):
        """Limpia únicamente los campos de la pestaña de login."""
        self.login_correo.clear()
        self.login_contrasena.clear()

    def _iniciar_sesion(self):
        correo = self.login_correo.text().strip()
        contrasena = self.login_contrasena.text()

        try:
            usuario = ServicioUsuarioBiblioteca.iniciar_sesion(correo, contrasena)
        except ErrorValidacion as e:
            QMessageBox.warning(self, "⚠ No se pudo iniciar sesión", str(e))
            return

        QMessageBox.information(self, "✔ Bienvenido", f"Bienvenido, {usuario.nombre}.")

        # Import diferido para evitar import circular entre GUI de login y principal.
        from GUI.ventana_principal import VentanaPrincipal
        self.ventana_principal = VentanaPrincipal(usuario)
        self.ventana_principal.show()
        self.close()

    # ---------------------------------------------------------
    # PESTAÑA: REGISTRARSE
    # ---------------------------------------------------------
    def _crear_tab_registro(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(12)

        form = QFormLayout()
        form.setSpacing(10)

        self.reg_nombre = QLineEdit()
        self.reg_nombre.setPlaceholderText("Ej: Juan Pérez")
        self.reg_nombre.setStyleSheet(ESTILO_INPUT)
        self.reg_nombre.setMinimumHeight(36)
        form.addRow("Nombre completo *", self.reg_nombre)

        self.reg_cedula = QLineEdit()
        self.reg_cedula.setPlaceholderText("10 dígitos numéricos")
        self.reg_cedula.setMaxLength(10)
        self.reg_cedula.setStyleSheet(ESTILO_INPUT)
        self.reg_cedula.setMinimumHeight(36)
        self.reg_cedula.textChanged.connect(self._solo_numeros_cedula)
        form.addRow("Cédula *", self.reg_cedula)

        self.reg_correo = QLineEdit()
        self.reg_correo.setPlaceholderText("correo@ejemplo.com")
        self.reg_correo.setStyleSheet(ESTILO_INPUT)
        self.reg_correo.setMinimumHeight(36)
        form.addRow("Correo electrónico *", self.reg_correo)

        self.reg_contrasena = QLineEdit()
        self.reg_contrasena.setPlaceholderText("Mínimo 6 caracteres, letra y número")
        self.reg_contrasena.setEchoMode(QLineEdit.Password)
        self.reg_contrasena.setStyleSheet(ESTILO_INPUT)
        self.reg_contrasena.setMinimumHeight(36)
        form.addRow("Contraseña *", self.reg_contrasena)

        self.reg_confirmar = QLineEdit()
        self.reg_confirmar.setPlaceholderText("Repita la contraseña")
        self.reg_confirmar.setEchoMode(QLineEdit.Password)
        self.reg_confirmar.setStyleSheet(ESTILO_INPUT)
        self.reg_confirmar.setMinimumHeight(36)
        form.addRow("Confirmar contraseña *", self.reg_confirmar)

        layout.addLayout(form)

        lbl_obligatorio = QLabel("* Todos los campos son obligatorios")
        lbl_obligatorio.setStyleSheet("color: #e74c3c; font-size: 11px;")
        layout.addWidget(lbl_obligatorio)

        botones = QHBoxLayout()
        btn_limpiar = QPushButton("🧹  Limpiar")
        btn_limpiar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_limpiar.setMinimumHeight(40)
        btn_limpiar.clicked.connect(self._limpiar_registro)

        btn_registrar = QPushButton("✔  Registrar")
        btn_registrar.setStyleSheet(ESTILO_BTN_PRINCIPAL)
        btn_registrar.setMinimumHeight(40)
        btn_registrar.clicked.connect(self._registrar)

        botones.addWidget(btn_limpiar)
        botones.addWidget(btn_registrar)
        layout.addLayout(botones)
        layout.addStretch()

        return tab

    def _solo_numeros_cedula(self, texto):
        solo_digitos = "".join(c for c in texto if c.isdigit())
        if solo_digitos != texto:
            self.reg_cedula.blockSignals(True)
            self.reg_cedula.setText(solo_digitos)
            self.reg_cedula.blockSignals(False)

    def _limpiar_registro(self):
        """Limpia únicamente los campos de la pestaña de registro."""
        self.reg_nombre.clear()
        self.reg_cedula.clear()
        self.reg_correo.clear()
        self.reg_contrasena.clear()
        self.reg_confirmar.clear()

    def _registrar(self):
        nombre = self.reg_nombre.text()
        cedula = self.reg_cedula.text()
        correo = self.reg_correo.text()
        contrasena = self.reg_contrasena.text()
        confirmar = self.reg_confirmar.text()

        try:
            ServicioUsuarioBiblioteca.registrar_usuario(nombre, cedula, correo, contrasena, confirmar)
        except ErrorValidacion as e:
            QMessageBox.warning(self, "⚠ Error de validación", str(e))
            return

        QMessageBox.information(self, "✔ Registro exitoso", "Usuario registrado correctamente. Ya puede iniciar sesión.")
        self._limpiar_registro()
        self.tabs.setCurrentIndex(0)
