"""Sección de operaciones aritméticas con escalares."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_ADVERTENCIA


class SeccionAritmeticas(SeccionBase):
    """Sección para operaciones aritméticas con escalares."""
    
    def __init__(self, ventana_principal):
        super().__init__("OPERACIONES ARITMÉTICAS", COLOR_ADVERTENCIA, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de operaciones aritméticas."""
        self.crear_boton("Suma Escalar", COLOR_ADVERTENCIA, lambda: self.aplicar_operacion("suma"))
        self.crear_boton("Resta Escalar", COLOR_ADVERTENCIA, lambda: self.aplicar_operacion("resta"))
        self.crear_boton("Multiplicación Escalar", COLOR_ADVERTENCIA, lambda: self.aplicar_operacion("multiplicacion"))
        self.crear_boton("División Escalar", COLOR_ADVERTENCIA, lambda: self.aplicar_operacion("division"))
    
    def aplicar_operacion(self, operacion):
        """Aplica operaciones aritméticas con escalar."""
        nombres = {
            'suma': 'Suma Escalar',
            'resta': 'Resta Escalar',
            'multiplicacion': 'Multiplicación Escalar',
            'division': 'División Escalar'
        }
        
        dialogo = DialogoBase(self.ventana_principal, f"Aplicar: {nombres[operacion]}")
        dialogo.agregar_selector_imagen()
        
        # Parámetro escalar
        if operacion in ["multiplicacion", "division"]:
            escalar_spin = dialogo.agregar_spin("Valor escalar:", 0.1, 10.0, 1.0, 0.1, es_double=True)
        else:
            escalar_spin = dialogo.agregar_spin("Valor escalar:", -255, 255, 0, 1)
        
        info = QLabel(f"Se aplicará {nombres[operacion]} a la imagen seleccionada")
        info.setStyleSheet(f"color: {COLOR_ADVERTENCIA}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            from src.operaciones import OperacionesAritmeticas
            
            try:
                escalar = escalar_spin.value()
                
                if operacion == "suma":
                    resultado = OperacionesAritmeticas.suma_escalar(imagen, escalar)
                elif operacion == "resta":
                    resultado = OperacionesAritmeticas.resta_escalar(imagen, escalar)
                elif operacion == "multiplicacion":
                    resultado = OperacionesAritmeticas.multiplicacion_escalar(imagen, escalar)
                elif operacion == "division":
                    resultado = OperacionesAritmeticas.division_escalar(imagen, escalar)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(f"{nombres[operacion]}: {escalar}")
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
