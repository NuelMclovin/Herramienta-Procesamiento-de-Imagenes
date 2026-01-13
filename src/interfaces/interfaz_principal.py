"""
Interfaz principal del sistema de procesamiento de imágenes.
Diseño con panel lateral izquierdo y 3 paneles de imagen (Imagen 1, Imagen 2, Resultado).
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
import cv2
import numpy as np

from config import *

# Importar secciones modulares organizadas
from src.interfaces.seccion_archivo import SeccionArchivo
from src.interfaces.seccion_utilidades import SeccionUtilidades
from src.interfaces.seccion_aritmeticas import SeccionAritmeticas
from src.interfaces.seccion_logicas import SeccionLogicas
from src.interfaces.seccion_ajuste_brillo import SeccionAjusteBrillo
from src.interfaces.seccion_segmentacion import SeccionSegmentacion
from src.interfaces.seccion_morfologia import SeccionMorfologia
from src.interfaces.seccion_filtros import SeccionFiltros
from src.interfaces.seccion_ruido import SeccionRuido
from src.interfaces.seccion_fourier import SeccionFourier
from src.interfaces.seccion_modos_color import SeccionModosColor
from src.interfaces.seccion_componentes_conexas import SeccionComponentesConexas
from src.interfaces.histograma_widget import PanelImagenConHistograma


class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación con panel lateral y 3 áreas de imagen."""
    
    def __init__(self):
        super().__init__()
        # Variables de estado
        self.imagen_actual = None  # Imagen 1 (principal)
        self.imagen_original_backup = None  # Backup de Imagen 1
        self.imagen_segunda = None  # Imagen 2
        self.imagen_segunda_backup = None  # Backup de Imagen 2
        self.imagen_resultado = None  # Resultado de operaciones
        
        # Modos de color de cada imagen (RGB, HSV, CMY, GRAY)
        self.modo_color_img1 = 'RGB'
        self.modo_color_img2 = 'RGB'
        self.modo_color_resultado = 'RGB'
        
        # Historiales para deshacer/rehacer
        self.historial_img1 = []
        self.historial_rehacer_img1 = []
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializar la interfaz gráfica con panel lateral izquierdo y 3 imágenes."""
        self.setWindowTitle("Procesamiento de Imágenes - PDI Completo")
        self.setGeometry(50, 50, 1600, 900)
        self.setMinimumSize(1200, 700)  # Tamaño mínimo para responsividad
        self.setStyleSheet(f"background-color: {COLOR_FONDO};")
        
        # Widget central y layout principal (HORIZONTAL)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setStretch(0, 0)  # Panel lateral no se estira
        main_layout.setStretch(1, 1)  # Área principal se estira
        
        # PANEL LATERAL IZQUIERDO (HERRAMIENTAS)
        panel_lateral = QWidget()
        panel_lateral.setFixedWidth(200)
        panel_lateral.setMinimumWidth(180)
        panel_lateral.setMaximumWidth(220)
        panel_lateral.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_CARD}, stop:0.5 {COLOR_OSCURO}, stop:1 {COLOR_CARD});
                border-right: 4px solid;
                border-image: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:0.5 {COLOR_ACENTO}, stop:1 {COLOR_SECUNDARIO}) 1;
            }}
        """)
        
        # Scroll vertical para el panel lateral
        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        panel_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        panel_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: {COLOR_OSCURO};
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 6px;
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_ACENTO}, stop:1 {COLOR_SECUNDARIO});
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        panel_widget = QWidget()
        panel_layout = QVBoxLayout(panel_widget)
        panel_layout.setSpacing(8)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        
        # Título del panel
        titulo_panel = QLabel("HERRAMIENTAS")
        titulo_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_panel.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 10px;
                border: 2px solid {COLOR_TEXT_PRIMARY};
                margin-bottom: 8px;
            }}
        """)
        panel_layout.addWidget(titulo_panel)
        
        # Crear secciones modulares organizadas por categorías
        # 1. Gestión de Archivos e Imágenes
        panel_layout.addWidget(SeccionArchivo(self))
        panel_layout.addWidget(self._crear_separador())
        panel_layout.addWidget(SeccionUtilidades(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 2. Operaciones Básicas
        panel_layout.addWidget(SeccionAritmeticas(self))
        panel_layout.addWidget(self._crear_separador())
        panel_layout.addWidget(SeccionLogicas(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 3. Ajustes y Mejoras
        panel_layout.addWidget(SeccionAjusteBrillo(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 4. Segmentación
        panel_layout.addWidget(SeccionSegmentacion(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 5. Procesamiento Espacial
        panel_layout.addWidget(SeccionFiltros(self))
        panel_layout.addWidget(self._crear_separador())
        panel_layout.addWidget(SeccionRuido(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 6. Morfología Matemática
        panel_layout.addWidget(SeccionMorfologia(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 7. Transformadas (Frecuencia)
        panel_layout.addWidget(SeccionFourier(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 8. Análisis de Color
        panel_layout.addWidget(SeccionModosColor(self))
        panel_layout.addWidget(self._crear_separador())
        
        # 9. Componentes Conexas
        panel_layout.addWidget(SeccionComponentesConexas(self))
        
        panel_layout.addStretch()
        
        panel_scroll.setWidget(panel_widget)
        
        panel_lateral_layout = QVBoxLayout(panel_lateral)
        panel_lateral_layout.setContentsMargins(0, 0, 0, 0)
        panel_lateral_layout.addWidget(panel_scroll)
        
        main_layout.addWidget(panel_lateral)
        
        # AREA PRINCIPAL (DERECHA) - 3 PANELES DE IMAGEN
        area_principal = QWidget()
        area_layout = QVBoxLayout(area_principal)
        area_layout.setSpacing(0)
        area_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area para las imágenes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: {COLOR_FONDO};
                border: none;
            }}
            QScrollBar:vertical, QScrollBar:horizontal {{
                background: {COLOR_OSCURO};
                width: 14px;
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_PRIMARIO}, stop:1 {COLOR_ACENTO});
                border-radius: 7px;
                min-height: 30px;
                min-width: 30px;
            }}
            QScrollBar::handle:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLOR_ACENTO}, stop:1 {COLOR_EXITO});
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                height: 0px;
                width: 0px;
            }}
        """)
        
        area_imagenes = QWidget()
        imagenes_layout = QHBoxLayout(area_imagenes)
        imagenes_layout.setSpacing(15)
        imagenes_layout.setContentsMargins(15, 15, 15, 15)
        area_imagenes.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Panel 1: Imagen Principal (Imagen 1) con histograma
        self.panel_img1 = PanelImagenConHistograma("IMAGEN 1", COLOR_PRIMARIO)
        self.panel_img1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.panel_img1.setMinimumWidth(300)
        self.panel_img1.hide()  # Oculto inicialmente
        imagenes_layout.addWidget(self.panel_img1, 1)
        
        # Panel 2: Segunda Imagen (Imagen 2) con histograma
        self.panel_img2 = PanelImagenConHistograma("IMAGEN 2", COLOR_SECUNDARIO)
        self.panel_img2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.panel_img2.setMinimumWidth(300)
        self.panel_img2.hide()  # Oculto inicialmente
        imagenes_layout.addWidget(self.panel_img2, 1)
        
        # Panel 3: Resultado con histograma
        self.panel_resultado = PanelImagenConHistograma("RESULTADO", COLOR_EXITO)
        self.panel_resultado.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.panel_resultado.setMinimumWidth(300)
        self.panel_resultado.hide()  # Oculto inicialmente
        imagenes_layout.addWidget(self.panel_resultado, 1)
        
        scroll_area.setWidget(area_imagenes)
        area_layout.addWidget(scroll_area)
        
        main_layout.addWidget(area_principal)
        
        # Barra de estado
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_CARD}, stop:1 {COLOR_OSCURO});
                color: {COLOR_TEXT_PRIMARY};
                border-top: 2px solid {COLOR_PRIMARIO};
                font-size: 10px;
                font-weight: bold;
                padding: 5px;
            }}
        """)
        self.statusBar().showMessage("Listo para procesar imagenes")
    

    
    def _crear_separador(self):
        """Crea un separador horizontal."""
        separador = QWidget()
        separador.setFixedHeight(2)
        separador.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLOR_PRIMARIO}, stop:0.5 {COLOR_ACENTO}, stop:1 {COLOR_PRIMARIO});
            border-radius: 1px;
        """)
        return separador
    
    def guardar_en_historial(self):
        """Guarda el estado actual de la imagen 1 en el historial."""
        if self.imagen_actual is not None:
            # Hacer copia profunda de la imagen
            self.historial_img1.append(self.imagen_actual.copy())
            if len(self.historial_img1) > 10:
                self.historial_img1.pop(0)
            # Limpiar historial de rehacer
            self.historial_rehacer_img1.clear()
    
    def mostrar_imagen_1(self):
        """Muestra la imagen 1 en su panel con histograma."""
        if self.imagen_actual is not None:
            self.panel_img1.show()  # Mostrar panel al cargar imagen
            self.panel_img1.mostrar_imagen(self.imagen_actual)
    
    def mostrar_imagen_2(self):
        """Muestra la imagen 2 en su panel con histograma."""
        if self.imagen_segunda is not None:
            self.panel_img2.show()  # Mostrar panel al cargar imagen
            self.panel_img2.mostrar_imagen(self.imagen_segunda)
    
    def mostrar_resultado(self):
        """Muestra el resultado en su panel con histograma."""
        if self.imagen_resultado is not None:
            self.panel_resultado.show()  # Mostrar panel al generar resultado
            self.panel_resultado.mostrar_imagen(self.imagen_resultado)


def main():
    """Función principal."""
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
