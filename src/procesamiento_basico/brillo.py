"""
Módulo de ajuste de brillo y ecualización de histogramas
"""

import cv2
import numpy as np
from typing import Tuple


class AjusteBrillo:
    """
    Clase para aplicar técnicas de ajuste de brillo y ecualización.
    """
    
    @staticmethod
    def _convertir_a_gris(imagen: np.ndarray) -> np.ndarray:
        """Convierte imagen a escala de grises si es necesario."""
        if len(imagen.shape) == 3:
            return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        return imagen
    
    @staticmethod
    def ecualizacion_uniforme(imagen: np.ndarray) -> np.ndarray:
        """
        Aplica ecualización uniforme del histograma.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Imagen ecualizada
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return cv2.equalizeHist(imagen)
    
    @staticmethod
    def ecualizacion_exponencial(imagen: np.ndarray) -> np.ndarray:
        """
        Aplica ecualización exponencial.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Imagen con ecualización exponencial
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return np.uint8(255 * (1 - np.exp(-imagen / 255)))
    
    @staticmethod
    def ecualizacion_rayleigh(imagen: np.ndarray) -> np.ndarray:
        """
        Aplica ecualización Rayleigh.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Imagen con ecualización Rayleigh
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return np.uint8(255 * np.sqrt(imagen / 255))
    
    @staticmethod
    def ecualizacion_hipercubica(imagen: np.ndarray) -> np.ndarray:
        """
        Aplica ecualización hipercúbica.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Imagen con ecualización hipercúbica
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return np.uint8(255 * (imagen / 255) ** 4)
    
    @staticmethod
    def ecualizacion_logaritmica_hiperbolica(imagen: np.ndarray) -> np.ndarray:
        """
        Aplica ecualización logarítmica hiperbólica.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Imagen con ecualización logarítmica hiperbólica
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return np.uint8(255 * np.log1p(imagen) / np.log1p(255))
    
    @staticmethod
    def funcion_potencia(imagen: np.ndarray, potencia: float = 2.0) -> np.ndarray:
        """
        Aplica función potencia.
        
        Args:
            imagen: Imagen de entrada
            potencia: Exponente de la función potencia
            
        Returns:
            Imagen con función potencia aplicada
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return np.uint8(255 * (imagen / 255) ** potencia)
    
    @staticmethod
    def correccion_gamma(imagen: np.ndarray, gamma: float) -> np.ndarray:
        """
        Aplica corrección gamma.
        
        Args:
            imagen: Imagen de entrada
            gamma: Valor de gamma para la corrección
            
        Returns:
            Imagen con corrección gamma aplicada
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        imagen_gamma = np.power(imagen / 255.0, gamma) * 255
        return np.uint8(imagen_gamma)
    
    @staticmethod
    def clahe(imagen: np.ndarray, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        Aplica CLAHE (Contrast Limited Adaptive Histogram Equalization).
        
        Args:
            imagen: Imagen de entrada
            clip_limit: Límite de contraste
            tile_grid_size: Tamaño de la cuadrícula de azulejos
            
        Returns:
            Imagen con CLAHE aplicado
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(imagen)
    
    @staticmethod
    def normalizacion(imagen: np.ndarray, rango_min: int = 0, rango_max: int = 255) -> np.ndarray:
        """
        Normaliza la imagen a un rango específico.
        
        Args:
            imagen: Imagen de entrada
            rango_min: Valor mínimo del rango
            rango_max: Valor máximo del rango
            
        Returns:
            Imagen normalizada
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        return cv2.normalize(imagen, None, rango_min, rango_max, cv2.NORM_MINMAX)
    
    @staticmethod
    def realce_adaptativo(imagen: np.ndarray, clip_limit: float = 3.0) -> np.ndarray:
        """
        Aplica realce adaptativo de contraste.
        
        Args:
            imagen: Imagen de entrada
            clip_limit: Límite de contraste
            
        Returns:
            Imagen con realce adaptativo
        """
        imagen = AjusteBrillo._convertir_a_gris(imagen)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(16, 16))
        return clahe.apply(imagen)
