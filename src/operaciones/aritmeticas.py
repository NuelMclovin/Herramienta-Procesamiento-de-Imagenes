"""
Módulo de operaciones aritméticas
"""

import numpy as np
import cv2


class OperacionesAritmeticas:
    """Clase para operaciones aritméticas con imágenes."""
    
    @staticmethod
    def suma_escalar(imagen: np.ndarray, escalar: float) -> np.ndarray:
        """Suma un escalar a cada píxel."""
        resultado = imagen.astype(np.float32) + escalar
        return np.clip(resultado, 0, 255).astype(np.uint8)
    
    @staticmethod
    def resta_escalar(imagen: np.ndarray, escalar: float) -> np.ndarray:
        """Resta un escalar de cada píxel."""
        resultado = imagen.astype(np.float32) - escalar
        return np.clip(resultado, 0, 255).astype(np.uint8)
    
    @staticmethod
    def multiplicacion_escalar(imagen: np.ndarray, escalar: float) -> np.ndarray:
        """Multiplica cada píxel por un escalar."""
        resultado = imagen.astype(np.float32) * escalar
        return np.clip(resultado, 0, 255).astype(np.uint8)
    
    @staticmethod
    def division_escalar(imagen: np.ndarray, escalar: float) -> np.ndarray:
        """Divide cada píxel por un escalar."""
        if escalar == 0:
            return imagen
        resultado = imagen.astype(np.float32) / escalar
        return np.clip(resultado, 0, 255).astype(np.uint8)
    
    @staticmethod
    def suma_imagenes(imagen1: np.ndarray, imagen2: np.ndarray, peso1: float = 0.5, peso2: float = 0.5) -> np.ndarray:
        """Suma ponderada de dos imágenes."""
        return cv2.addWeighted(imagen1, peso1, imagen2, peso2, 0)
    
    @staticmethod
    def resta_imagenes(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Resta dos imágenes."""
        return cv2.subtract(imagen1, imagen2)
    
    @staticmethod
    def multiplicacion_imagenes(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Multiplica dos imágenes."""
        resultado = imagen1.astype(np.float32) * imagen2.astype(np.float32) / 255.0
        return np.clip(resultado, 0, 255).astype(np.uint8)
    
    @staticmethod
    def division_imagenes(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Divide dos imágenes."""
        imagen2_safe = np.where(imagen2 == 0, 1, imagen2)
        resultado = (imagen1.astype(np.float32) / imagen2_safe.astype(np.float32)) * 255
        return np.clip(resultado, 0, 255).astype(np.uint8)
    
    @staticmethod
    def fusion_imagenes(imagen1: np.ndarray, imagen2: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """Fusión de dos imágenes con transparencia."""
        return cv2.addWeighted(imagen1, alpha, imagen2, 1 - alpha, 0)
    
    # Alias para compatibilidad con la interfaz
    @staticmethod
    def suma(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Suma dos imágenes (alias)."""
        return cv2.add(imagen1, imagen2)
    
    @staticmethod
    def resta(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Resta dos imágenes (alias)."""
        return OperacionesAritmeticas.resta_imagenes(imagen1, imagen2)
    
    @staticmethod
    def multiplicacion(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Multiplica dos imágenes (alias)."""
        return OperacionesAritmeticas.multiplicacion_imagenes(imagen1, imagen2)
    
    @staticmethod
    def division(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Divide dos imágenes (alias)."""
        return OperacionesAritmeticas.division_imagenes(imagen1, imagen2)
