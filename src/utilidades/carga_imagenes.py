"""
Módulo para carga y preprocesamiento de imágenes
"""

import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple


class CargadorImagenes:
    """Clase para cargar y preprocesar imágenes."""
    
    @staticmethod
    def cargar_imagen(ruta: str, convertir_rgb: bool = True) -> Optional[np.ndarray]:
        """
        Carga una imagen desde archivo.
        
        Args:
            ruta: Ruta al archivo de imagen
            convertir_rgb: Si convertir BGR a RGB
            
        Returns:
            Array numpy con la imagen o None si hay error
        """
        try:
            imagen = cv2.imread(ruta)
            if imagen is None:
                return None
            
            if convertir_rgb:
                imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            
            return imagen
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return None
    
    @staticmethod
    def cargar_imagen_pil(ruta: str) -> Optional[Image.Image]:
        """Carga imagen usando PIL."""
        try:
            return Image.open(ruta)
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return None
    
    @staticmethod
    def redimensionar(imagen: np.ndarray, tamano: Tuple[int, int]) -> np.ndarray:
        """Redimensiona la imagen al tamaño especificado."""
        return cv2.resize(imagen, tamano, interpolation=cv2.INTER_AREA)
    
    @staticmethod
    def convertir_a_gris(imagen: np.ndarray) -> np.ndarray:
        """Convierte imagen a escala de grises."""
        if len(imagen.shape) == 3:
            return cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        return imagen
    
    @staticmethod
    def normalizar(imagen: np.ndarray) -> np.ndarray:
        """Normaliza imagen a rango [0, 1]."""
        return imagen.astype(np.float32) / 255.0
    
    @staticmethod
    def desnormalizar(imagen: np.ndarray) -> np.ndarray:
        """Desnormaliza imagen de [0, 1] a [0, 255]."""
        return (imagen * 255).astype(np.uint8)
    
    @staticmethod
    def guardar_imagen(imagen: np.ndarray, ruta: str, convertir_bgr: bool = True) -> bool:
        """
        Guarda imagen en archivo.
        
        Args:
            imagen: Array numpy con la imagen
            ruta: Ruta donde guardar
            convertir_bgr: Si convertir RGB a BGR para OpenCV
            
        Returns:
            True si se guardó correctamente
        """
        try:
            if convertir_bgr and len(imagen.shape) == 3:
                imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
            
            return cv2.imwrite(ruta, imagen)
        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            return False
