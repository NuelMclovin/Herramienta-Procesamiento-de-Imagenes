"""Sección de operaciones con archivos."""

from PySide6.QtWidgets import QFileDialog, QMessageBox
from src.interfaces.seccion_base import SeccionBase
from config import COLOR_PRIMARIO


class SeccionArchivo(SeccionBase):
    """Sección para cargar, guardar y restaurar imágenes."""
    
    def __init__(self, ventana_principal):
        super().__init__("ARCHIVO", COLOR_PRIMARIO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de la sección archivo."""
        self.crear_boton("Cargar Imagen 1", COLOR_PRIMARIO, self.cargar_imagen_1)
        self.crear_boton("Cargar Imagen 2", COLOR_PRIMARIO, self.cargar_imagen_2)
        self.crear_boton("Guardar Imagen 1", COLOR_PRIMARIO, self.guardar_imagen_1)
        self.crear_boton("Guardar Resultado", COLOR_PRIMARIO, self.guardar_resultado)
        self.crear_boton("Restaurar Original", COLOR_PRIMARIO, self.restaurar_imagen)
    
    def cargar_imagen_1(self):
        """Carga la primera imagen."""
        from src.utilidades import CargadorImagenes
        ruta, _ = QFileDialog.getOpenFileName(
            self.ventana_principal,
            "Cargar Imagen 1",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if ruta:
            try:
                img = CargadorImagenes.cargar_imagen(ruta)
                self.ventana_principal.imagen_actual = img
                self.ventana_principal.imagen_original_backup = img.copy()
                # Inicializar modo de color según la imagen cargada
                if len(img.shape) == 2:
                    self.ventana_principal.modo_color_img1 = 'GRAY'
                else:
                    self.ventana_principal.modo_color_img1 = 'RGB'
                self.ventana_principal.mostrar_imagen_1()
                self.ventana_principal.statusBar().showMessage(f"Imagen 1 cargada: {ruta}")
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error al cargar: {str(e)}")
    
    def cargar_imagen_2(self):
        """Carga la segunda imagen."""
        from src.utilidades import CargadorImagenes
        ruta, _ = QFileDialog.getOpenFileName(
            self.ventana_principal,
            "Cargar Imagen 2",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if ruta:
            try:
                img = CargadorImagenes.cargar_imagen(ruta)
                self.ventana_principal.imagen_segunda = img
                self.ventana_principal.imagen_segunda_backup = img.copy()
                # Inicializar modo de color según la imagen cargada
                if len(img.shape) == 2:
                    self.ventana_principal.modo_color_img2 = 'GRAY'
                else:
                    self.ventana_principal.modo_color_img2 = 'RGB'
                self.ventana_principal.mostrar_imagen_2()
                self.ventana_principal.statusBar().showMessage(f"Imagen 2 cargada: {ruta}")
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error al cargar: {str(e)}")
    
    def guardar_imagen_1(self):
        """Guarda la imagen actual."""
        if self.ventana_principal.imagen_actual is None:
            QMessageBox.warning(self.ventana_principal, "Advertencia", "No hay imagen para guardar")
            return
        
        from src.utilidades import CargadorImagenes
        ruta, _ = QFileDialog.getSaveFileName(
            self.ventana_principal,
            "Guardar Imagen 1",
            "",
            "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        if ruta:
            try:
                CargadorImagenes.guardar_imagen(self.ventana_principal.imagen_actual, ruta)
                self.ventana_principal.statusBar().showMessage(f"Imagen guardada: {ruta}")
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error al guardar: {str(e)}")
    
    def guardar_resultado(self):
        """Guarda la imagen resultado."""
        if self.ventana_principal.imagen_resultado is None:
            QMessageBox.warning(self.ventana_principal, "Advertencia", "No hay resultado para guardar")
            return
        
        from src.utilidades import CargadorImagenes
        ruta, _ = QFileDialog.getSaveFileName(
            self.ventana_principal,
            "Guardar Resultado",
            "",
            "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        if ruta:
            try:
                CargadorImagenes.guardar_imagen(self.ventana_principal.imagen_resultado, ruta)
                self.ventana_principal.statusBar().showMessage(f"Resultado guardado: {ruta}")
            except Exception as e:
                QMessageBox.critical(self.ventana_principal, "Error", f"Error al guardar: {str(e)}")
    
    def restaurar_imagen(self):
        """Restaura la imagen original."""
        if self.ventana_principal.imagen_original_backup is None:
            QMessageBox.warning(self.ventana_principal, "Advertencia", "No hay imagen original")
            return
        
        self.ventana_principal.imagen_actual = self.ventana_principal.imagen_original_backup.copy()
        # Restaurar modo de color original
        if len(self.ventana_principal.imagen_original_backup.shape) == 2:
            self.ventana_principal.modo_color_img1 = 'GRAY'
        else:
            self.ventana_principal.modo_color_img1 = 'RGB'
        self.ventana_principal.mostrar_imagen_1()
        self.ventana_principal.statusBar().showMessage("Imagen 1 restaurada")
