"""
Módulo de morfología matemática
"""

import cv2
import numpy as np


class MorfologiaMatematica:
    """Clase para operaciones de morfología matemática."""
    
    @staticmethod
    def erosion(imagen: np.ndarray, kernel: np.ndarray = None, iteraciones: int = 1) -> np.ndarray:
        """Aplica erosión."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(imagen, kernel, iterations=iteraciones)
    
    @staticmethod
    def dilatacion(imagen: np.ndarray, kernel: np.ndarray = None, iteraciones: int = 1) -> np.ndarray:
        """Aplica dilatación."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(imagen, kernel, iterations=iteraciones)
    
    @staticmethod
    def apertura(imagen: np.ndarray, kernel: np.ndarray = None, iteraciones: int = 1) -> np.ndarray:
        """Aplica apertura (erosión seguida de dilatación)."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel, iterations=iteraciones)
    
    @staticmethod
    def cierre(imagen: np.ndarray, kernel: np.ndarray = None, iteraciones: int = 1) -> np.ndarray:
        """Aplica cierre (dilatación seguida de erosión)."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel, iterations=iteraciones)
    
    @staticmethod
    def gradiente_morfologico(imagen: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
        """Calcula gradiente morfológico (diferencia entre dilatación y erosión)."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(imagen, cv2.MORPH_GRADIENT, kernel)
    
    @staticmethod
    def top_hat(imagen: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
        """Aplica Top Hat (diferencia entre imagen y apertura)."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(imagen, cv2.MORPH_TOPHAT, kernel)
    
    @staticmethod
    def black_hat(imagen: np.ndarray, kernel: np.ndarray = None) -> np.ndarray:
        """Aplica Black Hat (diferencia entre cierre e imagen)."""
        if kernel is None:
            kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(imagen, cv2.MORPH_BLACKHAT, kernel)
