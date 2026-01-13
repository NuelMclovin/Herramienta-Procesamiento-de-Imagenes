"""
Módulo de operaciones lógicas
"""

import numpy as np
import cv2


class OperacionesLogicas:
    """Clase para operaciones lógicas bit a bit."""
    
    @staticmethod
    def _asegurar_tipo_compatible(imagen1: np.ndarray, imagen2: np.ndarray = None) -> tuple:
        """
        Asegura que las imágenes tengan el tipo de dato correcto (uint8).
        
        Args:
            imagen1: Primera imagen
            imagen2: Segunda imagen (opcional)
            
        Returns:
            Tupla con las imágenes convertidas a uint8
        """
        # Convertir imagen1 a uint8
        if imagen1.dtype != np.uint8:
            if imagen1.max() <= 1.0:
                # Imagen normalizada [0, 1]
                imagen1 = (imagen1 * 255).astype(np.uint8)
            else:
                # Imagen en otro rango
                imagen1 = np.clip(imagen1, 0, 255).astype(np.uint8)
        
        # Convertir imagen2 si existe
        if imagen2 is not None:
            if imagen2.dtype != np.uint8:
                if imagen2.max() <= 1.0:
                    imagen2 = (imagen2 * 255).astype(np.uint8)
                else:
                    imagen2 = np.clip(imagen2, 0, 255).astype(np.uint8)
            return imagen1, imagen2
        
        return (imagen1,)
    
    @staticmethod
    def operacion_and(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Operación AND bit a bit."""
        imagen1, imagen2 = OperacionesLogicas._asegurar_tipo_compatible(imagen1, imagen2)
        return cv2.bitwise_and(imagen1, imagen2)
    
    @staticmethod
    def operacion_or(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Operación OR bit a bit."""
        imagen1, imagen2 = OperacionesLogicas._asegurar_tipo_compatible(imagen1, imagen2)
        return cv2.bitwise_or(imagen1, imagen2)
    
    @staticmethod
    def operacion_xor(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Operación XOR bit a bit."""
        imagen1, imagen2 = OperacionesLogicas._asegurar_tipo_compatible(imagen1, imagen2)
        return cv2.bitwise_xor(imagen1, imagen2)
    
    @staticmethod
    def operacion_not(imagen: np.ndarray) -> np.ndarray:
        """Operación NOT bit a bit."""
        imagen, = OperacionesLogicas._asegurar_tipo_compatible(imagen)
        return cv2.bitwise_not(imagen)
    
    # Alias para compatibilidad con la interfaz
    @staticmethod
    def AND(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Operación AND (alias)."""
        return OperacionesLogicas.operacion_and(imagen1, imagen2)
    
    @staticmethod
    def OR(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Operación OR (alias)."""
        return OperacionesLogicas.operacion_or(imagen1, imagen2)
    
    @staticmethod
    def XOR(imagen1: np.ndarray, imagen2: np.ndarray) -> np.ndarray:
        """Operación XOR (alias)."""
        return OperacionesLogicas.operacion_xor(imagen1, imagen2)
    
    @staticmethod
    def NOT(imagen: np.ndarray) -> np.ndarray:
        """Operación NOT (alias)."""
        return OperacionesLogicas.operacion_not(imagen)
