"""
Archivo de configuración y constantes del proyecto.
Contiene todas las constantes globales y configuraciones.
"""

# Tamaño de referencia para las imágenes
TAMANO_REFERENCIA = (512, 512)

# Configuración de umbral para binarización
UMBRAL_DEFAULT = 127

# Configuración de ruido
RUIDO_SAL_PIMIENTA_DEFAULT = 0.02
RUIDO_GAUSSIANO_MEDIA_DEFAULT = 0
RUIDO_GAUSSIANO_SIGMA_DEFAULT = 20

# Configuración de filtros
KERNEL_SIZE_DEFAULT = 5
FILTRO_BILATERAL_D = 9
FILTRO_BILATERAL_SIGMA_COLOR = 75
FILTRO_BILATERAL_SIGMA_SPACE = 75
FILTRO_GAUSSIANO_SIGMA = 1.0

# Configuración de Fourier
FOURIER_FILTRO_CUTOFF_DEFAULT = 0.2
FOURIER_FILTRO_ORDEN_DEFAULT = 2

# Configuración de DCT
DCT_Q_FACTOR_DEFAULT = 0.5
DCT_BLOCK_SIZE = 8

# Conectividad para componentes conexas
CONECTIVIDAD_DEFAULT = 8

# Colores de interfaz - Paleta Profesional
COLOR_FONDO = "#1E1E1E"           # Fondo principal - gris oscuro
COLOR_PRIMARIO = "#4A90E2"        # Azul profesional
COLOR_SECUNDARIO = "#5C6BC0"      # Índigo suave
COLOR_TERCIARIO = "#7986CB"       # Azul lavanda
COLOR_ACENTO = "#42A5F5"          # Azul claro
COLOR_EXITO = "#66BB6A"           # Verde suave
COLOR_ERROR = "#E57373"           # Rojo suave
COLOR_PELIGRO = "#EF5350"         # Rojo intenso
COLOR_ADVERTENCIA = "#FFA726"     # Naranja suave
COLOR_INFO = "#29B6F6"            # Cyan profesional
COLOR_OSCURO = "#252526"          # Gris muy oscuro
COLOR_CLARO = "#E0E0E0"           # Gris claro
COLOR_CARD = "#2D2D30"            # Gris medio oscuro
COLOR_BORDER = "#3E3E42"          # Gris borde
COLOR_TEXT_PRIMARY = "#FFFFFF"    # Blanco puro
COLOR_TEXT_SECONDARY = "#A8B2D1"
COLOR_HOVER = "#7C3AED"
COLOR_SHADOW = "rgba(102, 126, 234, 0.4)"

# Formatos de imagen soportados
FORMATOS_IMAGEN = [
    "Imágenes (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)",
    "PNG (*.png)",
    "JPEG (*.jpg *.jpeg)",
    "BMP (*.bmp)",
    "TIFF (*.tiff *.tif)",
    "Todos los archivos (*.*)"
]
