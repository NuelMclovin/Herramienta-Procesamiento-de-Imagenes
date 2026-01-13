"""
Diálogos base para selección de imágenes y parámetros.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QGroupBox, QRadioButton, QMessageBox, QSlider,
    QSpinBox, QDoubleSpinBox, QComboBox
)
from PySide6.QtCore import Qt
from config import (
    COLOR_FONDO, COLOR_OSCURO, COLOR_PRIMARIO, COLOR_TEXT_PRIMARY,
    COLOR_BORDER, COLOR_CARD, COLOR_EXITO, COLOR_ERROR, COLOR_ACENTO
)


class DialogoBase(QDialog):
    """Clase base para crear diálogos con estilo consistente."""
    
    def __init__(self, parent, titulo, ancho=500):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumWidth(ancho)
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_OSCURO}, stop:1 {COLOR_FONDO});
                border: 3px solid {COLOR_PRIMARIO};
                border-radius: 15px;
            }}
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 12px;
                font-weight: 500;
            }}
            QPushButton {{
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 8px;
                border: 2px solid {COLOR_BORDER};
            }}
            QPushButton:hover {{
                border: 2px solid {COLOR_PRIMARIO};
                background: {COLOR_PRIMARIO};
            }}
            QSpinBox, QDoubleSpinBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }}
            QComboBox {{
                background: {COLOR_CARD};
                color: {COLOR_TEXT_PRIMARY};
                border: 2px solid {COLOR_BORDER};
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }}
        """)
        
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setSpacing(15)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.ventana_principal = parent
        self.radio_resultado = None  # Inicializar como None
    
    def agregar_selector_imagen(self, incluir_resultado=False):
        """
        Agrega selector de imagen al diálogo.
        
        Args:
            incluir_resultado: Si True, incluye la opción "Resultado". 
                              Por defecto False (solo Imagen 1 e Imagen 2)
        """
        grupo_box = QGroupBox("Seleccionar imagen objetivo:")
        grupo_box.setStyleSheet(f"""
            QGroupBox {{
                color: {COLOR_TEXT_PRIMARY};
                font-weight: bold;
                font-size: 13px;
                border: 2px solid {COLOR_PRIMARIO};
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background: {COLOR_CARD};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                background: {COLOR_PRIMARIO};
                border-radius: 5px;
            }}
        """)
        
        grupo_layout = QVBoxLayout(grupo_box)
        
        self.radio_img1 = QRadioButton("Imagen 1 (Principal)")
        self.radio_img1.setChecked(True)
        self.radio_img1.setStyleSheet(f"""
            QRadioButton {{
                color: {COLOR_TEXT_PRIMARY}; 
                font-size: 12px;
                font-weight: 600;
                padding: 5px;
            }}
        """)
        
        self.radio_img2 = QRadioButton("Imagen 2 (Segunda)")
        self.radio_img2.setStyleSheet(f"""
            QRadioButton {{
                color: {COLOR_TEXT_PRIMARY}; 
                font-size: 12px;
                font-weight: 600;
                padding: 5px;
            }}
        """)
        
        grupo_layout.addWidget(self.radio_img1)
        grupo_layout.addWidget(self.radio_img2)
        
        # Solo agregar opción "Resultado" si se solicita explícitamente
        if incluir_resultado:
            self.radio_resultado = QRadioButton("Resultado")
            self.radio_resultado.setStyleSheet(f"""
                QRadioButton {{
                    color: {COLOR_TEXT_PRIMARY}; 
                    font-size: 12px;
                    font-weight: 600;
                    padding: 5px;
                }}
            """)
            grupo_layout.addWidget(self.radio_resultado)
        
        self.layout_principal.addWidget(grupo_box)
    
    def obtener_imagen_seleccionada(self):
        """Retorna la imagen seleccionada y un identificador."""
        if self.radio_img1.isChecked():
            if self.ventana_principal.imagen_actual is None:
                QMessageBox.warning(self, "Advertencia", "Imagen 1 no esta cargada")
                return None, None
            return self.ventana_principal.imagen_actual.copy(), 'img1'
        elif self.radio_img2.isChecked():
            if self.ventana_principal.imagen_segunda is None:
                QMessageBox.warning(self, "Advertencia", "Imagen 2 no esta cargada")
                return None, None
            return self.ventana_principal.imagen_segunda.copy(), 'img2'
        elif self.radio_resultado is not None and self.radio_resultado.isChecked():
            if self.ventana_principal.imagen_resultado is None:
                QMessageBox.warning(self, "Advertencia", "No hay imagen resultado")
                return None, None
            return self.ventana_principal.imagen_resultado.copy(), 'resultado'
        else:
            # Por defecto devolver None si no hay selección válida
            return None, None
    
    def actualizar_imagen_seleccionada(self, resultado):
        """Actualiza la imagen seleccionada con el resultado."""
        if self.radio_img1.isChecked():
            self.ventana_principal.guardar_en_historial()
            self.ventana_principal.imagen_actual = resultado.copy()
            self.ventana_principal.mostrar_imagen_1()
        elif self.radio_img2.isChecked():
            self.ventana_principal.imagen_segunda = resultado.copy()
            self.ventana_principal.mostrar_imagen_2()
        elif self.radio_resultado is not None and self.radio_resultado.isChecked():
            self.ventana_principal.imagen_resultado = resultado.copy()
            self.ventana_principal.mostrar_resultado()
    
    def agregar_spin(self, etiqueta, minimo, maximo, valor_inicial, paso=1, es_double=False):
        """Agrega un spinbox al diálogo."""
        layout_h = QHBoxLayout()
        label = QLabel(etiqueta)
        label.setMinimumWidth(150)
        
        if es_double:
            spin = QDoubleSpinBox()
            spin.setDecimals(2)
            spin.setSingleStep(paso)
        else:
            spin = QSpinBox()
            spin.setSingleStep(paso)
        
        spin.setMinimum(minimo)
        spin.setMaximum(maximo)
        spin.setValue(valor_inicial)
        spin.setMinimumWidth(100)
        
        layout_h.addWidget(label)
        layout_h.addWidget(spin)
        layout_h.addStretch()
        
        self.layout_principal.addLayout(layout_h)
        return spin
    
    def agregar_combo(self, etiqueta, opciones, seleccion_inicial=0):
        """Agrega un combobox al diálogo."""
        layout_h = QHBoxLayout()
        label = QLabel(etiqueta)
        label.setMinimumWidth(150)
        
        combo = QComboBox()
        combo.addItems(opciones)
        combo.setCurrentIndex(seleccion_inicial)
        combo.setMinimumWidth(100)
        
        layout_h.addWidget(label)
        layout_h.addWidget(combo)
        layout_h.addStretch()
        
        self.layout_principal.addLayout(layout_h)
        return combo
    
    def agregar_botones(self, callback_aceptar):
        """Agrega botones de Aceptar y Cancelar."""
        layout_botones = QHBoxLayout()
        
        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_EXITO}, stop:1 #2d8659);
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background: {COLOR_EXITO};
            }}
        """)
        btn_aceptar.clicked.connect(callback_aceptar)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_ERROR}, stop:1 #c94965);
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background: {COLOR_ERROR};
            }}
        """)
        btn_cancelar.clicked.connect(self.reject)
        
        layout_botones.addStretch()
        layout_botones.addWidget(btn_aceptar)
        layout_botones.addWidget(btn_cancelar)
        
        self.layout_principal.addLayout(layout_botones)
