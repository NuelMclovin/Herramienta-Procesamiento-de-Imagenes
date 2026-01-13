"""
Módulo para análisis de canales de color
"""

import cv2
import numpy as np
from typing import Dict, Optional


class AnalizadorCanales:
    """Clase para análisis de canales RGB, HSV, CMY."""
    
    @staticmethod
    def extraer_canales_rgb(imagen: np.ndarray) -> Dict[str, np.ndarray]:
        """Extrae canales RGB."""
        if len(imagen.shape) != 3:
            return {}
        
        return {
            'Rojo': imagen[:, :, 0],
            'Verde': imagen[:, :, 1],
            'Azul': imagen[:, :, 2]
        }
    
    @staticmethod
    def extraer_canales_hsv(imagen: np.ndarray) -> Dict[str, np.ndarray]:
        """Extrae canales HSV."""
        if len(imagen.shape) != 3:
            return {}
        
        imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_RGB2HSV)
        return {
            'H': imagen_hsv[:, :, 0],
            'S': imagen_hsv[:, :, 1],
            'V': imagen_hsv[:, :, 2]
        }
    
    @staticmethod
    def extraer_canales_cmy(imagen: np.ndarray) -> Dict[str, np.ndarray]:
        """Extrae canales CMY."""
        if len(imagen.shape) != 3:
            return {}
        
        imagen_cmy = 255 - imagen
        return {
            'Cian': imagen_cmy[:, :, 0],
            'Magenta': imagen_cmy[:, :, 1],
            'Amarillo': imagen_cmy[:, :, 2]
        }
    
    @staticmethod
    def calcular_histograma(canal: np.ndarray) -> np.ndarray:
        """Calcula histograma de un canal."""
        histograma, _ = np.histogram(canal.flatten(), bins=256, range=(0, 256))
        return histograma
    
    @staticmethod
    def calcular_estadisticas(canal: np.ndarray) -> Dict[str, float]:
        """Calcula estadísticas de un canal."""
        return {
            'media': float(np.mean(canal)),
            'mediana': float(np.median(canal)),
            'desviacion_estandar': float(np.std(canal)),
            'minimo': float(np.min(canal)),
            'maximo': float(np.max(canal))
        }
