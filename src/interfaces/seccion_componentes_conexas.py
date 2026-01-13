"""Sección de análisis de componentes conexas."""

from PySide6.QtWidgets import QMessageBox, QLabel
from src.interfaces.seccion_base import SeccionBase
from src.interfaces.dialogos_base import DialogoBase
from config import COLOR_EXITO
import cv2
import numpy as np


class SeccionComponentesConexas(SeccionBase):
    """Sección para análisis de componentes conexas."""
    
    def __init__(self, ventana_principal):
        super().__init__("COMPONENTES CONEXAS", COLOR_EXITO, ventana_principal)
    
    def crear_botones(self):
        """Crea los botones de componentes conexas."""
        self.crear_boton("Detectar Componentes", COLOR_EXITO, self.detectar_componentes)
        self.crear_boton("Contar Componentes", COLOR_EXITO, self.contar_componentes)
        self.crear_boton("Etiquetar Componentes", COLOR_EXITO, self.etiquetar_componentes)
    
    def detectar_componentes(self):
        """Detecta y visualiza componentes conexas."""
        dialogo = DialogoBase(self.ventana_principal, "Detectar Componentes Conexas")
        dialogo.agregar_selector_imagen()
        
        conectividad = dialogo.agregar_combo("Conectividad:", ["4", "8"], 1)  # Índice en lugar de texto
        
        info = QLabel("Se detectarán y colorearán las componentes conexas")
        info.setStyleSheet(f"color: {COLOR_EXITO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                # Convertir a binaria si no lo es
                if len(imagen.shape) == 3:
                    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                else:
                    imagen_gris = imagen.copy()
                
                _, imagen_bin = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY)
                
                # Detectar componentes
                conn = 8 if conectividad.currentText() == "8" else 4
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                    imagen_bin, connectivity=conn
                )
                
                # Crear imagen coloreada
                colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)
                colors[0] = [0, 0, 0]  # Fondo negro
                
                resultado = colors[labels]
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(
                    f"Detectadas {num_labels-1} componentes"
                )
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def contar_componentes(self):
        """Cuenta el número de componentes conexas con información detallada."""
        dialogo = DialogoBase(self.ventana_principal, "Análisis Detallado de Componentes")
        dialogo.agregar_selector_imagen()
        
        conectividad = dialogo.agregar_combo("Conectividad:", ["4", "8"], 1)
        
        info = QLabel("Analiza y cuenta las secciones blancas con estadísticas detalladas")
        info.setStyleSheet(f"color: {COLOR_EXITO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                # Convertir a binaria
                if len(imagen.shape) == 3:
                    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                else:
                    imagen_gris = imagen.copy()
                
                _, imagen_bin = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY)
                
                # Analizar componentes con estadísticas
                conn = 8 if conectividad.currentText() == "8" else 4
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                    imagen_bin, connectivity=conn
                )
                
                # Número de componentes (sin contar el fondo)
                num_componentes = num_labels - 1
                
                if num_componentes == 0:
                    QMessageBox.warning(
                        dialogo,
                        "Sin Componentes",
                        "No se detectaron objetos blancos en la imagen"
                    )
                    return
                
                # Extraer estadísticas (ignorar fondo en índice 0)
                areas = stats[1:, cv2.CC_STAT_AREA]
                anchos = stats[1:, cv2.CC_STAT_WIDTH]
                alturas = stats[1:, cv2.CC_STAT_HEIGHT]
                
                # Calcular estadísticas básicas de área
                area_min = np.min(areas)
                area_max = np.max(areas)
                area_promedio = np.mean(areas)
                area_total = np.sum(areas)
                area_std = np.std(areas)
                
                ancho_promedio = np.mean(anchos)
                altura_promedio = np.mean(alturas)
                
                # Calcular porcentaje de área ocupada
                total_pixeles = imagen_bin.shape[0] * imagen_bin.shape[1]
                porcentaje_ocupado = (area_total / total_pixeles) * 100
                
                # ===== CARACTERÍSTICAS AVANZADAS =====
                
                # Calcular perímetros y circularidad para cada componente
                circularidades = []
                perimetros = []
                relaciones_aspecto = []
                
                for i in range(1, num_labels):
                    # Crear máscara para esta componente
                    mask = (labels == i).astype(np.uint8) * 255
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    if contours:
                        perimetro = cv2.arcLength(contours[0], True)
                        perimetros.append(perimetro)
                        
                        # Circularidad: 4π*Área / Perímetro² (1.0 = círculo perfecto)
                        if perimetro > 0:
                            circularidad = (4 * np.pi * areas[i-1]) / (perimetro ** 2)
                            circularidades.append(min(circularidad, 1.0))  # Limitar a 1.0
                        else:
                            circularidades.append(0.0)
                    else:
                        perimetros.append(0.0)
                        circularidades.append(0.0)
                    
                    # Relación de aspecto (ancho/alto)
                    if alturas[i-1] > 0:
                        relacion = anchos[i-1] / alturas[i-1]
                        relaciones_aspecto.append(relacion)
                    else:
                        relaciones_aspecto.append(0.0)
                
                circularidades = np.array(circularidades)
                perimetros = np.array(perimetros)
                relaciones_aspecto = np.array(relaciones_aspecto)
                
                # Estadísticas de circularidad
                circ_promedio = np.mean(circularidades)
                circ_min = np.min(circularidades)
                circ_max = np.max(circularidades)
                
                # Estadísticas de perímetro
                perim_promedio = np.mean(perimetros)
                perim_min = np.min(perimetros)
                perim_max = np.max(perimetros)
                
                # Estadísticas de relación de aspecto
                aspecto_promedio = np.mean(relaciones_aspecto)
                
                # Uniformidad: Coeficiente de variación (CV)
                coef_variacion = (area_std / area_promedio) * 100 if area_promedio > 0 else 0
                
                # Clasificación por tamaño (terciles)
                if num_componentes >= 3:
                    percentil_33 = np.percentile(areas, 33)
                    percentil_66 = np.percentile(areas, 66)
                    pequenos = np.sum(areas < percentil_33)
                    medianos = np.sum((areas >= percentil_33) & (areas < percentil_66))
                    grandes = np.sum(areas >= percentil_66)
                    clasificacion = f"   • Pequeños: {pequenos} | Medianos: {medianos} | Grandes: {grandes}"
                else:
                    clasificacion = "   • Insuficientes para clasificar (mínimo 3)"
                
                # Evaluar calidad de circularidad (para monedas)
                objetos_circulares = np.sum(circularidades >= 0.8)
                porcentaje_circular = (objetos_circulares / num_componentes) * 100
                
                # Densidad (objetos por megapíxel)
                megapixeles = total_pixeles / 1_000_000
                densidad = num_componentes / megapixeles if megapixeles > 0 else 0
                
                # Crear mensaje detallado
                mensaje = f""" ANÁLISIS COMPLETO DE COMPONENTES CONEXAS

 CONTEO:
   • Componentes detectadas: {num_componentes}
   • Conectividad: {conn} vecinos
   • Densidad: {densidad:.1f} objetos/megapíxel

 ÁREAS (píxeles²):
   • Mínima: {area_min:,.0f} px²
   • Máxima: {area_max:,.0f} px²
   • Promedio: {area_promedio:,.1f} px²
   • Desv. Estándar: {area_std:,.1f} px²
   • Total: {area_total:,.0f} px²

 DIMENSIONES PROMEDIO:
   • Ancho: {ancho_promedio:.1f} px
   • Alto: {altura_promedio:.1f} px
   • Relación Aspecto: {aspecto_promedio:.2f} (1.0 = cuadrado/circular)

 CIRCULARIDAD (0.0-1.0):
   • Promedio: {circ_promedio:.3f}
   • Mínima: {circ_min:.3f}
   • Máxima: {circ_max:.3f}
   • Objetos circulares (≥0.8): {objetos_circulares}/{num_componentes} ({porcentaje_circular:.1f}%)

 PERÍMETROS (píxeles):
   • Promedio: {perim_promedio:.1f} px
   • Mínimo: {perim_min:.1f} px
   • Máximo: {perim_max:.1f} px

 UNIFORMIDAD:
   • Coef. Variación: {coef_variacion:.1f}% {"(Homogéneos)" if coef_variacion < 20 else "(Variables)"}
{clasificacion}

 OCUPACIÓN DE IMAGEN:
   • Objetos: {porcentaje_ocupado:.2f}%
   • Fondo: {100-porcentaje_ocupado:.2f}%

 INFO ADICIONAL:
   • Imagen: {imagen_bin.shape[1]} × {imagen_bin.shape[0]} px
   • Total píxeles: {total_pixeles:,}
"""
                
                # Mostrar pop-up con información detallada
                msg_box = QMessageBox(dialogo)
                msg_box.setWindowTitle("Análisis Detallado de Componentes")
                msg_box.setText(mensaje)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
                
                self.ventana_principal.statusBar().showMessage(
                    f" {num_componentes} componentes | Área promedio: {area_promedio:.0f}px² | Ocupación: {porcentaje_ocupado:.1f}%"
                )
                dialogo.accept()
                
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error al analizar componentes: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
    
    def etiquetar_componentes(self):
        """Etiqueta componentes con números."""
        dialogo = DialogoBase(self.ventana_principal, "Etiquetar Componentes")
        dialogo.agregar_selector_imagen()
        
        info = QLabel("Se etiquetarán las componentes con sus índices")
        info.setStyleSheet(f"color: {COLOR_EXITO}; font-style: italic;")
        info.setWordWrap(True)
        dialogo.layout_principal.addWidget(info)
        
        def aplicar():
            imagen, tipo = dialogo.obtener_imagen_seleccionada()
            if imagen is None:
                return
            
            try:
                # Convertir a binaria
                if len(imagen.shape) == 3:
                    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                else:
                    imagen_gris = imagen.copy()
                
                _, imagen_bin = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY)
                
                # Detectar componentes
                num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen_bin)
                
                # Crear imagen RGB para dibujar
                resultado = cv2.cvtColor(imagen_bin, cv2.COLOR_GRAY2RGB)
                
                # Dibujar etiquetas
                for i in range(1, num_labels):
                    cx, cy = centroids[i]
                    cv2.putText(resultado, str(i), 
                              (int(cx)-10, int(cy)+10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                
                dialogo.actualizar_imagen_seleccionada(resultado)
                self.ventana_principal.statusBar().showMessage(
                    f"Etiquetadas {num_labels-1} componentes"
                )
                dialogo.accept()
            except Exception as e:
                QMessageBox.critical(dialogo, "Error", f"Error: {str(e)}")
        
        dialogo.agregar_botones(aplicar)
        dialogo.exec()
