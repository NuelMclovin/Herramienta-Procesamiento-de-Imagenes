"""
Módulo de filtros para reducción de ruido y suavizado de imágenes
"""

import cv2
import numpy as np


class Filtros:
    """Clase para aplicar filtros de reducción de ruido y suavizado."""
    
    @staticmethod
    def filtro_promediador(imagen: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Aplica filtro promediador (blur)."""
        return cv2.blur(imagen, (kernel_size, kernel_size))
    
    @staticmethod
    def filtro_mediana(imagen: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Aplica filtro de mediana."""
        return cv2.medianBlur(imagen, kernel_size)
    
    @staticmethod
    def filtro_gaussiano(imagen: np.ndarray, kernel_size: int = 5, sigma: float = 1.0) -> np.ndarray:
        """Aplica filtro gaussiano."""
        return cv2.GaussianBlur(imagen, (kernel_size, kernel_size), sigma)
    
    @staticmethod
    def filtro_bilateral(imagen: np.ndarray, d: int = 9, sigma_color: int = 75, sigma_space: int = 75) -> np.ndarray:
        """Aplica filtro bilateral (preserva bordes)."""
        return cv2.bilateralFilter(imagen, d, sigma_color, sigma_space)
    
    @staticmethod
    def filtro_moda(imagen: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Aplica filtro de moda (aproximado con mediana)."""
        return cv2.medianBlur(imagen, kernel_size)
    
    @staticmethod
    def filtro_minimo(imagen: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Aplica filtro de mínimo (erosión)."""
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(imagen, kernel)
    
    @staticmethod
    def filtro_maximo(imagen: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Aplica filtro de máximo (dilatación)."""
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(imagen, kernel)
