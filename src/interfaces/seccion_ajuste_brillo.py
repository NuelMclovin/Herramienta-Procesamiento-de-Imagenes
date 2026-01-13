"""Sección de ajuste de brillo y contraste."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_ACENTO


class SeccionAjusteBrillo(SeccionBase):
    """Sección para ajuste de brillo, contraste y ecualización."""
    
    def __init__(self, ventana_principal):
        super().__init__("AJUSTE DE BRILLO", COLOR_ACENTO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de ajuste de brillo."""
        self.crear_boton("Corrección Gamma", COLOR_ACENTO, lambda: self.aplicar_brillo("gamma"))
        self.crear_boton("CLAHE", COLOR_ACENTO, lambda: self.aplicar_brillo("clahe"))
        self.crear_boton("Ecualización Uniforme", COLOR_ACENTO, lambda: self.aplicar_brillo("uniforme"))
        self.crear_boton("Ecualización Exponencial", COLOR_ACENTO, lambda: self.aplicar_brillo("exponencial"))
        self.crear_boton("Ecualización Rayleigh", COLOR_ACENTO, lambda: self.aplicar_brillo("rayleigh"))
    
    def aplicar_brillo(self, metodo):
        """Aplica técnicas de ajuste de brillo."""
        nombres = {
            'gamma': 'Corrección Gamma',
            'clahe': 'CLAHE',
            'uniforme': 'Ecualización Uniforme',
            'exponencial': 'Ecualización Exponencial',
            'rayleigh': 'Ecualización Rayleigh'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[metodo]}")
        dialogo.agregar_selector_imagen()
        
        gamma_spin = None
        if metodo == "gamma":
            gamma_spin = dialogo.agregar_spin("Valor Gamma:", 0.1, 5.0, 1.5, 0.1, es_double=True)
        
        info = QLabel(f"Se aplicará {nombres[metodo]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_ACENTO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.procesamiento_basico import AjusteBrillo
            
            try:
                if metodo == "gamma":
                    resultado = AjusteBrillo.correccion_gamma(imagen, gamma_spin.value())
                elif metodo == "clahe":
                    resultado = AjusteBrillo.clahe(imagen)
                elif metodo == "uniforme":
                    resultado = AjusteBrillo.ecualizacion_uniforme(imagen)
                elif metodo == "exponencial":
                    resultado = AjusteBrillo.ecualizacion_exponencial(imagen)
                elif metodo == "rayleigh":
                    resultado = AjusteBrillo.ecualizacion_rayleigh(imagen)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[metodo]} aplicado")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
