# Sistema Integrado de Procesamiento Digital de Imágenes

Proyecto completo que integra todas las funcionalidades de procesamiento digital de imágenes desarrolladas durante el curso.

## Características

### Transformadas y Análisis de Frecuencia
- **Transformada de Fourier (FFT)**
  - Espectro de magnitud y fase
  - Filtros pasa bajas, pasa altas, pasa banda
  - Filtros ideal, gaussiano y Butterworth
  - Análisis comparativo de efectos del filtrado

- **Transformada Discreta del Coseno (DCT)**
  - Compresión por bloques 8x8
  - Múltiples niveles de calidad
  - Análisis de pérdida de información (PSNR, MSE, SSIM)

### Procesamiento Básico
- **Análisis de Canales**
  - RGB, HSV, CMY
  - Escala de grises
  - Binarización

- **Ajuste de Brillo**
  - Ecualización de histograma
  - CLAHE (Contrast Limited Adaptive Histogram Equalization)
  - Gamma correction
  - Normalización
  - Realce adaptativo

- **Segmentación**
  - Umbralización global
  - Umbralización adaptativa
  - Otsu
  - K-means
  - Watershed
  - GrabCut

### Procesamiento Avanzado
- **Filtros de Restauración**
  - Media
  - Mediana
  - Gaussiano
  - Bilateral
  - Moda

- **Generación de Ruido**
  - Sal y Pimienta
  - Gaussiano
  - Uniforme
  - Speckle

- **Morfología Matemática**
  - Erosión
  - Dilatación
  - Apertura
  - Clausura
  - Gradiente morfológico
  - Top hat / Black hat

- **Componentes Conexas**
  - Etiquetado
  - Coloreo
  - Análisis de propiedades

### Operaciones
- **Aritméticas**
  - Suma, resta, multiplicación, división con escalares
  - Operaciones entre imágenes
  - Fusión de imágenes

- **Lógicas**
  - AND, OR, XOR, NOT
  - Operaciones bit a bit

## Instalación

1. Clonar o descargar el proyecto
2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```



## Estructura del Proyecto

```
PDI_Proyecto_Completo/
├── main.py                      # Archivo principal
├── config.py                    # Configuración y constantes
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
└── src/
    ├── fourier/                 # Transformadas de Fourier y DCT
    ├── procesamiento_basico/    # Brillo, segmentación, umbralización
    ├── procesamiento_avanzado/  # Filtros, ruido, morfología, componentes
    ├── operaciones/             # Operaciones aritméticas y lógicas
    ├── utilidades/              # Utilidades de carga y manejo de imágenes
    └── interfaces/              # Interfaz gráfica modular
```

## Tecnologías Utilizadas

- **Python 3.x**
- **NumPy**: Operaciones numéricas y matrices
- **OpenCV**: Procesamiento de imágenes
- **Matplotlib**: Visualización y gráficas
- **PIL/Pillow**: Manipulación de imágenes
- **PySide6**: Interfaz gráfica Qt
- **SciPy**: Estadísticas y procesamiento científico

## Características de la Interfaz

- Interfaz gráfica moderna y responsive
- Organización modular por secciones
- Vista previa de resultados en tiempo real
- Comparación lado a lado de imágenes
- Exportación de resultados

