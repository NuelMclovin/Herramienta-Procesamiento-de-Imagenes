"""Sección de operaciones lógicas entre imágenes."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from config import COLOR_ERROR
import numpy as np


class SeccionLogicas(SeccionBase):
    """Sección para operaciones lógicas entre imágenes."""
    
    def __init__(self, ventana_principal):
        super().__init__("OPERACIONES LÓGICAS", COLOR_ERROR, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de operaciones lógicas."""
        self.crear_boton("AND Lógico", COLOR_ERROR, lambda: self.aplicar_operacion("and"))
        self.crear_boton("OR Lógico", COLOR_ERROR, lambda: self.aplicar_operacion("or"))
        self.crear_boton("XOR Lógico", COLOR_ERROR, lambda: self.aplicar_operacion("xor"))
        self.crear_boton("NOT Lógico", COLOR_ERROR, lambda: self.aplicar_operacion("not"))
    
    def aplicar_operacion(self, operacion):
        """Aplica operaciones lógicas entre Imagen 1 e Imagen 2."""
        from src.operaciones import OperacionesLogicas
        import cv2
        import numpy as np
        
        nombres = {
            'and': 'AND Lógico',
            'or': 'OR Lógico',
            'xor': 'XOR Lógico',
            'not': 'NOT Lógico'
        }
        
        try:
            if operacion == "not":
                # NOT solo necesita Imagen 1
                if self.ventana_principal.imagen_actual is None:
                    QMessageBox.warning(self.ventana_principal, "Advertencia", 
                                      "Carga una imagen en Imagen 1")
                    return
                
                img = self.ventana_principal.imagen_actual.copy()
                
                # Convertir a uint8 si es necesario
                if img.dtype != np.uint8:
                    if img.max() <= 1.0:
                        img = (img * 255).astype(np.uint8)
                    else:
                        img = np.clip(img, 0, 255).astype(np.uint8)
                
                resultado = OperacionesLogicas.operacion_not(img)
                self.ventana_principal.imagen_resultado = resultado
                self.ventana_principal.mostrar_resultado()
                self.ventana_principal.statusBar().showMessage(f"NOT Lógico aplicado")
            else:
                # AND, OR, XOR necesitan ambas imágenes
                if self.ventana_principal.imagen_actual is None or self.ventana_principal.imagen_segunda is None:
                    QMessageBox.warning(self.ventana_principal, "Advertencia", 
                                      "Carga imágenes en Imagen 1 e Imagen 2")
                    return
                
                img1 = self.ventana_principal.imagen_actual.copy()
                img2 = self.ventana_principal.imagen_segunda.copy()
                
                # Convertir a uint8 si es necesario
                if img1.dtype != np.uint8:
                    if img1.max() <= 1.0:
                        img1 = (img1 * 255).astype(np.uint8)
                    else:
                        img1 = np.clip(img1, 0, 255).astype(np.uint8)
                
                if img2.dtype != np.uint8:
                    if img2.max() <= 1.0:
                        img2 = (img2 * 255).astype(np.uint8)
                    else:
                        img2 = np.clip(img2, 0, 255).astype(np.uint8)
                
                # Asegurar que ambas imágenes tengan las mismas dimensiones
                if img1.shape != img2.shape:
                    # Si tienen diferente número de canales (color vs gris)
                    if len(img1.shape) == 2 and len(img2.shape) == 3:
                        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
                    elif len(img1.shape) == 3 and len(img2.shape) == 2:
                        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
                    
                    # Si tienen diferente tamaño (ancho x alto)
                    if img1.shape[:2] != img2.shape[:2]:
                        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                
                if operacion == "and":
                    resultado = OperacionesLogicas.operacion_and(img1, img2)
                elif operacion == "or":
                    resultado = OperacionesLogicas.operacion_or(img1, img2)
                elif operacion == "xor":
                    resultado = OperacionesLogicas.operacion_xor(img1, img2)
                
                self.ventana_principal.imagen_resultado = resultado
                self.ventana_principal.mostrar_resultado()
                self.ventana_principal.statusBar().showMessage(f"{nombres[operacion]} → Resultado")
        
        except Exception as e:
            QMessageBox.critical(self.ventana_principal, "Error", f"Error en operación: {str(e)}\n\nDetalles: Verifica que las imágenes sean compatibles")
