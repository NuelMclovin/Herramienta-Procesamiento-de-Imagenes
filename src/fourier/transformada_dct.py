"""
Módulo de Transformada Discreta del Coseno (DCT)
Implementa compresión por bloques y análisis de calidad
"""

import numpy as np
import math
from typing import Tuple, Dict


class TransformadaDCT:
    """
    Clase para aplicar la Transformada Discreta del Coseno y compresión de imágenes.
    """
    
    # Tabla de cuantización JPEG estándar
    Q_JPEG = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=np.float64)
    
    def __init__(self, block_size: int = 8):
        """
        Inicializa la clase de DCT.
        
        Args:
            block_size: Tamaño del bloque para DCT (típicamente 8)
        """
        self.block_size = block_size
        self.C = self._crear_matriz_dct(block_size)
    
    def _crear_matriz_dct(self, N: int = 8) -> np.ndarray:
        """
        Genera matriz DCT tipo II ortogonal.
        
        Args:
            N: Tamaño de la matriz
            
        Returns:
            Matriz DCT NxN
        """
        C = np.zeros((N, N), dtype=np.float64)
        for k in range(N):
            alpha = np.sqrt(1/N) if k == 0 else np.sqrt(2/N)
            for n in range(N):
                C[k, n] = alpha * np.cos((2*n + 1) * k * np.pi / (2*N))
        return C
    
    def dct_bloque_2d(self, bloque: np.ndarray) -> np.ndarray:
        """
        Aplica DCT 2D a un bloque: D = C * bloque * C^T
        
        Args:
            bloque: Bloque de imagen
            
        Returns:
            Coeficientes DCT del bloque
        """
        return self.C @ bloque @ self.C.T
    
    def idct_bloque_2d(self, coef_dct: np.ndarray) -> np.ndarray:
        """
        Aplica IDCT 2D a coeficientes: bloque = C^T * coef_dct * C
        
        Args:
            coef_dct: Coeficientes DCT
            
        Returns:
            Bloque reconstruido
        """
        return self.C.T @ coef_dct @ self.C
    
    def pad_multiplo(self, img: np.ndarray, N: int = 8) -> Tuple[np.ndarray, int, int]:
        """
        Rellena imagen a múltiplo de N.
        
        Args:
            img: Imagen original
            N: Tamaño del bloque
            
        Returns:
            padded: Imagen rellenada
            h: Altura original
            w: Ancho original
        """
        h, w = img.shape
        nh = ((h + N - 1) // N) * N
        nw = ((w + N - 1) // N) * N
        padded = np.zeros((nh, nw), dtype=img.dtype)
        padded[:h, :w] = img
        return padded, h, w
    
    def comprimir_dct(self, img: np.ndarray, q_factor: float = 0.5) -> Tuple[np.ndarray, Dict]:
        """
        Compresión DCT por bloques.
        
        Args:
            img: Imagen en escala de grises normalizada [0,1]
            q_factor: Factor de calidad (0.1-2.0, menor = más compresión/pérdida)
            
        Returns:
            recon: Imagen reconstruida
            metricas: Diccionario con métricas de calidad
        """
        padded, h, w = self.pad_multiplo(img, self.block_size)
        H, W = padded.shape
        Q = self.Q_JPEG * q_factor
        
        coef_total = 0
        coef_no_cero = 0
        recon = np.zeros_like(padded, dtype=np.float64)
        
        for i in range(0, H, self.block_size):
            for j in range(0, W, self.block_size):
                # Extraer bloque y centrar
                bloque = padded[i:i+self.block_size, j:j+self.block_size] - 0.5
                
                # DCT
                coef_dct = self.dct_bloque_2d(bloque)
                
                # Cuantización
                coef_cuant = np.round(coef_dct / Q) * Q
                
                # Contar coeficientes
                coef_total += coef_cuant.size
                coef_no_cero += np.count_nonzero(coef_cuant)
                
                # IDCT
                bloque_recon = self.idct_bloque_2d(coef_cuant)
                recon[i:i+self.block_size, j:j+self.block_size] = bloque_recon + 0.5
        
        # Recortar al tamaño original
        recon = np.clip(recon[:h, :w], 0, 1)
        
        # Calcular métricas
        mse = np.mean((img - recon)**2)
        psnr = 20 * math.log10(1.0) - 10 * math.log10(mse) if mse > 0 else float('inf')
        tasa_compresion = coef_no_cero / coef_total
        ssim = self.calcular_ssim(img, recon)
        
        metricas = {
            'mse': mse,
            'psnr': psnr,
            'tasa_retencion': tasa_compresion,
            'ssim': ssim,
            'q_factor': q_factor
        }
        
        return recon, metricas
    
    def calcular_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """
        Calcula SSIM (Structural Similarity Index) aproximado.
        
        Args:
            img1: Primera imagen
            img2: Segunda imagen
            
        Returns:
            Valor SSIM entre 0 y 1
        """
        C1 = (0.01)**2
        C2 = (0.03)**2
        
        mu1 = np.mean(img1)
        mu2 = np.mean(img2)
        sigma1 = np.std(img1)
        sigma2 = np.std(img2)
        sigma12 = np.mean((img1 - mu1) * (img2 - mu2))
        
        ssim = ((2*mu1*mu2 + C1) * (2*sigma12 + C2)) / \
               ((mu1**2 + mu2**2 + C1) * (sigma1**2 + sigma2**2 + C2))
        
        return float(ssim)
    
    def analizar_bloque(self, img: np.ndarray, pos_i: int = 0, pos_j: int = 0) -> Dict:
        """
        Analiza un bloque específico de la imagen.
        
        Args:
            img: Imagen
            pos_i: Posición fila del bloque
            pos_j: Posición columna del bloque
            
        Returns:
            Diccionario con información del bloque
        """
        padded, h, w = self.pad_multiplo(img, self.block_size)
        
        # Validar posiciones
        pos_i = min(pos_i, padded.shape[0] - self.block_size)
        pos_j = min(pos_j, padded.shape[1] - self.block_size)
        
        # Extraer bloque
        bloque = padded[pos_i:pos_i+self.block_size, pos_j:pos_j+self.block_size] - 0.5
        coef_dct = self.dct_bloque_2d(bloque)
        
        return {
            'bloque_original': bloque + 0.5,
            'coeficientes_dct': coef_dct,
            'coef_dc': coef_dct[0, 0],
            'energia_ac': np.sum(np.abs(coef_dct[1:, :])) + np.sum(np.abs(coef_dct[0, 1:])),
            'posicion': (pos_i, pos_j)
        }
    
    def comparar_calidades(self, img: np.ndarray, q_factors: list = None) -> Dict:
        """
        Compara múltiples niveles de calidad.
        
        Args:
            img: Imagen original
            q_factors: Lista de factores de calidad a probar
            
        Returns:
            Diccionario con resultados para cada factor
        """
        if q_factors is None:
            q_factors = [0.1, 0.2, 0.5, 1.0, 2.0]
        
        resultados = {}
        
        for q in q_factors:
            recon, metricas = self.comprimir_dct(img, q_factor=q)
            resultados[q] = {
                'imagen_reconstruida': recon,
                'metricas': metricas
            }
        
        return resultados
