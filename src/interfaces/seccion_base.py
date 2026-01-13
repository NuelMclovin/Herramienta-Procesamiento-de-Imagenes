"""
Clase base para las secciones de la interfaz.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from config import COLOR_TEXT_PRIMARY, COLOR_BORDER, COLOR_SECUNDARIO, COLOR_HOVER


class SeccionBase(QWidget):
    """Clase base para crear secciones colapsables en el panel lateral."""
    
    def __init__(self, titulo, color_titulo, ventana_principal):
        super().__init__()
        self.titulo = titulo
        self.color_titulo = color_titulo
        self.ventana_principal = ventana_principal
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de la sección."""
        layout = QVBoxLayout(self)
        layout.setSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Botón de título (expandir/contraer)
        self.btn_titulo = QPushButton(f"▼ {self.titulo}")
        self.btn_titulo.setMinimumHeight(30)
        self.btn_titulo.setMaximumHeight(35)
        self.btn_titulo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_titulo.setStyleSheet(f"""
            QPushButton {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 0.5px;
                padding: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color_titulo}, stop:1 {COLOR_SECUNDARIO});
                border-radius: 6px;
                margin-top: 4px;
                border: 1px solid {COLOR_BORDER};
                text-align: left;
                padding-left: 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_HOVER}, stop:1 {self.color_titulo});
                border: 1px solid {self.color_titulo};
            }}
        """)
        
        # Contenedor de botones (colapsable)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(3)
        self.contenedor_layout.setContentsMargins(2, 2, 2, 2)
        self.contenedor.setVisible(True)
        
        # Conectar toggle
        self.btn_titulo.clicked.connect(self.toggle_seccion)
        
        layout.addWidget(self.btn_titulo)
        layout.addWidget(self.contenedor)
        
        # Crear botones de la sección
        self.crear_botones()
    
    def toggle_seccion(self):
        """Expandir/contraer la sección."""
        visible = self.contenedor.isVisible()
        self.contenedor.setVisible(not visible)
        self.btn_titulo.setText(f"{'▼' if not visible else '▶'} {self.titulo}")
    
    def crear_botones(self):
        """Método a sobrescribir por las clases hijas para crear sus botones."""
        pass
    
    def crear_boton(self, texto, color, callback):
        """Crea un botón para la sección."""
        btn = QPushButton(texto)
        btn.setMinimumHeight(32)
        btn.setMaximumHeight(36)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1f2e, stop:1 #0f1419);
                color: {COLOR_TEXT_PRIMARY};
                border: 1.5px solid {color};
                border-radius: 8px;
                font-size: 8.5px;
                font-weight: 600;
                padding: 6px 8px;
                text-align: left;
                padding-left: 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {COLOR_SECUNDARIO});
                border: 1.5px solid {COLOR_TEXT_PRIMARY};
            }}
            QPushButton:pressed {{
                background: {color};
            }}
        """)
        btn.clicked.connect(callback)
        self.contenedor_layout.addWidget(btn)
        return btn
