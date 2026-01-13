"""
Módulo de análisis de componentes conexas
"""

import cv2
import numpy as np
from typing import Tuple, List, Dict


class ComponentesConexas:
    """Clase para análisis de componentes conexas."""
    
    @staticmethod
    def etiquetar_componentes(bin_img: np.ndarray, connectivity: int = 8) -> Tuple:
        """
        Etiqueta componentes conexas.
        
        Returns:
            num_labels, labels, stats, centroids
        """
        if bin_img.dtype != np.uint8:
            bin_img = bin_img.astype(np.uint8)
        
        return cv2.connectedComponentsWithStats(bin_img, connectivity=connectivity)
    
    @staticmethod
    def colorear_componentes(labels: np.ndarray) -> np.ndarray:
        """Colorea cada componente con un color diferente."""
        label_hue = np.uint8(179 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue == 0] = 0
        return labeled_img
    
    @staticmethod
    def obtener_estadisticas_componentes(labels: np.ndarray) -> List[Dict]:
        """Calcula estadísticas de cada componente."""
        estadisticas = []
        
        for lab in range(1, labels.max() + 1):
            mask = (labels == lab).astype(np.uint8)
            area = np.sum(mask)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            perimetro = cv2.arcLength(contours[0], True) if contours else 0
            
            M = cv2.moments(mask)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            
            if contours:
                x, y, w, h = cv2.boundingRect(contours[0])
                aspect_ratio = float(w) / h if h > 0 else 0
            else:
                x, y, w, h = 0, 0, 0, 0
                aspect_ratio = 0
            
            circularidad = (4 * np.pi * area) / (perimetro ** 2) if perimetro > 0 else 0
            
            estadisticas.append({
                'etiqueta': lab,
                'area': area,
                'perimetro': perimetro,
                'centroide': (cx, cy),
                'bbox': (x, y, w, h),
                'aspect_ratio': aspect_ratio,
                'circularidad': circularidad
            })
        
        return estadisticas
    
    @staticmethod
    def filtrar_componentes_pequenas(labels: np.ndarray, area_minima: int) -> Tuple[np.ndarray, int]:
        """Filtra componentes con área menor al umbral."""
        labels_filtradas = labels.copy()
        componentes_eliminadas = 0
        
        for lab in range(1, labels.max() + 1):
            area = np.sum(labels == lab)
            if area < area_minima:
                labels_filtradas[labels == lab] = 0
                componentes_eliminadas += 1
        
        labels_unicas = np.unique(labels_filtradas)
        labels_nuevas = np.zeros_like(labels_filtradas)
        
        for idx, lab in enumerate(labels_unicas):
            if lab != 0:
                labels_nuevas[labels_filtradas == lab] = idx
        
        return labels_nuevas, componentes_eliminadas
