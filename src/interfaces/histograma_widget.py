"""
Widget de histograma interactivo para imágenes.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QImage, QPixmap
import numpy as np
import cv2


class HistogramaWidget(QWidget):
    """Widget que muestra un histograma interactivo de una imagen."""
    
    # Señal emitida cuando se mueve el cursor sobre el histograma
    valor_seleccionado = Signal(int)  # Emite el valor de intensidad seleccionado
    sin_seleccion = Signal()  # Emite cuando el cursor sale del histograma
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.histograma = None
        self.imagen_original = None
        self.valor_actual = -1
        self.setFixedHeight(120)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: #1E2640; border: 2px solid #667EEA; border-radius: 5px;")
    
    def calcular_histograma(self, imagen):
        """Calcula el histograma de la imagen."""
        self.imagen_original = imagen
        
        if imagen is None:
            self.histograma = None
            self.update()
            return
        
        # Convertir a escala de grises si es necesario
        if len(imagen.shape) == 3:
            img_gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        else:
            img_gris = imagen
        
        # Calcular histograma
        self.histograma = cv2.calcHist([img_gris], [0], None, [256], [0, 256])
        self.histograma = self.histograma.flatten()
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el histograma."""
        super().paintEvent(event)
        
        if self.histograma is None:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensiones del widget
        width = self.width() - 20
        height = self.height() - 20
        offset_x = 10
        offset_y = 10
        
        # Normalizar histograma
        max_val = np.max(self.histograma)
        if max_val == 0:
            return
        
        hist_norm = (self.histograma / max_val) * height
        
        # Dibujar barras del histograma
        bar_width = width / 256.0
        
        for i in range(256):
            # Color de la barra según la intensidad
            color = QColor(i, i, i)
            
            # Si es el valor actual, resaltar
            if i == self.valor_actual:
                pen = QPen(QColor(255, 0, 0), 2)
                painter.setPen(pen)
                painter.setBrush(QColor(255, 100, 100, 150))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(color)
            
            x = offset_x + i * bar_width
            y = offset_y + height - hist_norm[i]
            h = hist_norm[i]
            
            painter.drawRect(int(x), int(y), max(1, int(bar_width)), int(h))
        
        # Dibujar línea vertical en el valor actual
        if self.valor_actual >= 0:
            pen = QPen(QColor(255, 255, 0), 2)
            painter.setPen(pen)
            x = offset_x + self.valor_actual * bar_width
            painter.drawLine(int(x), offset_y, int(x), offset_y + height)
        
        painter.end()
    
    def mouseMoveEvent(self, event):
        """Maneja el movimiento del mouse sobre el histograma."""
        if self.histograma is None:
            return
        
        # Calcular el valor de intensidad según la posición del mouse
        width = self.width() - 20
        offset_x = 10
        
        x = event.pos().x() - offset_x
        
        if 0 <= x <= width:
            valor = int((x / width) * 256)
            valor = max(0, min(255, valor))
            
            if valor != self.valor_actual:
                self.valor_actual = valor
                self.valor_seleccionado.emit(valor)
                self.update()
        else:
            if self.valor_actual >= 0:
                self.valor_actual = -1
                self.sin_seleccion.emit()
                self.update()
    
    def leaveEvent(self, event):
        """Maneja cuando el mouse sale del widget."""
        if self.valor_actual >= 0:
            self.valor_actual = -1
            self.sin_seleccion.emit()
            self.update()


class PanelImagenConHistograma(QWidget):
    """Panel que contiene una imagen y su histograma."""
    
    def __init__(self, titulo, color_borde, parent=None):
        super().__init__(parent)
        self.imagen_actual = None
        self.imagen_resaltada = None
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        self.label_titulo = QLabel(titulo)
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_titulo.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color_borde}, stop:1 #764BA2);
                border-radius: 8px;
                border: 2px solid {color_borde};
            }}
        """)
        
        # Contenedor cuadrado para la imagen
        self.imagen_container = QWidget()
        self.imagen_container.setFixedSize(400, 400)
        self.imagen_container.setStyleSheet(f"""
            QWidget {{
                background: #1E2640;
                border: 3px solid {color_borde};
                border-radius: 10px;
            }}
        """)
        
        imagen_layout = QVBoxLayout(self.imagen_container)
        imagen_layout.setContentsMargins(10, 10, 10, 10)
        
        # Label para la imagen
        self.label_imagen = QLabel()
        self.label_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_imagen.setStyleSheet("color: #A8B2D1; border: none;")
        self.label_imagen.setText("Sin imagen")
        self.label_imagen.setScaledContents(False)
        
        imagen_layout.addWidget(self.label_imagen)
        
        # Histograma
        self.histograma = HistogramaWidget()
        self.histograma.valor_seleccionado.connect(self.resaltar_valor)
        self.histograma.sin_seleccion.connect(self.limpiar_resaltado)
        
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.imagen_container)
        layout.addWidget(self.histograma)
    
    def mostrar_imagen(self, imagen):
        """Muestra una imagen en el panel y actualiza el histograma."""
        if imagen is None:
            self.label_imagen.clear()
            self.label_imagen.setText("Sin imagen")
            self.histograma.calcular_histograma(None)
            self.imagen_actual = None
            return
        
        self.imagen_actual = imagen.copy()
        self.imagen_resaltada = None
        
        # Mostrar imagen
        self._actualizar_display(imagen)
        
        # Actualizar histograma
        self.histograma.calcular_histograma(imagen)
    
    def _actualizar_display(self, imagen):
        """Actualiza el display de la imagen."""
        try:
            # Convertir numpy array a QImage
            if len(imagen.shape) == 2:  # Escala de grises
                height, width = imagen.shape
                bytes_per_line = width
                q_img = QImage(imagen.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
            else:  # Color
                height, width, channels = imagen.shape
                bytes_per_line = channels * width
                if channels == 3:
                    # La imagen ya está en RGB desde la carga, no convertir nuevamente
                    q_img = QImage(imagen.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                elif channels == 4:
                    q_img = QImage(imagen.data, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)
            
            # Crear pixmap y escalar manteniendo aspecto (tamaño fijo 380x380)
            pixmap = QPixmap.fromImage(q_img)
            scaled_pixmap = pixmap.scaled(
                380, 380,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label_imagen.setPixmap(scaled_pixmap)
        except Exception as e:
            self.label_imagen.setText(f"Error: {str(e)}")
    
    def resaltar_valor(self, valor):
        """Resalta los píxeles con el valor especificado."""
        if self.imagen_actual is None:
            return
        
        # Convertir a escala de grises si es necesario
        if len(self.imagen_actual.shape) == 3:
            img_gris = cv2.cvtColor(self.imagen_actual, cv2.COLOR_RGB2GRAY)
        else:
            img_gris = self.imagen_actual
        
        # Crear máscara de píxeles con valores cercanos al seleccionado (±5)
        rango = 5
        mascara = np.abs(img_gris.astype(int) - valor) <= rango
        
        # Crear imagen resaltada
        if len(self.imagen_actual.shape) == 3:
            img_resaltada = self.imagen_actual.copy()
            # Resaltar en amarillo los píxeles seleccionados (RGB)
            img_resaltada[mascara] = [255, 255, 0]  # Amarillo en RGB
        else:
            # Convertir a color para poder resaltar
            img_resaltada = cv2.cvtColor(self.imagen_actual, cv2.COLOR_GRAY2RGB)
            img_resaltada[mascara] = [255, 255, 0]  # Amarillo en RGB
        
        self.imagen_resaltada = img_resaltada
        self._actualizar_display(img_resaltada)
    
    def limpiar_resaltado(self):
        """Elimina el resaltado y muestra la imagen original."""
        if self.imagen_actual is not None and self.imagen_resaltada is not None:
            self._actualizar_display(self.imagen_actual)
            self.imagen_resaltada = None
