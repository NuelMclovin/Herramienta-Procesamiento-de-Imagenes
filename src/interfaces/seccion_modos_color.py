"""Sección de análisis de modos de color."""

from PySide6.QtWidgets import (
    QMessageBox, QLabel, QDialog, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.interfaces.histograma_widget import HistogramaWidget
from config import (
    COLOR_PRIMARIO, COLOR_FONDO, COLOR_OSCURO, COLOR_TEXT_PRIMARY,
    COLOR_CARD, COLOR_BORDER
)
import numpy as np
import cv2


class SeccionModosColor(SeccionBase):
    """Sección para análisis y conversión de modos de color."""
    
    def __init__(self, ventana_principal):
        super().__init__("MODOS DE COLOR", COLOR_PRIMARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de modos de color."""
        self.crear_boton("Escala de Grises", COLOR_PRIMARIO, lambda: self.convertir_modo("gris"))
        self.crear_boton("Convertir a CMY", COLOR_PRIMARIO, lambda: self.convertir_modo("cmy"))
        self.crear_boton("Convertir a RGB", COLOR_PRIMARIO, lambda: self.convertir_modo("rgb"))
        self.crear_boton("Convertir a HSV", COLOR_PRIMARIO, lambda: self.convertir_modo("hsv"))
        self.crear_boton("Separación de Canales", COLOR_PRIMARIO, self.separar_canales)
    
    def convertir_modo(self, modo):
        """Convierte la imagen a diferentes modos de color."""
        nombres = {
            'gris': 'Escala de Grises',
            'cmy': 'CMY',
            'rgb': 'RGB',
            'hsv': 'HSV'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Convertir a: {nombres[modo]}")
        dialogo.agregar_selector_imagen()
        
        info = QLabel(f"Se convertirá la imagen a {nombres[modo]}")
        info.setStyleSheet(f"color: {COLOR_PRIMARIO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            import cv2
            import numpy as np
            
            try:
                if modo == "gris":
                    if len(imagen.shape) == 2:
                        resultado = imagen
                    else:
                        resultado = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                
                elif modo == "cmy":
                    if len(imagen.shape) == 2:
                        QMessageBox.warning(dialogo, "Advertencia", 
                                          "La imagen debe ser a color")
                        return
                    # Convertir RGB a CMY: CMY = 255 - RGB
                    resultado = 255 - imagen
                
                elif modo == "rgb":
                    if len(imagen.shape) == 2:
                        # Convertir escala de grises a RGB
                        resultado = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
                    else:
                        # Ya está en RGB, devolver copia
                        resultado = imagen.copy()
                
                elif modo == "hsv":
                    if len(imagen.shape) == 2:
                        QMessageBox.warning(dialogo, "Advertencia", 
                                          "La imagen debe ser a color")
                        return
                    resultado = cv2.cvtColor(imagen, cv2.COLOR_RGB2HSV)
                
                # Actualizar el modo de color de la imagen
                if tipo == 'img1':
                    if modo == "gris":
                        self.ventana_principal.modo_color_img1 = 'GRAY'
                    elif modo == "cmy":
                        self.ventana_principal.modo_color_img1 = 'CMY'
                    elif modo == "rgb":
                        self.ventana_principal.modo_color_img1 = 'RGB'
                    elif modo == "hsv":
                        self.ventana_principal.modo_color_img1 = 'HSV'
                elif tipo == 'img2':
                    if modo == "gris":
                        self.ventana_principal.modo_color_img2 = 'GRAY'
                    elif modo == "cmy":
                        self.ventana_principal.modo_color_img2 = 'CMY'
                    elif modo == "rgb":
                        self.ventana_principal.modo_color_img2 = 'RGB'
                    elif modo == "hsv":
                        self.ventana_principal.modo_color_img2 = 'HSV'
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"Convertido a {nombres[modo]}")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def separar_canales(self):
        """Muestra una ventana con la separación de canales según el modo de color."""
        dialogo = DialogoBase(self.ventana_principal, "Separar Canales")
        dialogo.agregar_selector_imagen()
        
        info = QLabel("Se mostrarán los canales individuales de la imagen con sus histogramas")
        info.setStyleSheet(f"color: {COLOR_PRIMARIO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            # Obtener el modo de color almacenado
            if tipo == 'img1':
                modo_color = self.ventana_principal.modo_color_img1
            elif tipo == 'img2':
                modo_color = self.ventana_principal.modo_color_img2
            else:
                modo_color = self.ventana_principal.modo_color_resultado
            
            try:
                # Crear ventana de separación de canales con el modo de color
                ventana_canales = VentanaSeparacionCanales(self.ventana_principal, imagen, modo_color)
                ventana_canales.exec()
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()


class VentanaSeparacionCanales(QDialog):
    """Ventana que muestra la separación de canales con histogramas."""
    
    def __init__(self, parent, imagen, modo_color='RGB'):
        super().__init__(parent)
        self.modo_color = modo_color
        self.setWindowTitle("Separación de Canales")
        self.setMinimumSize(900, 600)
        
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
        
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setSpacing(15)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        
        # Detectar el modo de color y separar canales
        self.mostrar_canales(imagen)
    
    def detectar_modo_color(self, imagen):
        """Detecta el modo de color de la imagen."""
        if len(imagen.shape) == 2:
            return "Escala de Grises"
        
        canal_0 = imagen[:, :, 0]
        max_0 = np.max(canal_0)
        media_0 = np.mean(imagen[:, :, 0])
        media_1 = np.mean(imagen[:, :, 1])
        media_2 = np.mean(imagen[:, :, 2])
        
        # HSV: Canal H tiene rango 0-179
        if max_0 <= 180:
            return "HSV"
        # CMY: Valores promedio altos en todos los canales
        elif media_0 > 200 and media_1 > 200 and media_2 > 200:
            return "CMY"
        else:
            return "RGB"
    
    def mostrar_canales(self, imagen):
        """Muestra los canales según el modo de color almacenado."""
        # Usar el modo de color almacenado
        modo_color = self.modo_color
        
        # Título con modo de color
        titulo = QLabel(f"CANALES SEPARADOS - Modo: {modo_color}")
        titulo.setStyleSheet(f"""
            color: {COLOR_PRIMARIO};
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.addWidget(titulo)
        
        # Área de scroll para los canales
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
        """)
        
        contenedor = QWidget()
        contenedor_layout = QHBoxLayout(contenedor)
        contenedor_layout.setSpacing(20)
        
        # Usar el modo de color almacenado
        if self.modo_color == 'GRAY' or len(imagen.shape) == 2:
            # Escala de grises
            self.agregar_canal(contenedor_layout, imagen, "Intensidad", "gray")
        else:
            # Separar según el modo de color almacenado
            canales = self.separar_imagen_por_modo(imagen, self.modo_color)
            
            for nombre, canal, cmap in canales:
                self.agregar_canal(contenedor_layout, canal, nombre, cmap)
        
        scroll.setWidget(contenedor)
        self.layout_principal.addWidget(scroll)
    
    def separar_imagen_por_modo(self, imagen, modo_color):
        """Separa la imagen en sus canales según el modo de color especificado."""
        canales_resultado = []
        
        if modo_color == 'HSV':
            # Canales HSV
            nombres = ["H (Matiz)", "S (Saturación)", "V (Valor)"]
            cmaps = ["hsv", "gray", "gray"]
            for i, (nombre, cmap) in enumerate(zip(nombres, cmaps)):
                canal = imagen[:, :, i]
                # Normalizar H para visualización (0-179 -> 0-255)
                if i == 0 and np.max(canal) <= 179:
                    canal = (canal * 255 / 179).astype(np.uint8)
                canales_resultado.append((nombre, canal, cmap))
        
        elif modo_color == 'CMY':
            # Canales CMY
            nombres = ["C (Cian)", "M (Magenta)", "Y (Amarillo)"]
            cmaps = ["cyan", "magenta", "yellow"]
            for i, (nombre, cmap) in enumerate(zip(nombres, cmaps)):
                canal = imagen[:, :, i]
                canales_resultado.append((nombre, canal, cmap))
        
        else:  # RGB por defecto
            # Canales RGB
            nombres = ["R (Rojo)", "G (Verde)", "B (Azul)"]
            cmaps = ["red", "green", "blue"]
            for i, (nombre, cmap) in enumerate(zip(nombres, cmaps)):
                canal = imagen[:, :, i]
                canales_resultado.append((nombre, canal, cmap))
        
        return canales_resultado
    
    def agregar_canal(self, layout, canal, nombre, colormap):
        """Agrega un canal con su histograma al layout."""
        grupo = QGroupBox(nombre)
        grupo_layout = QVBoxLayout(grupo)
        
        # Guardar canal original para resaltado
        canal_original = canal.copy()
        
        # Redimensionar si es muy grande
        altura, ancho = canal.shape if len(canal.shape) == 2 else canal.shape[:2]
        max_size = 250
        
        if altura > max_size or ancho > max_size:
            scale = min(max_size / altura, max_size / ancho)
            nuevo_ancho = int(ancho * scale)
            nuevo_alto = int(altura * scale)
            canal_mostrar = cv2.resize(canal, (nuevo_ancho, nuevo_alto))
        else:
            canal_mostrar = canal.copy()
        
        # Función para aplicar colormap
        def aplicar_colormap(canal_data, cmap):
            """Aplica colormap a un canal."""
            if cmap == "gray":
                return canal_data
            elif cmap == "red":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 0] = canal_data
                return resultado
            elif cmap == "green":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 1] = canal_data
                return resultado
            elif cmap == "blue":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 2] = canal_data
                return resultado
            elif cmap == "cyan":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 1] = canal_data
                resultado[:, :, 2] = canal_data
                return resultado
            elif cmap == "magenta":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 0] = canal_data
                resultado[:, :, 2] = canal_data
                return resultado
            elif cmap == "yellow":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 0] = canal_data
                resultado[:, :, 1] = canal_data
                return resultado
            elif cmap == "hsv":
                resultado = np.zeros((*canal_data.shape, 3), dtype=np.uint8)
                resultado[:, :, 0] = canal_data
                resultado[:, :, 1] = 255
                resultado[:, :, 2] = 255
                return cv2.cvtColor(resultado, cv2.COLOR_HSV2RGB)
            else:
                return canal_data
        
        # Aplicar colormap inicial
        canal_vis = aplicar_colormap(canal_mostrar, colormap)
        
        # Función para convertir numpy a QPixmap
        def convertir_a_pixmap(imagen_data):
            """Convierte numpy array a QPixmap."""
            if len(imagen_data.shape) == 2:
                h, w = imagen_data.shape
                bytes_per_line = w
                qimage = QImage(imagen_data.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
            else:
                h, w, c = imagen_data.shape
                bytes_per_line = c * w
                qimage = QImage(imagen_data.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            return QPixmap.fromImage(qimage)
        
        # Label para la imagen
        label_imagen = QLabel()
        label_imagen.setPixmap(convertir_a_pixmap(canal_vis))
        label_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grupo_layout.addWidget(label_imagen)
        
        # Label para mostrar el valor del histograma
        label_valor = QLabel("Mueve el cursor sobre el histograma")
        label_valor.setStyleSheet(f"""
            color: {COLOR_PRIMARIO};
            font-size: 11px;
            font-weight: bold;
            padding: 5px;
        """)
        label_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grupo_layout.addWidget(label_valor)
        
        # Histograma dinámico
        histograma = HistogramaWidget()
        histograma.calcular_histograma(canal)
        
        # Conectar señales del histograma para resaltar y mostrar valores
        def resaltar_valor(valor):
            """Resalta los píxeles con el valor seleccionado."""
            # Contar cuántos píxeles tienen ese valor
            count = int(np.sum(canal_original == valor))
            label_valor.setText(f"Valor: {valor} | Píxeles: {count:,}")
            
            # Crear máscara de píxeles cercanos al valor seleccionado (±5)
            rango = 5
            mascara = np.abs(canal_mostrar.astype(int) - valor) <= rango
            
            # Crear imagen resaltada con colormap
            canal_resaltado = aplicar_colormap(canal_mostrar, colormap)
            
            # Convertir a RGB si es escala de grises para poder resaltar
            if len(canal_resaltado.shape) == 2:
                canal_resaltado = cv2.cvtColor(canal_resaltado, cv2.COLOR_GRAY2RGB)
            
            # Resaltar en amarillo los píxeles seleccionados
            canal_resaltado[mascara] = [255, 255, 0]  # Amarillo en RGB
            
            # Actualizar la imagen
            label_imagen.setPixmap(convertir_a_pixmap(canal_resaltado))
        
        def limpiar_resaltado():
            """Limpia el resaltado y muestra la imagen original."""
            label_valor.setText("Mueve el cursor sobre el histograma")
            # Restaurar imagen original con colormap
            canal_vis_original = aplicar_colormap(canal_mostrar, colormap)
            label_imagen.setPixmap(convertir_a_pixmap(canal_vis_original))
        
        histograma.valor_seleccionado.connect(resaltar_valor)
        histograma.sin_seleccion.connect(limpiar_resaltado)
        
        grupo_layout.addWidget(histograma)
        
        layout.addWidget(grupo)
