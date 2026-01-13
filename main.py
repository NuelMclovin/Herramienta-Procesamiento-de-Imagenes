"""
Sistema Integrado de Procesamiento Digital de Imágenes
Proyecto Completo - PDI

Este proyecto unifica todas las funcionalidades de procesamiento de imágenes:
- Transformada de Fourier y DCT
- Operaciones aritméticas y lógicas
- Generación y filtrado de ruido
- Ajuste de brillo y segmentación
- Análisis de componentes conexas
- Morfología matemática
- Análisis de canales RGB, HSV, CMY
- Histogramas y propiedades estadísticas
"""

import sys
from PySide6.QtWidgets import QApplication
from src.interfaces.interfaz_principal import VentanaPrincipal


def main():
    """Función principal que inicia la aplicación."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    ventana = VentanaPrincipal()
    ventana.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
