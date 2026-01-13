"""Sección de generación de ruido."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_ERROR


class SeccionRuido(SeccionBase):
    """Sección para generación de ruido."""
    
    def __init__(self, ventana_principal):
        super().__init__("GENERACIÓN DE RUIDO", COLOR_ERROR, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de ruido."""
        self.crear_boton("Ruido Sal", COLOR_ERROR, lambda: self.aplicar_ruido("sal"))
        self.crear_boton("Ruido Pimienta", COLOR_ERROR, lambda: self.aplicar_ruido("pimienta"))
        self.crear_boton("Ruido Gaussiano", COLOR_ERROR, lambda: self.aplicar_ruido("gaussiano"))
    
    def aplicar_ruido(self, tipo):
        """Aplica ruido a la imagen."""
        nombres = {
            'sal': 'Ruido Sal',
            'pimienta': 'Ruido Pimienta',
            'gaussiano': 'Ruido Gaussiano'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[tipo]}")
        dialogo.agregar_selector_imagen()
        
        if tipo in ["sal", "pimienta"]:
            param_spin = dialogo.agregar_spin("Probabilidad:", 0.01, 0.3, 0.05, 0.01, es_double=True)
        elif tipo == "gaussiano":
            param_spin = dialogo.agregar_spin("Desviación estándar:", 1, 50, 10, 1)
        
        info = QLabel(f"Se aplicará {nombres[tipo]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_ERROR}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.procesamiento_avanzado import GeneradorRuido
            
            try:
                param = param_spin.value()
                
                if tipo == "sal":
                    resultado = GeneradorRuido.agregar_ruido_sal(imagen, param)
                elif tipo == "pimienta":
                    resultado = GeneradorRuido.agregar_ruido_pimienta(imagen, param)
                elif tipo == "gaussiano":
                    resultado = GeneradorRuido.agregar_ruido_gaussiano(imagen, 0, param)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[tipo]} aplicado")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
