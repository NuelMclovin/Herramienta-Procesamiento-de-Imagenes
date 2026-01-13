"""Sección de utilidades (modos de color y deshacer/rehacer)."""

from PySide6.QtWidgets import QMessageBox, QLabel
import cv2
import numpy as np
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_INFO


class SeccionUtilidades(SeccionBase):
    """Sección para cambiar modos de color y deshacer/rehacer."""
    
    def __init__(self, ventana_principal):
        super().__init__("UTILIDADES", COLOR_INFO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de utilidades."""
        self.crear_boton("Convertir a Color", COLOR_INFO, self.convertir_a_color)
        self.crear_boton("Convertir a Grises", COLOR_INFO, self.convertir_a_grises)
        self.crear_boton("Convertir a Binaria", COLOR_INFO, self.convertir_a_binaria)
        self.crear_boton("Deshacer Imagen 1", COLOR_INFO, self.deshacer_imagen_1)
        self.crear_boton("Rehacer Imagen 1", COLOR_INFO, self.rehacer_imagen_1)
    
    def convertir_a_color(self):
        """Convierte la imagen seleccionada a color."""
        dialogo = DialogoBase(self.ventana_principal, "Convertir a Color")
        dialogo.agregar_selector_imagen()
        
        # Info
        info = QLabel("Se convertira la imagen a modo COLOR (RGB)")
        info.setStyleSheet(f"color: {COLOR_INFO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                if len(imagen.shape) == 2:  # Escala de grises
                    resultado = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
                elif len(imagen.shape) == 3 and imagen.shape[2] == 1:
                    resultado = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
                else:
                    QMessageBox.information(dialogo, "Info", "La imagen ya esta en color")
                    return
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage("Imagen convertida a color")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al convertir: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def convertir_a_grises(self):
        """Convierte la imagen seleccionada a escala de grises."""
        dialogo = DialogoBase(self.ventana_principal, "Convertir a Escala de Grises")
        dialogo.agregar_selector_imagen()
        
        # Info
        info = QLabel("Se convertira la imagen a modo ESCALA DE GRISES")
        info.setStyleSheet(f"color: {COLOR_INFO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                if len(imagen.shape) == 3:  # Color
                    resultado = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                else:
                    QMessageBox.information(dialogo, "Info", "La imagen ya esta en escala de grises")
                    return
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage("Imagen convertida a escala de grises")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al convertir: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def convertir_a_binaria(self):
        """Convierte la imagen seleccionada a binaria."""
        dialogo = DialogoBase(self.ventana_principal, "Convertir a Binaria")
        dialogo.agregar_selector_imagen()
        
        # Parámetros
        umbral_spin = dialogo.agregar_spin("Valor umbral:", 0, 255, 127, 1)
        metodo_combo = dialogo.agregar_combo("Método:", ["Manual", "Otsu", "Adaptativo"], 1)
        
        # Info
        info = QLabel("Se convertira la imagen a modo BINARIO")
        info.setStyleSheet(f"color: {COLOR_INFO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                # Convertir a grises si es necesario
                if len(imagen.shape) == 3:
                    img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
                else:
                    img_gris = imagen
                
                metodo = metodo_combo.currentIndex()
                umbral = umbral_spin.value()
                
                if metodo == 0:  # Manual
                    _, resultado = cv2.threshold(img_gris, umbral, 255, cv2.THRESH_BINARY)
                elif metodo == 1:  # Otsu
                    _, resultado = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                else:  # Adaptativo
                    resultado = cv2.adaptiveThreshold(img_gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                     cv2.THRESH_BINARY, 11, 2)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage("Imagen convertida a binaria")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al convertir: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()

    
    def deshacer_imagen_1(self):
        """Deshace el último cambio en la imagen 1."""
        if not hasattr(self.ventana_principal, 'historial_img1') or len(self.ventana_principal.historial_img1) == 0:
            QMessageBox.information(self.ventana_principal, "Info", "No hay cambios para deshacer")
            return
        
        try:
            # Guardar estado actual en rehacer
            if self.ventana_principal.imagen_actual is not None:
                if not hasattr(self.ventana_principal, 'historial_rehacer_img1'):
                    self.ventana_principal.historial_rehacer_img1 = []
                
                self.ventana_principal.historial_rehacer_img1.append(
                    self.ventana_principal.imagen_actual.copy()
                )
                
                # Limitar tamaño del historial de rehacer
                if len(self.ventana_principal.historial_rehacer_img1) > 10:
                    self.ventana_principal.historial_rehacer_img1.pop(0)
            
            # Recuperar estado anterior
            self.ventana_principal.imagen_actual = self.ventana_principal.historial_img1.pop()
            self.ventana_principal.mostrar_imagen_1()
            self.ventana_principal.statusBar().showMessage("Cambio deshecho")
        except Exception as e:
            QMessageBox.critical(self.ventana_principal, "Error", f"Error al deshacer: {str(e)}")
    
    def rehacer_imagen_1(self):
        """Rehace el último cambio deshecho en la imagen 1."""
        if not hasattr(self.ventana_principal, 'historial_rehacer_img1') or len(self.ventana_principal.historial_rehacer_img1) == 0:
            QMessageBox.information(self.ventana_principal, "Info", "No hay cambios para rehacer")
            return
        
        try:
            # Guardar estado actual en historial
            if self.ventana_principal.imagen_actual is not None:
                self._guardar_en_historial()
            
            # Recuperar estado siguiente
            self.ventana_principal.imagen_actual = self.ventana_principal.historial_rehacer_img1.pop()
            self.ventana_principal.mostrar_imagen_1()
            self.ventana_principal.statusBar().showMessage("Cambio rehecho")
        except Exception as e:
            QMessageBox.critical(self.ventana_principal, "Error", f"Error al rehacer: {str(e)}")
    
    def _guardar_en_historial(self):
        """Guarda el estado actual en el historial."""
        if self.ventana_principal.imagen_actual is not None:
            # Inicializar historial si no existe
            if not hasattr(self.ventana_principal, 'historial_img1'):
                self.ventana_principal.historial_img1 = []
            
            # Guardar copia del estado actual
            self.ventana_principal.historial_img1.append(
                self.ventana_principal.imagen_actual.copy()
            )
            
            # Limitar tamaño del historial a 10 estados
            if len(self.ventana_principal.historial_img1) > 10:
                self.ventana_principal.historial_img1.pop(0)
            
            # Limpiar historial de rehacer cuando se hace un cambio nuevo
            if hasattr(self.ventana_principal, 'historial_rehacer_img1'):
                self.ventana_principal.historial_rehacer_img1.clear()
