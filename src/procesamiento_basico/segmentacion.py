"""
Módulo de segmentación de imágenes
"""

import cv2
import numpy as np
from typing import Tuple
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d


class Segmentacion:
    """
    Clase para aplicar técnicas de segmentación de imágenes.
    """
    
    @staticmethod
    def _convertir_a_gris(imagen: np.ndarray) -> np.ndarray:
        """Convierte imagen a escala de grises si es necesario."""
        if len(imagen.shape) == 3:
            return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        return imagen
    
    @staticmethod
    def segmentacion_otsu(imagen: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Aplica segmentación por método de Otsu.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Tupla (imagen_segmentada, umbral_utilizado)
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        umbral, imagen_segmentada = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return imagen_segmentada, float(umbral)
    
    @staticmethod
    def _entropia_kapur(histograma: np.ndarray, total_pixeles: int) -> int:
        """
        Calcula el umbral óptimo usando entropía de Kapur.
        
        Args:
            histograma: Histograma de la imagen
            total_pixeles: Total de píxeles
            
        Returns:
            Umbral óptimo
        """
        max_entropia = -1
        umbral_optimo = 0
        
        prob = histograma / total_pixeles
        
        for t in range(1, 255):
            w0 = np.sum(prob[:t])
            w1 = np.sum(prob[t:])
            
            if w0 == 0 or w1 == 0:
                continue
            
            h0 = 0
            for i in range(t):
                if prob[i] > 0:
                    p_i_w0 = prob[i] / w0
                    h0 -= p_i_w0 * np.log(p_i_w0)
            
            h1 = 0
            for i in range(t, 256):
                if prob[i] > 0:
                    p_i_w1 = prob[i] / w1
                    h1 -= p_i_w1 * np.log(p_i_w1)
            
            entropia_total = h0 + h1
            
            if entropia_total > max_entropia:
                max_entropia = entropia_total
                umbral_optimo = t
        
        return umbral_optimo
    
    @staticmethod
    def segmentacion_kapur(imagen: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Aplica segmentación por técnica de entropía de Kapur.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Tupla (imagen_segmentada, umbral_utilizado)
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        
        histograma, _ = np.histogram(imagen, bins=256, range=(0, 256))
        total_pixeles = imagen.size
        
        umbral = Segmentacion._entropia_kapur(histograma, total_pixeles)
        imagen_segmentada = (imagen > umbral).astype(np.uint8) * 255
        
        return imagen_segmentada, float(umbral)
    
    @staticmethod
    def segmentacion_minimo_histograma(imagen: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Aplica segmentación por método del mínimo del histograma.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Tupla (imagen_segmentada, umbral_utilizado)
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        
        histograma, _ = np.histogram(imagen, bins=256, range=(0, 256))
        histograma_suavizado = gaussian_filter1d(histograma.astype(float), sigma=2)
        
        picos, propiedades = find_peaks(histograma_suavizado, prominence=np.max(histograma_suavizado)*0.1)
        
        if len(picos) >= 2:
            prominencias = propiedades['prominences']
            indices_ordenados = np.argsort(prominencias)[::-1]
            dos_picos_principales = np.sort(picos[indices_ordenados[:2]])
            
            region = histograma_suavizado[dos_picos_principales[0]:dos_picos_principales[1]+1]
            minimo = np.argmin(region) + dos_picos_principales[0]
        else:
            minimo, _ = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            minimo = int(minimo)
        
        imagen_segmentada = (imagen > minimo).astype(np.uint8) * 255
        
        return imagen_segmentada, float(minimo)
    
    @staticmethod
    def segmentacion_media(imagen: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Aplica segmentación por umbral de media.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Tupla (imagen_segmentada, umbral_utilizado)
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        
        umbral = np.mean(imagen)
        imagen_segmentada = (imagen >= umbral).astype(np.uint8) * 255
        
        return imagen_segmentada, float(umbral)
    
    @staticmethod
    def segmentacion_multiples_umbrales(imagen: np.ndarray, T1: int, T2: int) -> np.ndarray:
        """
        Aplica segmentación por múltiples umbrales.
        
        Args:
            imagen: Imagen de entrada
            T1: Primer umbral
            T2: Segundo umbral
            
        Returns:
            Imagen segmentada con tres niveles
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        
        imagen_segmentada = np.zeros_like(imagen)
        imagen_segmentada[imagen < T1] = 0
        imagen_segmentada[(imagen >= T1) & (imagen < T2)] = 127
        imagen_segmentada[imagen >= T2] = 255
        
        return imagen_segmentada
    
    @staticmethod
    def segmentacion_umbral_banda(imagen: np.ndarray, T1: int, T2: int) -> np.ndarray:
        """
        Aplica segmentación por umbral banda.
        
        Args:
            imagen: Imagen de entrada
            T1: Umbral inferior
            T2: Umbral superior
            
        Returns:
            Imagen segmentada (binaria)
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        
        imagen_segmentada = np.zeros_like(imagen)
        imagen_segmentada[(imagen >= T1) & (imagen <= T2)] = 255
        
        return imagen_segmentada
    
    @staticmethod
    def segmentacion_kmeans(imagen: np.ndarray, k: int = 3) -> np.ndarray:
        """
        Aplica segmentación usando K-means.
        
        Args:
            imagen: Imagen de entrada
            k: Número de clusters
            
        Returns:
            Imagen segmentada
        """
        imagen = Segmentacion._convertir_a_gris(imagen)
        
        pixel_values = imagen.reshape((-1, 1))
        pixel_values = np.float32(pixel_values)
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        centers = np.uint8(centers)
        segmented_image = centers[labels.flatten()]
        segmented_image = segmented_image.reshape(imagen.shape)
        
        return segmented_image
    
    @staticmethod
    def segmentacion_watershed(imagen: np.ndarray) -> np.ndarray:
        """
        Aplica segmentación usando Watershed.
        
        Args:
            imagen: Imagen de entrada
            
        Returns:
            Imagen segmentada
        """
        if len(imagen.shape) == 2:
            imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)
        
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        
        markers = cv2.watershed(imagen, markers)
        imagen[markers == -1] = [255, 0, 0]
        
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
