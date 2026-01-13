"""Sección de segmentación de imágenes."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_EXITO


class SeccionSegmentacion(SeccionBase):
    """Sección para técnicas de segmentación."""
    
    def __init__(self, ventana_principal):
        super().__init__("SEGMENTACIÓN", COLOR_EXITO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de segmentación."""
        self.crear_boton("Otsu", COLOR_EXITO, lambda: self.aplicar_segmentacion("otsu"))
        self.crear_boton("Kapur", COLOR_EXITO, lambda: self.aplicar_segmentacion("kapur"))
        self.crear_boton("Media", COLOR_EXITO, lambda: self.aplicar_segmentacion("media"))
        self.crear_boton("K-Means", COLOR_EXITO, lambda: self.aplicar_segmentacion("kmeans"))
    
    def aplicar_segmentacion(self, metodo):
        """Aplica técnicas de segmentación."""
        nombres = {
            'otsu': 'Segmentación Otsu',
            'kapur': 'Segmentación Kapur',
            'media': 'Segmentación Media',
            'kmeans': 'K-Means'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[metodo]}")
        dialogo.agregar_selector_imagen()
        
        k_spin = None
        if metodo == "kmeans":
            k_spin = dialogo.agregar_spin("Número de clusters (K):", 2, 10, 3, 1)
        
        info = QLabel(f"Se aplicará {nombres[metodo]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_EXITO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.procesamiento_basico import Segmentacion
            
            try:
                if metodo == "otsu":
                    resultado, _ = Segmentacion.segmentacion_otsu(imagen)
                elif metodo == "kapur":
                    resultado, _ = Segmentacion.segmentacion_kapur(imagen)
                elif metodo == "media":
                    resultado, _ = Segmentacion.segmentacion_media(imagen)
                elif metodo == "kmeans":
                    k = k_spin.value()
                    resultado = Segmentacion.segmentacion_kmeans(imagen, k)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[metodo]} aplicado")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
