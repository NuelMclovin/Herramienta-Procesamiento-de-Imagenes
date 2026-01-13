"""
Módulo de Transformada de Fourier
Implementa FFT 2D y filtros en dominio de frecuencia
"""

import numpy as np
from typing import Tuple, Dict, Union


class TransformadaFourier:
    """
    Clase para aplicar la Transformada de Fourier y filtros en dominio de frecuencia.
    """
    
    def __init__(self):
        """Inicializa la clase de Transformada de Fourier."""
        self.ultima_fft = None
        self.ultima_magnitud = None
        self.ultima_fase = None
    
    def fft2_imagen(self, img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Calcula FFT 2D y retorna componentes.
        
        Args:
            img: Imagen en escala de grises normalizada [0,1]
            
        Returns:
            F: FFT 2D sin shift
            Fshift: FFT 2D con shift (centro en frecuencia 0)
            magnitud: Magnitud del espectro
            magnitud_log: Magnitud en escala logarítmica
            fase: Fase del espectro
        """
        F = np.fft.fft2(img)
        Fshift = np.fft.fftshift(F)
        magnitud = np.abs(Fshift)
        magnitud_log = np.log(1 + magnitud)
        fase = np.angle(Fshift)
        
        # Guardar para uso posterior
        self.ultima_fft = Fshift
        self.ultima_magnitud = magnitud
        self.ultima_fase = fase
        
        return F, Fshift, magnitud, magnitud_log, fase
    
    def crear_mascara_filtro(self, shape: Tuple[int, int], filtro: str = 'butterworth', 
                            tipo: str = 'lowpass', cutoff: Union[float, Tuple[float, float]] = 0.2, 
                            orden: int = 2) -> np.ndarray:
        """
        Crea máscara de filtro en dominio de frecuencia.
        
        Args:
            shape: Forma de la imagen (filas, columnas)
            filtro: Tipo de filtro - 'ideal', 'gaussiano', 'butterworth'
            tipo: Tipo de operación - 'lowpass', 'highpass', 'bandpass', 'bandstop'
            cutoff: Radio de corte (0-0.5), para bandpass/bandstop es (inner, outer)
            orden: Orden para Butterworth
            
        Returns:
            Máscara del filtro como array 2D
        """
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2
        Y, X = np.ogrid[:rows, :cols]
        D = np.sqrt((Y - crow)**2 + (X - ccol)**2)
        Dnorm = D / float(min(crow, ccol))
        
        # Crear filtro pasa bajas base
        if filtro == 'ideal':
            H = (Dnorm <= cutoff).astype(np.float32)
        elif filtro == 'gaussiano':
            H = np.exp(-(Dnorm**2) / (2 * (cutoff**2)))
        elif filtro == 'butterworth':
            H = 1 / (1 + (Dnorm / (cutoff + 1e-8))**(2 * orden))
        else:
            raise ValueError(f'Filtro desconocido: {filtro}')
        
        # Modificar según tipo
        if tipo == 'lowpass':
            mask = H
        elif tipo == 'highpass':
            mask = 1 - H
        elif tipo == 'bandpass':
            if isinstance(cutoff, tuple):
                inner_cutoff, outer_cutoff = cutoff
            else:
                inner_cutoff, outer_cutoff = cutoff * 0.5, cutoff * 1.5
            
            if filtro == 'butterworth':
                H_inner = 1 / (1 + (Dnorm / (inner_cutoff + 1e-8))**(2 * orden))
                H_outer = 1 / (1 + (Dnorm / (outer_cutoff + 1e-8))**(2 * orden))
            else:
                if filtro == 'ideal':
                    H_inner = (Dnorm <= inner_cutoff).astype(np.float32)
                    H_outer = (Dnorm <= outer_cutoff).astype(np.float32)
                else:  # gaussiano
                    H_inner = np.exp(-(Dnorm**2) / (2 * (inner_cutoff**2)))
                    H_outer = np.exp(-(Dnorm**2) / (2 * (outer_cutoff**2)))
            
            mask = H_outer - H_inner
        elif tipo == 'bandstop':
            if isinstance(cutoff, tuple):
                inner_cutoff, outer_cutoff = cutoff
            else:
                inner_cutoff, outer_cutoff = cutoff * 0.5, cutoff * 1.5
            
            if filtro == 'butterworth':
                H_inner = 1 / (1 + (Dnorm / (inner_cutoff + 1e-8))**(2 * orden))
                H_outer = 1 / (1 + (Dnorm / (outer_cutoff + 1e-8))**(2 * orden))
            else:
                if filtro == 'ideal':
                    H_inner = (Dnorm <= inner_cutoff).astype(np.float32)
                    H_outer = (Dnorm <= outer_cutoff).astype(np.float32)
                else:  # gaussiano
                    H_inner = np.exp(-(Dnorm**2) / (2 * (inner_cutoff**2)))
                    H_outer = np.exp(-(Dnorm**2) / (2 * (outer_cutoff**2)))
            
            mask = 1 - (H_outer - H_inner)
        else:
            raise ValueError(f'Tipo desconocido: {tipo}')
        
        return mask.astype(np.float32)
    
    def aplicar_filtro_frecuencia(self, img: np.ndarray, filtro: str = 'butterworth', 
                                  tipo: str = 'lowpass', cutoff: Union[float, Tuple[float, float]] = 0.2, 
                                  orden: int = 2) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Aplica filtro en dominio de frecuencia y reconstruye imagen.
        
        Args:
            img: Imagen en escala de grises normalizada [0,1]
            filtro: Tipo de filtro
            tipo: Tipo de operación
            cutoff: Radio de corte
            orden: Orden para Butterworth
            
        Returns:
            g: Imagen filtrada
            mask: Máscara del filtro aplicado
            Gshift: Espectro filtrado
        """
        F = np.fft.fft2(img)
        Fshift = np.fft.fftshift(F)
        mask = self.crear_mascara_filtro(img.shape, filtro=filtro, tipo=tipo, cutoff=cutoff, orden=orden)
        Gshift = Fshift * mask
        G = np.fft.ifftshift(Gshift)
        g = np.fft.ifft2(G)
        g = np.real(g)
        g = np.clip(g, 0, 1)
        
        return g, mask, Gshift
    
    def reconstruir_desde_magnitud_fase(self, magnitud: np.ndarray, fase: np.ndarray) -> np.ndarray:
        """
        Reconstruye imagen desde magnitud y fase.
        
        Args:
            magnitud: Magnitud del espectro
            fase: Fase del espectro
            
        Returns:
            Imagen reconstruida
        """
        Fshift = magnitud * np.exp(1j * fase)
        F = np.fft.ifftshift(Fshift)
        img = np.fft.ifft2(F)
        img = np.real(img)
        img = np.clip(img, 0, 1)
        
        return img
    
    def calcular_perfil_radial(self, espectro: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula el perfil radial del espectro.
        
        Args:
            espectro: Espectro de frecuencia (magnitud)
            
        Returns:
            radios: Array de radios
            perfil: Valores promedio del espectro para cada radio
        """
        rows, cols = espectro.shape
        crow, ccol = rows // 2, cols // 2
        Y, X = np.ogrid[:rows, :cols]
        D = np.sqrt((Y - crow)**2 + (X - ccol)**2).astype(int)
        
        max_radio = int(np.sqrt(crow**2 + ccol**2))
        radios = np.arange(0, max_radio)
        perfil = np.zeros(max_radio)
        
        for r in radios:
            mask = (D == r)
            if np.sum(mask) > 0:
                perfil[r] = np.mean(espectro[mask])
        
        return radios, perfil
    
    def obtener_estadisticas(self, img: np.ndarray) -> Dict[str, float]:
        """
        Calcula estadísticas básicas del espectro.
        
        Args:
            img: Imagen en escala de grises
            
        Returns:
            Diccionario con estadísticas
        """
        _, _, magnitud, magnitud_log, fase = self.fft2_imagen(img)
        
        return {
            'mag_min': float(magnitud.min()),
            'mag_max': float(magnitud.max()),
            'mag_mean': float(magnitud.mean()),
            'mag_std': float(magnitud.std()),
            'fase_min': float(fase.min()),
            'fase_max': float(fase.max()),
            'fase_mean': float(fase.mean()),
            'fase_std': float(fase.std())
        }
