"""
Módulo de umbralización para binarización de imágenes
"""

import cv2
import numpy as np
from typing import Tuple


class Umbralizacion:
    """
    Clase para aplicar técnicas de umbralización.
    """
    
    @staticmethod
    def _convertir_a_gris(imagen: np.ndarray) -> np.ndarray:
        """Convierte imagen a escala de grises si es necesario."""
        if len(imagen.shape) == 3:
            return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        return imagen
    
    @staticmethod
    def umbral_fijo(imagen: np.ndarray, umbral: int = 127) -> np.ndarray:
        """
        Aplica umbralización con valor fijo.
        
        Args:
            imagen: Imagen de entrada
            umbral: Valor de umbral (0-255)
            
        Returns:
            Imagen binarizada
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        _, resultado = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)
        return resultado
    
    @staticmethod
    def umbral_adaptativo(imagen: np.ndarray, block_size: int = 11, C: int = 2) -> np.ndarray:
        """
        Aplica umbralización adaptativa.
        
        Args:
            imagen: Imagen de entrada
            block_size: Tamaño del bloque (debe ser impar)
            C: Constante a restar de la media
            
        Returns:
            Imagen binarizada
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        
        if block_size % 2 == 0:
            block_size += 1
        
        resultado = cv2.adaptiveThreshold(
            imagen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, C
        )
        return resultado
    
    @staticmethod
    def umbral_otsu(imagen: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Aplica umbralización usando método de Otsu.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Tupla (imagen_binarizada, umbral_utilizado)
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        umbral, resultado = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return resultado, float(umbral)
    
    @staticmethod
    def umbral_inverso(imagen: np.ndarray, umbral: int = 127) -> np.ndarray:
        """
        Aplica umbralización inversa.
        
        Args:
            imagen: Imagen de entrada
            umbral: Valor de umbral (0-255)
            
        Returns:
            Imagen binarizada inversa
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        _, resultado = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY_INV)
        return resultado
    
    @staticmethod
    def umbral_truncado(imagen: np.ndarray, umbral: int = 127) -> np.ndarray:
        """
        Aplica umbralización truncada.
        
        Args:
            imagen: Imagen de entrada
            umbral: Valor de umbral (0-255)
            
        Returns:
            Imagen con umbral truncado
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        _, resultado = cv2.threshold(imagen, umbral, 255, cv2.THRESH_TRUNC)
        return resultado
    
    @staticmethod
    def umbral_a_cero(imagen: np.ndarray, umbral: int = 127) -> np.ndarray:
        """
        Aplica umbralización a cero.
        
        Args:
            imagen: Imagen de entrada
            umbral: Valor de umbral (0-255)
            
        Returns:
            Imagen con umbral a cero
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        _, resultado = cv2.threshold(imagen, umbral, 255, cv2.THRESH_TOZERO)
        return resultado
    
    @staticmethod
    def umbral_a_cero_inverso(imagen: np.ndarray, umbral: int = 127) -> np.ndarray:
        """
        Aplica umbralización a cero inversa.
        
        Args:
            imagen: Imagen de entrada
            umbral: Valor de umbral (0-255)
            
        Returns:
            Imagen con umbral a cero inverso
        """
        imagen = Umbralizacion._convertir_a_gris(imagen)
        _, resultado = cv2.threshold(imagen, umbral, 255, cv2.THRESH_TOZERO_INV)
        return resultado
