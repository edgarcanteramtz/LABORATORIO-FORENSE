import os
from datetime import datetime

def generar_reporte_txt(tipo_analisis, usuario, datos_evidencia):
    """
    Genera un archivo .txt formateado como reporte técnico forense y cadena de custodia.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo_reporte = f"REPORTE_{tipo_analisis.upper()}_{timestamp_filename}.txt"

    contenido = []
    contenido.append("================================================================================")
    contenido.append("                    LAB VISUAL FORENSE — REPORTE TÉCNICO")
    contenido.append("                         DOCUMENTO DE CADENA DE CUSTODIA")
    contenido.append("================================================================================")
    contenido.append(f"FECHA Y HORA DE GENERACIÓN: {fecha_hora}")
    contenido.append(f"PERITO / INVESTIGADOR     : {usuario.upper()}")
    contenido.append(f"TIPO DE ANÁLISIS          : {tipo_analisis.upper()}")
    contenido.append("================================================================================")
    contenido.append("\n[ DETALLES Y HALLAZGOS DE LA EVIDENCIA DIGITAL ]\n")

    if isinstance(datos_evidencia, dict):
        for clave, valor in datos_evidencia.items():
            contenido.append(f"  * {clave:<25}: {valor}")
    elif isinstance(datos_evidencia, list):
        for linea in datos_evidencia:
            contenido.append(f"  * {linea}")

    contenido.append("\n================================================================================")
    contenido.append("DECLARACIÓN DE INTEGRIDAD:")
    contenido.append("Los datos descritos en este documento corresponden a los valores extraídos de la")
    contenido.append("muestra analizada en el laboratorio y no han sido modificados durante el proceso.")
    contenido.append("================================================================================")
    contenido.append("\n\n-----------------------------------------")
    contenido.append(f"Firma de conformidad: {usuario}")
    contenido.append("Laboratorio Visual de Ciberforense")

    texto_final = "\n".join(contenido)

    return nombre_archivo_reporte, texto_final