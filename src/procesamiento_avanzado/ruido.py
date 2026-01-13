"""
Módulo para generación de ruido
"""

import numpy as np


class GeneradorRuido:
    """Clase para agregar diferentes tipos de ruido a imágenes."""
    
    @staticmethod
    def agregar_ruido_sal(imagen: np.ndarray, cantidad: float = 0.02) -> np.ndarray:
        """Agrega ruido sal (píxeles blancos)."""
        resultado = imagen.copy()
        num_pixeles = int(cantidad * imagen.size)
        
        coords_sal = [np.random.randint(0, i, num_pixeles) for i in imagen.shape[:2]]
        resultado[coords_sal[0], coords_sal[1]] = 255
        
        return resultado
    
    @staticmethod
    def agregar_ruido_pimienta(imagen: np.ndarray, cantidad: float = 0.02) -> np.ndarray:
        """Agrega ruido pimienta (píxeles negros)."""
        resultado = imagen.copy()
        num_pixeles = int(cantidad * imagen.size)
        
        coords_pimienta = [np.random.randint(0, i, num_pixeles) for i in imagen.shape[:2]]
        resultado[coords_pimienta[0], coords_pimienta[1]] = 0
        
        return resultado
    
    @staticmethod
    def agregar_ruido_gaussiano(imagen: np.ndarray, media: float = 0, sigma: float = 20) -> np.ndarray:
        """Agrega ruido gaussiano."""
        resultado = imagen.copy().astype(np.float32)
        ruido = np.random.normal(media, sigma, imagen.shape).astype(np.float32)
        resultado = resultado + ruido
        resultado = np.clip(resultado, 0, 255)
        return resultado.astype(np.uint8)
    
    @staticmethod
    def agregar_ruido_speckle(imagen: np.ndarray, cantidad: float = 0.1) -> np.ndarray:
        """Agrega ruido speckle (multiplicativo)."""
        resultado = imagen.copy().astype(np.float32)
        ruido = np.random.randn(*imagen.shape) * cantidad
        resultado = resultado + resultado * ruido
        resultado = np.clip(resultado, 0, 255)
        return resultado.astype(np.uint8)
