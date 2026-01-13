"""Sección de transformada de Fourier y DCT."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_EXITO


class SeccionFourier(SeccionBase):
    """Sección para transformadas de Fourier y DCT."""
    
    def __init__(self, ventana_principal):
        super().__init__("FOURIER / DCT", COLOR_EXITO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de Fourier/DCT."""
        self.crear_boton("FFT 2D", COLOR_EXITO, lambda: self.aplicar_fourier("fft"))
        self.crear_boton("Filtro Pasa Bajas", COLOR_EXITO, lambda: self.aplicar_fourier("lowpass"))
        self.crear_boton("Filtro Pasa Altas", COLOR_EXITO, lambda: self.aplicar_fourier("highpass"))
        self.crear_boton("DCT Compresión", COLOR_EXITO, self.aplicar_dct_dialogo)
    
    def aplicar_fourier(self, operacion):
        """Aplica transformada de Fourier con diálogo."""
        nombres = {
            'fft': 'FFT 2D (Espectro de Magnitud)',
            'lowpass': 'Filtro Pasa Bajas',
            'highpass': 'Filtro Pasa Altas'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[operacion]}")
        dialogo.agregar_selector_imagen()
        
        # Parámetros
        cutoff_spin = None
        if operacion in ['lowpass', 'highpass']:
            cutoff_spin = dialogo.agregar_spin("Cutoff (frecuencia):", 0.01, 0.5, 0.2 if operacion == 'lowpass' else 0.08, 0.01, es_double=True)
        
        # Info
        info = QLabel(f"Se aplicara {nombres[operacion]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_EXITO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.fourier import TransformadaFourier
            from src.utilidades import CargadorImagenes
            
            try:
                tf = TransformadaFourier()
                img_gris = CargadorImagenes.convertir_a_gris(imagen)
                img_norm = CargadorImagenes.normalizar(img_gris)
                
                if operacion == "fft":
                    _, _, _, magnitud_log, _ = tf.fft2_imagen(img_norm)
                    resultado = CargadorImagenes.desnormalizar(magnitud_log / magnitud_log.max())
                elif operacion == "lowpass":
                    cutoff = cutoff_spin.value()
                    img_filt, _, _ = tf.aplicar_filtro_frecuencia(img_norm, tipo='lowpass', cutoff=cutoff)
                    resultado = CargadorImagenes.desnormalizar(img_filt)
                elif operacion == "highpass":
                    cutoff = cutoff_spin.value()
                    img_filt, _, _ = tf.aplicar_filtro_frecuencia(img_norm, tipo='highpass', cutoff=cutoff)
                    resultado = CargadorImagenes.desnormalizar(img_filt)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"Transformada de Fourier: {operacion.upper()}")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al aplicar Fourier: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def aplicar_dct_dialogo(self):
        """Aplica compresión DCT con diálogo."""
        dialogo = DialogoBase(self.ventana_principal, "Aplicar: DCT Compresión")
        dialogo.agregar_selector_imagen()
        
        # Parámetros
        q_spin = dialogo.agregar_spin("Factor de calidad (Q):", 1, 100, 50, 1)
        
        # Info
        info = QLabel("Se aplicara compresion DCT a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_EXITO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, img_tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.fourier import TransformadaDCT
            from src.utilidades import CargadorImagenes
            
            try:
                q_factor = q_spin.value()
                dct = TransformadaDCT()
                img_gris = CargadorImagenes.convertir_a_gris(imagen)
                img_norm = CargadorImagenes.normalizar(img_gris)
                
                img_comp, metricas = dct.comprimir_dct(img_norm, q_factor)
                resultado = CargadorImagenes.desnormalizar(img_comp)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"DCT aplicado (Q={q_factor}): PSNR={metricas['psnr']:.2f} dB")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al aplicar DCT: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
