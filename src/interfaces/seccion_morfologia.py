"""Sección de morfología matemática."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_SECUNDARIO
import cv2
import numpy as np


class SeccionMorfologia(SeccionBase):
    """Sección para operaciones de morfología matemática."""
    
    def __init__(self, ventana_principal):
        super().__init__("MORFOLOGÍA MATEMÁTICA", COLOR_SECUNDARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de morfología."""
        self.crear_boton("Erosión", COLOR_SECUNDARIO, lambda: self.aplicar_morfologia("erosion"))
        self.crear_boton("Dilatación", COLOR_SECUNDARIO, lambda: self.aplicar_morfologia("dilatacion"))
        self.crear_boton("Apertura", COLOR_SECUNDARIO, lambda: self.aplicar_morfologia("apertura"))
        self.crear_boton("Cierre", COLOR_SECUNDARIO, lambda: self.aplicar_morfologia("cierre"))
        self.crear_boton("Gradiente Morfológico", COLOR_SECUNDARIO, lambda: self.aplicar_morfologia("gradiente"))
    
    def aplicar_morfologia(self, operacion):
        """Aplica operaciones morfológicas."""
        nombres = {
            'erosion': 'Erosión',
            'dilatacion': 'Dilatación',
            'apertura': 'Apertura',
            'cierre': 'Cierre',
            'gradiente': 'Gradiente Morfológico'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[operacion]}")
        dialogo.agregar_selector_imagen()
        
        tamano_spin = dialogo.agregar_spin("Tamaño Kernel:", 3, 15, 5, 2)
        tipo_kernel = dialogo.agregar_combo("Forma Kernel:", 
                                           ["Rectángulo", "Elipse", "Cruz"], 
                                           0)  # Índice en lugar de texto
        
        info = QLabel(f"Se aplicará {nombres[operacion]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_SECUNDARIO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.procesamiento_avanzado import MorfologiaMatematica
            
            try:
                tamano = tamano_spin.value()
                forma_texto = tipo_kernel.currentText()
                
                # Crear kernel según forma
                formas_map = {
                    "Rectángulo": cv2.MORPH_RECT,
                    "Elipse": cv2.MORPH_ELLIPSE,
                    "Cruz": cv2.MORPH_CROSS
                }
                forma = formas_map[forma_texto]
                kernel = cv2.getStructuringElement(forma, (tamano, tamano))
                
                if operacion == "erosion":
                    resultado = MorfologiaMatematica.erosion(imagen, kernel)
                elif operacion == "dilatacion":
                    resultado = MorfologiaMatematica.dilatacion(imagen, kernel)
                elif operacion == "apertura":
                    resultado = MorfologiaMatematica.apertura(imagen, kernel)
                elif operacion == "cierre":
                    resultado = MorfologiaMatematica.cierre(imagen, kernel)
                elif operacion == "gradiente":
                    resultado = MorfologiaMatematica.gradiente_morfologico(imagen, kernel)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[operacion]} aplicado")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
