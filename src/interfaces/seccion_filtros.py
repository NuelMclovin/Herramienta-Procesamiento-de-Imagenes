"""Sección de filtros espaciales."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_INFO


class SeccionFiltros(SeccionBase):
    """Sección para filtros espaciales."""
    
    def __init__(self, ventana_principal):
        super().__init__("FILTROS ESPACIALES", COLOR_INFO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de filtros."""
        self.crear_boton("Filtro Promediador", COLOR_INFO, lambda: self.aplicar_filtro("promediador"))
        self.crear_boton("Filtro Mediana", COLOR_INFO, lambda: self.aplicar_filtro("mediana"))
        self.crear_boton("Filtro Gaussiano", COLOR_INFO, lambda: self.aplicar_filtro("gaussiano"))
        self.crear_boton("Filtro Bilateral", COLOR_INFO, lambda: self.aplicar_filtro("bilateral"))
        self.crear_boton("Filtro Mínimo", COLOR_INFO, lambda: self.aplicar_filtro("minimo"))
        self.crear_boton("Filtro Máximo", COLOR_INFO, lambda: self.aplicar_filtro("maximo"))
    
    def aplicar_filtro(self, tipo):
        """Aplica filtros espaciales."""
        nombres = {
            'promediador': 'Filtro Promediador',
            'mediana': 'Filtro Mediana',
            'gaussiano': 'Filtro Gaussiano',
            'bilateral': 'Filtro Bilateral',
            'minimo': 'Filtro Mínimo',
            'maximo': 'Filtro Máximo'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[tipo]}")
        dialogo.agregar_selector_imagen()
        
        kernel_spin = dialogo.agregar_spin("Tamaño Kernel:", 3, 15, 5, 2)
        
        info = QLabel(f"Se aplicará {nombres[tipo]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_INFO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.procesamiento_avanzado import Filtros
            
            try:
                kernel_size = kernel_spin.value()
                
                if tipo == "promediador":
                    resultado = Filtros.filtro_promediador(imagen, kernel_size)
                elif tipo == "mediana":
                    resultado = Filtros.filtro_mediana(imagen, kernel_size)
                elif tipo == "gaussiano":
                    resultado = Filtros.filtro_gaussiano(imagen, kernel_size)
                elif tipo == "bilateral":
                    resultado = Filtros.filtro_bilateral(imagen, d=kernel_size)
                elif tipo == "minimo":
                    resultado = Filtros.filtro_minimo(imagen, kernel_size)
                elif tipo == "maximo":
                    resultado = Filtros.filtro_maximo(imagen, kernel_size)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[tipo]} aplicado")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
