"""
Módulo de interfaces gráficas
"""

from .interfaz_principal import VentanaPrincipal
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from src.interfaces.histograma_widget import HistogramaWidget, PanelImagenConHistograma
from src.interfaces.seccion_archivo import SeccionArchivo
from src.interfaces.seccion_utilidades import SeccionUtilidades
from src.interfaces.seccion_aritmeticas import SeccionAritmeticas
from src.interfaces.seccion_logicas import SeccionLogicas
from src.interfaces.seccion_ajuste_brillo import SeccionAjusteBrillo
from src.interfaces.seccion_segmentacion import SeccionSegmentacion
from src.interfaces.seccion_morfologia import SeccionMorfologia
from src.interfaces.seccion_filtros import SeccionFiltros
from src.interfaces.seccion_ruido import SeccionRuido
from src.interfaces.seccion_fourier import SeccionFourier
from src.interfaces.seccion_modos_color import SeccionModosColor
from src.interfaces.seccion_componentes_conexas import SeccionComponentesConexas

__all__ = [
    'VentanaPrincipal',
    'SeccionBase',
    'DialogoBase',
    'HistogramaWidget',
    'PanelImagenConHistograma',
    'SeccionArchivo',
    'SeccionUtilidades',
    'SeccionAritmeticas',
    'SeccionLogicas',
    'SeccionAjusteBrillo',
    'SeccionSegmentacion',
    'SeccionMorfologia',
    'SeccionFiltros',
    'SeccionRuido',
    'SeccionFourier',
    'SeccionModosColor',
    'SeccionComponentesConexas'
]
