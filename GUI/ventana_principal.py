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
# Ventana principal del Gestor de Biblioteca. Se abre solo después de un
# login exitoso. Contiene pestañas: Préstamos de libros, Préstamos
# digitales, Usuarios y Reportes — cada una con su propio CRUD real contra
# la base de datos. Esta capa SOLO arma widgets y llama a Servicios; nunca
# valida por sí sola ni ejecuta SQL directo.

from PySide6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QComboBox,
    QTextEdit
)
from PySide6.QtCore import Qt

from Servicios.prestamo_manager import PrestamoManager
from Servicios.servicio_usuario_biblioteca import ServicioUsuarioBiblioteca, ErrorValidacion
from Dominio.prestamo_libro import PrestamoLibro
from Dominio.prestamo_digital import PrestamoDigital
from Dominio.gestor_biblioteca import GestorBiblioteca


ESTILO_BTN_PRINCIPAL = (
    "QPushButton { background-color: #2c6fad; color: white; border-radius: 8px; "
    "padding: 10px; font-size: 13px; } "
    "QPushButton:hover { background-color: #1a4f80; }"
)
ESTILO_BTN_SECUNDARIO = (
    "QPushButton { background-color: #7f8c8d; color: white; border-radius: 8px; "
    "padding: 10px; font-size: 13px; } "
    "QPushButton:hover { background-color: #5d6d6e; }"
)
ESTILO_BTN_PELIGRO = (
    "QPushButton { background-color: #c0392b; color: white; border-radius: 8px; "
    "padding: 10px; font-size: 13px; } "
    "QPushButton:hover { background-color: #922b21; }"
)
ESTILO_INPUT = (
    "QLineEdit, QComboBox { border: 1px solid #bdc3c7; border-radius: 6px; padding: 8px; "
    "font-size: 13px; } "
    "QLineEdit:focus { border: 2px solid #2c6fad; }"
)


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal del sistema de Biblioteca: gestión de Usuarios,
    Préstamos de libros físicos, Préstamos digitales y Reportes.
    """

    def __init__(self, usuario_sesion):
        super().__init__()
        self.usuario_sesion = usuario_sesion
        self.setWindowTitle("Sistema de Gestión de Biblioteca")
        self.setMinimumSize(760, 560)

        # Estado de "modo edición": None = creando, código = editando ese registro.
        self._editando_codigo_libro = None
        self._editando_codigo_digital = None
        self._editando_cedula_usuario = None

        self._construir_ui()
        self._refrescar_todo()

    def _construir_ui(self):
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout = QVBoxLayout(contenedor)

        lbl_bienvenida = QLabel(f"📚  Biblioteca — Sesión iniciada como {self.usuario_sesion.nombre}")
        lbl_bienvenida.setStyleSheet("font-size: 14px; font-weight: bold; padding: 6px;")
        layout.addWidget(lbl_bienvenida)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._crear_tab_prestamo_libro(), "📖  Préstamos de libros")
        self.tabs.addTab(self._crear_tab_prestamo_digital(), "💻  Préstamos digitales")
        self.tabs.addTab(self._crear_tab_usuarios(), "👤  Usuarios")
        self.tabs.addTab(self._crear_tab_reportes(), "📊  Reportes")
        layout.addWidget(self.tabs)

    def _refrescar_todo(self):
        self._refrescar_lista_libros()
        self._refrescar_lista_digitales()
        self._refrescar_lista_usuarios()
        self._refrescar_combos_usuarios()

    # ===========================================================
    # PESTAÑA: PRÉSTAMOS DE LIBROS
    # ===========================================================
    def _crear_tab_prestamo_libro(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        form = QFormLayout()
        form.setSpacing(8)

        self.lib_codigo = QLineEdit()
        self.lib_codigo.setStyleSheet(ESTILO_INPUT)
        form.addRow("Código *", self.lib_codigo)

        self.lib_titulo = QLineEdit()
        self.lib_titulo.setStyleSheet(ESTILO_INPUT)
        form.addRow("Título *", self.lib_titulo)

        self.lib_fecha = QLineEdit()
        self.lib_fecha.setPlaceholderText("AAAA-MM-DD")
        self.lib_fecha.setStyleSheet(ESTILO_INPUT)
        form.addRow("Fecha de préstamo *", self.lib_fecha)

        self.lib_dias = QLineEdit()
        self.lib_dias.setPlaceholderText("Ej: 7")
        self.lib_dias.setStyleSheet(ESTILO_INPUT)
        form.addRow("Días de préstamo *", self.lib_dias)

        self.lib_atraso = QLineEdit()
        self.lib_atraso.setPlaceholderText("0 si no hay atraso")
        self.lib_atraso.setStyleSheet(ESTILO_INPUT)
        form.addRow("Días de atraso", self.lib_atraso)

        self.lib_usuario = QComboBox()
        self.lib_usuario.setStyleSheet(ESTILO_INPUT)
        form.addRow("Usuario que solicita *", self.lib_usuario)

        layout.addLayout(form)

        botones_form = QHBoxLayout()
        self.lib_btn_guardar = QPushButton("✔  Registrar préstamo")
        self.lib_btn_guardar.setStyleSheet(ESTILO_BTN_PRINCIPAL)
        self.lib_btn_guardar.clicked.connect(self._guardar_prestamo_libro)

        btn_cancelar_edicion = QPushButton("✖  Cancelar edición")
        btn_cancelar_edicion.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_cancelar_edicion.clicked.connect(self._cancelar_edicion_libro)

        btn_limpiar = QPushButton("🧹  Limpiar")
        btn_limpiar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_limpiar.clicked.connect(self._limpiar_form_libro)

        botones_form.addWidget(self.lib_btn_guardar)
        botones_form.addWidget(btn_cancelar_edicion)
        botones_form.addWidget(btn_limpiar)
        layout.addLayout(botones_form)

        layout.addWidget(QLabel("Préstamos de libros registrados:"))
        self.lib_buscar = QLineEdit()
        self.lib_buscar.setPlaceholderText("🔎 Buscar por código, título o cédula...")
        self.lib_buscar.setStyleSheet(ESTILO_INPUT)
        self.lib_buscar.textChanged.connect(self._filtrar_lista_libros)
        layout.addWidget(self.lib_buscar)

        self.lib_lista = QListWidget()
        layout.addWidget(self.lib_lista)

        botones_lista = QHBoxLayout()
        btn_editar = QPushButton("✏  Editar seleccionado")
        btn_editar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_editar.clicked.connect(self._editar_prestamo_libro_seleccionado)

        btn_eliminar = QPushButton("🗑  Eliminar seleccionado")
        btn_eliminar.setStyleSheet(ESTILO_BTN_PELIGRO)
        btn_eliminar.clicked.connect(self._eliminar_prestamo_libro_seleccionado)

        botones_lista.addWidget(btn_editar)
        botones_lista.addWidget(btn_eliminar)
        layout.addLayout(botones_lista)

        return tab

    def _limpiar_form_libro(self):
        self.lib_codigo.clear()
        self.lib_titulo.clear()
        self.lib_fecha.clear()
        self.lib_dias.clear()
        self.lib_atraso.clear()
        if self.lib_usuario.count() > 0:
            self.lib_usuario.setCurrentIndex(0)

    def _cancelar_edicion_libro(self):
        self._editando_codigo_libro = None
        self.lib_codigo.setEnabled(True)
        self.lib_btn_guardar.setText("✔  Registrar préstamo")
        self._limpiar_form_libro()

    def _guardar_prestamo_libro(self):
        codigo = self.lib_codigo.text()
        titulo = self.lib_titulo.text()
        fecha = self.lib_fecha.text()
        dias = self.lib_dias.text()
        atraso = self.lib_atraso.text() or "0"
        cedula_usuario = self.lib_usuario.currentData()

        try:
            if self._editando_codigo_libro is None:
                PrestamoManager.crear_prestamo_libro(codigo, titulo, fecha, dias, atraso, cedula_usuario)
                QMessageBox.information(self, "✔ Éxito", "Préstamo de libro registrado correctamente.")
            else:
                PrestamoManager.actualizar_prestamo_libro(
                    self._editando_codigo_libro, codigo, titulo, fecha, dias, atraso, cedula_usuario
                )
                QMessageBox.information(self, "✔ Éxito", "Préstamo de libro actualizado correctamente.")
        except ErrorValidacion as e:
            QMessageBox.warning(self, "⚠ Error de validación", str(e))
            return

        self._cancelar_edicion_libro()
        self._refrescar_lista_libros()

    def _refrescar_lista_libros(self):
        self.lib_lista.clear()
        for p in PrestamoManager.obtener_prestamos():
            if isinstance(p, PrestamoLibro):
                self.lib_lista.addItem(p.mostrar_info() + f" | Usuario: {p.cedula_usuario}")
        # Vuelve a aplicar el filtro de búsqueda activo (si lo hay) sobre los
        # datos recién cargados desde el DAO.
        self._filtrar_lista_libros(self.lib_buscar.text())

    def _filtrar_lista_libros(self, texto):
        """Filtra visualmente la lista de préstamos de libros ya cargada,
        por coincidencia (case-insensitive) contra código, título, fecha o
        cédula del usuario. No modifica ni vuelve a consultar la BD."""
        texto = texto.strip().lower()
        for i in range(self.lib_lista.count()):
            item = self.lib_lista.item(i)
            item.setHidden(bool(texto) and texto not in item.text().lower())

    def _editar_prestamo_libro_seleccionado(self):
        item = self.lib_lista.currentItem()
        if item is None:
            QMessageBox.warning(self, "⚠ Atención", "Seleccione un préstamo de la lista primero.")
            return
        codigo = item.text().split("Código:")[1].split("|")[0].strip()
        prestamo = next((p for p in PrestamoManager.obtener_prestamos()
                          if isinstance(p, PrestamoLibro) and p.codigo == codigo), None)
        if prestamo is None:
            return

        self._editando_codigo_libro = prestamo.codigo
        self.lib_codigo.setText(prestamo.codigo)
        self.lib_titulo.setText(prestamo.titulo_recurso)
        self.lib_fecha.setText(str(prestamo.fecha_prestamo))
        self.lib_dias.setText(str(prestamo.dias_prestamo))
        self.lib_atraso.setText(str(prestamo.dias_atraso))
        idx = self.lib_usuario.findData(prestamo.cedula_usuario)
        if idx >= 0:
            self.lib_usuario.setCurrentIndex(idx)
        self.lib_btn_guardar.setText("💾  Guardar cambios")

    def _eliminar_prestamo_libro_seleccionado(self):
        item = self.lib_lista.currentItem()
        if item is None:
            QMessageBox.warning(self, "⚠ Atención", "Seleccione un préstamo de la lista primero.")
            return
        codigo = item.text().split("Código:")[1].split("|")[0].strip()

        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Seguro que desea eliminar el préstamo con código {codigo}?"
        )
        if respuesta != QMessageBox.Yes:
            return

        try:
            PrestamoManager.eliminar_prestamo(codigo)
        except ErrorValidacion as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        QMessageBox.information(self, "✔ Eliminado", "El préstamo fue eliminado correctamente.")
        self._refrescar_lista_libros()

    # ===========================================================
    # PESTAÑA: PRÉSTAMOS DIGITALES
    # ===========================================================
    def _crear_tab_prestamo_digital(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        form = QFormLayout()
        form.setSpacing(8)

        self.dig_codigo = QLineEdit()
        self.dig_codigo.setStyleSheet(ESTILO_INPUT)
        form.addRow("Código *", self.dig_codigo)

        self.dig_titulo = QLineEdit()
        self.dig_titulo.setStyleSheet(ESTILO_INPUT)
        form.addRow("Título *", self.dig_titulo)

        self.dig_fecha = QLineEdit()
        self.dig_fecha.setPlaceholderText("AAAA-MM-DD")
        self.dig_fecha.setStyleSheet(ESTILO_INPUT)
        form.addRow("Fecha de préstamo *", self.dig_fecha)

        self.dig_dias = QLineEdit()
        self.dig_dias.setPlaceholderText("Ej: 5")
        self.dig_dias.setStyleSheet(ESTILO_INPUT)
        form.addRow("Días de préstamo *", self.dig_dias)

        self.dig_tipo_recurso = QComboBox()
        self.dig_tipo_recurso.addItems(["ebook", "video"])
        self.dig_tipo_recurso.setStyleSheet(ESTILO_INPUT)
        form.addRow("Tipo de recurso *", self.dig_tipo_recurso)

        self.dig_usuario = QComboBox()
        self.dig_usuario.setStyleSheet(ESTILO_INPUT)
        form.addRow("Usuario que solicita *", self.dig_usuario)

        layout.addLayout(form)

        botones_form = QHBoxLayout()
        self.dig_btn_guardar = QPushButton("✔  Registrar préstamo")
        self.dig_btn_guardar.setStyleSheet(ESTILO_BTN_PRINCIPAL)
        self.dig_btn_guardar.clicked.connect(self._guardar_prestamo_digital)

        btn_cancelar_edicion = QPushButton("✖  Cancelar edición")
        btn_cancelar_edicion.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_cancelar_edicion.clicked.connect(self._cancelar_edicion_digital)

        btn_limpiar = QPushButton("🧹  Limpiar")
        btn_limpiar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_limpiar.clicked.connect(self._limpiar_form_digital)

        botones_form.addWidget(self.dig_btn_guardar)
        botones_form.addWidget(btn_cancelar_edicion)
        botones_form.addWidget(btn_limpiar)
        layout.addLayout(botones_form)

        layout.addWidget(QLabel("Préstamos digitales registrados:"))
        self.dig_buscar = QLineEdit()
        self.dig_buscar.setPlaceholderText("🔎 Buscar por código, título o cédula...")
        self.dig_buscar.setStyleSheet(ESTILO_INPUT)
        self.dig_buscar.textChanged.connect(self._filtrar_lista_digitales)
        layout.addWidget(self.dig_buscar)

        self.dig_lista = QListWidget()
        layout.addWidget(self.dig_lista)

        botones_lista = QHBoxLayout()
        btn_editar = QPushButton("✏  Editar seleccionado")
        btn_editar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_editar.clicked.connect(self._editar_prestamo_digital_seleccionado)

        btn_eliminar = QPushButton("🗑  Eliminar seleccionado")
        btn_eliminar.setStyleSheet(ESTILO_BTN_PELIGRO)
        btn_eliminar.clicked.connect(self._eliminar_prestamo_digital_seleccionado)

        botones_lista.addWidget(btn_editar)
        botones_lista.addWidget(btn_eliminar)
        layout.addLayout(botones_lista)

        return tab

    def _limpiar_form_digital(self):
        self.dig_codigo.clear()
        self.dig_titulo.clear()
        self.dig_fecha.clear()
        self.dig_dias.clear()
        self.dig_tipo_recurso.setCurrentIndex(0)
        if self.dig_usuario.count() > 0:
            self.dig_usuario.setCurrentIndex(0)

    def _cancelar_edicion_digital(self):
        self._editando_codigo_digital = None
        self.dig_codigo.setEnabled(True)
        self.dig_btn_guardar.setText("✔  Registrar préstamo")
        self._limpiar_form_digital()

    def _guardar_prestamo_digital(self):
        codigo = self.dig_codigo.text()
        titulo = self.dig_titulo.text()
        fecha = self.dig_fecha.text()
        dias = self.dig_dias.text()
        tipo_recurso = self.dig_tipo_recurso.currentText()
        cedula_usuario = self.dig_usuario.currentData()

        try:
            if self._editando_codigo_digital is None:
                PrestamoManager.crear_prestamo_digital(codigo, titulo, fecha, dias, tipo_recurso, cedula_usuario)
                QMessageBox.information(self, "✔ Éxito", "Préstamo digital registrado correctamente.")
            else:
                PrestamoManager.actualizar_prestamo_digital(
                    self._editando_codigo_digital, codigo, titulo, fecha, dias, tipo_recurso, cedula_usuario
                )
                QMessageBox.information(self, "✔ Éxito", "Préstamo digital actualizado correctamente.")
        except ErrorValidacion as e:
            QMessageBox.warning(self, "⚠ Error de validación", str(e))
            return

        self._cancelar_edicion_digital()
        self._refrescar_lista_digitales()

    def _refrescar_lista_digitales(self):
        self.dig_lista.clear()
        for p in PrestamoManager.obtener_prestamos():
            if isinstance(p, PrestamoDigital):
                self.dig_lista.addItem(p.mostrar_info() + f" | Usuario: {p.cedula_usuario}")
        # Vuelve a aplicar el filtro de búsqueda activo (si lo hay) sobre los
        # datos recién cargados desde el DAO.
        self._filtrar_lista_digitales(self.dig_buscar.text())

    def _filtrar_lista_digitales(self, texto):
        """Filtra visualmente la lista de préstamos digitales ya cargada,
        por coincidencia (case-insensitive) contra código, título, fecha o
        cédula del usuario. No modifica ni vuelve a consultar la BD."""
        texto = texto.strip().lower()
        for i in range(self.dig_lista.count()):
            item = self.dig_lista.item(i)
            item.setHidden(bool(texto) and texto not in item.text().lower())

    def _editar_prestamo_digital_seleccionado(self):
        item = self.dig_lista.currentItem()
        if item is None:
            QMessageBox.warning(self, "⚠ Atención", "Seleccione un préstamo de la lista primero.")
            return
        codigo = item.text().split("Código:")[1].split("|")[0].strip()
        prestamo = next((p for p in PrestamoManager.obtener_prestamos()
                          if isinstance(p, PrestamoDigital) and p.codigo == codigo), None)
        if prestamo is None:
            return

        self._editando_codigo_digital = prestamo.codigo
        self.dig_codigo.setText(prestamo.codigo)
        self.dig_titulo.setText(prestamo.titulo_recurso)
        self.dig_fecha.setText(str(prestamo.fecha_prestamo))
        self.dig_dias.setText(str(prestamo.dias_prestamo))
        idx_tipo = self.dig_tipo_recurso.findText(prestamo.tipo_recurso)
        if idx_tipo >= 0:
            self.dig_tipo_recurso.setCurrentIndex(idx_tipo)
        idx_usr = self.dig_usuario.findData(prestamo.cedula_usuario)
        if idx_usr >= 0:
            self.dig_usuario.setCurrentIndex(idx_usr)
        self.dig_btn_guardar.setText("💾  Guardar cambios")

    def _eliminar_prestamo_digital_seleccionado(self):
        item = self.dig_lista.currentItem()
        if item is None:
            QMessageBox.warning(self, "⚠ Atención", "Seleccione un préstamo de la lista primero.")
            return
        codigo = item.text().split("Código:")[1].split("|")[0].strip()

        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Seguro que desea eliminar el préstamo con código {codigo}?"
        )
        if respuesta != QMessageBox.Yes:
            return

        try:
            PrestamoManager.eliminar_prestamo(codigo)
        except ErrorValidacion as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        QMessageBox.information(self, "✔ Eliminado", "El préstamo fue eliminado correctamente.")
        self._refrescar_lista_digitales()

    # ===========================================================
    # PESTAÑA: USUARIOS
    # ===========================================================
    def _crear_tab_usuarios(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        form = QFormLayout()
        form.setSpacing(8)

        self.usr_nombre = QLineEdit()
        self.usr_nombre.setStyleSheet(ESTILO_INPUT)
        form.addRow("Nombre *", self.usr_nombre)

        self.usr_cedula = QLineEdit()
        self.usr_cedula.setMaxLength(10)
        self.usr_cedula.setStyleSheet(ESTILO_INPUT)
        form.addRow("Cédula *", self.usr_cedula)

        self.usr_correo = QLineEdit()
        self.usr_correo.setStyleSheet(ESTILO_INPUT)
        form.addRow("Correo *", self.usr_correo)

        self.usr_contrasena = QLineEdit()
        self.usr_contrasena.setEchoMode(QLineEdit.Password)
        self.usr_contrasena.setStyleSheet(ESTILO_INPUT)
        form.addRow("Contraseña *", self.usr_contrasena)

        self.usr_confirmar = QLineEdit()
        self.usr_confirmar.setEchoMode(QLineEdit.Password)
        self.usr_confirmar.setStyleSheet(ESTILO_INPUT)
        form.addRow("Confirmar contraseña *", self.usr_confirmar)

        layout.addLayout(form)

        botones_form = QHBoxLayout()
        self.usr_btn_guardar = QPushButton("💾  Guardar cambios")
        self.usr_btn_guardar.setStyleSheet(ESTILO_BTN_PRINCIPAL)
        self.usr_btn_guardar.clicked.connect(self._guardar_usuario_editado)

        btn_cancelar = QPushButton("✖  Cancelar edición")
        btn_cancelar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_cancelar.clicked.connect(self._cancelar_edicion_usuario)

        btn_limpiar = QPushButton("🧹  Limpiar")
        btn_limpiar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_limpiar.clicked.connect(self._limpiar_form_usuario)

        botones_form.addWidget(self.usr_btn_guardar)
        botones_form.addWidget(btn_cancelar)
        botones_form.addWidget(btn_limpiar)
        layout.addLayout(botones_form)

        layout.addWidget(QLabel("Usuarios registrados (el registro nuevo se hace desde la pantalla de acceso):"))
        self.usr_buscar = QLineEdit()
        self.usr_buscar.setPlaceholderText("🔎 Buscar por nombre, cédula o correo...")
        self.usr_buscar.setStyleSheet(ESTILO_INPUT)
        self.usr_buscar.textChanged.connect(self._filtrar_lista_usuarios)
        layout.addWidget(self.usr_buscar)

        self.usr_lista = QListWidget()
        layout.addWidget(self.usr_lista)

        botones_lista = QHBoxLayout()
        btn_editar = QPushButton("✏  Editar seleccionado")
        btn_editar.setStyleSheet(ESTILO_BTN_SECUNDARIO)
        btn_editar.clicked.connect(self._editar_usuario_seleccionado)

        btn_eliminar = QPushButton("🗑  Eliminar seleccionado")
        btn_eliminar.setStyleSheet(ESTILO_BTN_PELIGRO)
        btn_eliminar.clicked.connect(self._eliminar_usuario_seleccionado)

        botones_lista.addWidget(btn_editar)
        botones_lista.addWidget(btn_eliminar)
        layout.addLayout(botones_lista)

        return tab

    def _limpiar_form_usuario(self):
        self.usr_nombre.clear()
        self.usr_cedula.clear()
        self.usr_correo.clear()
        self.usr_contrasena.clear()
        self.usr_confirmar.clear()

    def _cancelar_edicion_usuario(self):
        self._editando_cedula_usuario = None
        self.usr_cedula.setEnabled(True)
        self._limpiar_form_usuario()

    def _guardar_usuario_editado(self):
        if self._editando_cedula_usuario is None:
            QMessageBox.information(
                self, "Sin cambios pendientes",
                "Seleccione un usuario de la lista y presione 'Editar seleccionado' para modificarlo.\n"
                "Los usuarios nuevos se registran desde la pantalla de acceso."
            )
            return

        try:
            ServicioUsuarioBiblioteca.actualizar_usuario(
                self._editando_cedula_usuario,
                self.usr_nombre.text(), self.usr_cedula.text(),
                self.usr_correo.text(), self.usr_contrasena.text(), self.usr_confirmar.text()
            )
        except ErrorValidacion as e:
            QMessageBox.warning(self, "⚠ Error de validación", str(e))
            return

        QMessageBox.information(self, "✔ Éxito", "Usuario actualizado correctamente.")
        self._cancelar_edicion_usuario()
        self._refrescar_lista_usuarios()
        self._refrescar_combos_usuarios()

    def _refrescar_lista_usuarios(self):
        self.usr_lista.clear()
        for u in ServicioUsuarioBiblioteca.obtener_usuarios():
            self.usr_lista.addItem(str(u))
        # Vuelve a aplicar el filtro de búsqueda activo (si lo hay) sobre los
        # datos recién cargados desde el DAO.
        self._filtrar_lista_usuarios(self.usr_buscar.text())

    def _filtrar_lista_usuarios(self, texto):
        """Filtra visualmente la lista de usuarios ya cargada, por
        coincidencia (case-insensitive) contra nombre, cédula, email o ID.
        No modifica ni vuelve a consultar la BD."""
        texto = texto.strip().lower()
        for i in range(self.usr_lista.count()):
            item = self.usr_lista.item(i)
            item.setHidden(bool(texto) and texto not in item.text().lower())

    def _refrescar_combos_usuarios(self):
        usuarios = ServicioUsuarioBiblioteca.obtener_usuarios()
        for combo in (self.lib_usuario, self.dig_usuario):
            actual = combo.currentData()
            combo.clear()
            for u in usuarios:
                combo.addItem(f"{u.nombre} ({u.cedula})", u.cedula)
            if actual is not None:
                idx = combo.findData(actual)
                if idx >= 0:
                    combo.setCurrentIndex(idx)

    def _editar_usuario_seleccionado(self):
        item = self.usr_lista.currentItem()
        if item is None:
            QMessageBox.warning(self, "⚠ Atención", "Seleccione un usuario de la lista primero.")
            return
        cedula = item.text().split("Cédula:")[1].strip()
        usuario = next((u for u in ServicioUsuarioBiblioteca.obtener_usuarios() if u.cedula == cedula), None)
        if usuario is None:
            return

        self._editando_cedula_usuario = usuario.cedula
        self.usr_nombre.setText(usuario.nombre)
        self.usr_cedula.setText(usuario.cedula)
        self.usr_correo.setText(usuario.email)
        self.usr_contrasena.setText(usuario.contrasena)
        self.usr_confirmar.setText(usuario.contrasena)

    def _eliminar_usuario_seleccionado(self):
        item = self.usr_lista.currentItem()
        if item is None:
            QMessageBox.warning(self, "⚠ Atención", "Seleccione un usuario de la lista primero.")
            return
        cedula = item.text().split("Cédula:")[1].strip()

        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Seguro que desea eliminar al usuario con cédula {cedula}?"
        )
        if respuesta != QMessageBox.Yes:
            return

        try:
            ServicioUsuarioBiblioteca.eliminar_usuario(cedula)
        except ErrorValidacion as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        QMessageBox.information(self, "✔ Eliminado", "El usuario fue eliminado correctamente.")
        self._refrescar_lista_usuarios()
        self._refrescar_combos_usuarios()

    # ===========================================================
    # PESTAÑA: REPORTES
    # ===========================================================
    def _crear_tab_reportes(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        btn_generar = QPushButton("📊  Generar reporte")
        btn_generar.setStyleSheet(ESTILO_BTN_PRINCIPAL)
        btn_generar.clicked.connect(self._generar_reporte)
        layout.addWidget(btn_generar)

        self.reporte_texto = QTextEdit()
        self.reporte_texto.setReadOnly(True)
        layout.addWidget(self.reporte_texto)

        return tab

    def _generar_reporte(self):
        """
        Usa GestorBiblioteca (con su polimorfismo calcular_costo()/mostrar_info())
        alimentado con lo que hay REALMENTE en la base de datos.
        """
        gestor = GestorBiblioteca("Biblioteca Central")
        for p in PrestamoManager.obtener_prestamos():
            gestor.agregar_servicio(p)

        lineas = [f"--- REPORTE: {gestor.nombre_biblioteca} ---", ""]
        for servicio in gestor.servicios:
            lineas.append(servicio.mostrar_info())
        lineas.append("")
        lineas.append(f"Costo total acumulado: ${gestor.calcular_costo_total():.2f}")
        lineas.append(f"Cantidad de préstamos: {len(gestor.servicios)}")

        self.reporte_texto.setPlainText("\n".join(lineas))
