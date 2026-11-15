import os

def extraer_metadatos_imagen(ruta_imagen):
    """
    Extractor de metadatos robusto y a prueba de errores para imágenes forenses.
    Soporta JPG, JPEG, PNG, WEBP, TIFF, etc., manejando excepciones de forma limpia.
    """
    metadatos = {}

    if not os.path.exists(ruta_imagen):
        return {"Error": "El archivo especificado no existe en la ruta indicada."}

    try:
        # Metadatos del sistema de archivos
        tamaño_bytes = os.path.getsize(ruta_imagen)
        metadatos["Archivo"] = os.path.basename(ruta_imagen)
        metadatos["Ruta Completa"] = ruta_imagen
        metadatos["Tamaño en Disco"] = f"{round(tamaño_bytes / 1024, 2)} KB"
    except Exception as e:
        metadatos["Error Sistema Archivos"] = str(e)

    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        with Image.open(ruta_imagen) as img:
            metadatos["Formato de Imagen"] = str(img.format)
            metadatos["Modo de Color"] = str(img.mode)
            metadatos["Dimensiones (Resolución)"] = f"{img.width} x {img.height} píxeles"

            datos_exif = {}

            # Extracción segura de EXIF estándar
            try:
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, valor in exif_data.items():
                        etiqueta = TAGS.get(tag_id, tag_id)
                        # Limpiar valores binarios largos para evitar fallos de renderizado
                        if isinstance(valor, bytes):
                            valor = f"<Datos Binarios / {len(valor)} bytes>"
                        datos_exif[str(etiqueta)] = str(valor)
            except Exception:
                pass

            # Método alternativo para JPEGs legacy
            if not datos_exif and hasattr(img, '_getexif'):
                try:
                    exif_raw = img._getexif()
                    if exif_raw:
                        for tag_id, valor in exif_raw.items():
                            etiqueta = TAGS.get(tag_id, tag_id)
                            if isinstance(valor, bytes):
                                valor = f"<Datos Binarios / {len(valor)} bytes>"
                            datos_exif[str(etiqueta)] = str(valor)
                except Exception:
                    pass

            # Extraer bloques .info (muy útil para PNG, metadatos web o comentarios)
            if hasattr(img, 'info') and img.info:
                for k, v in img.info.items():
                    if k.lower() != 'exif':
                        if isinstance(v, bytes):
                            v = f"<Bytes / {len(v)}>"
                        datos_exif[f"Info adicional ({k})"] = str(v)

            if datos_exif:
                metadatos["EXIF / Metadatos Internos"] = datos_exif
            else:
                metadatos["EXIF / Metadatos Internos"] = "La imagen no contiene etiquetas EXIF o fueron depuradas (imagen limpia)."

    except ImportError:
        metadatos["Error de Dependencia"] = "La librería Pillow no está instalada correctamente."
    except Exception as e:
        metadatos["Error de Lectura de Imagen"] = f"El archivo no es una imagen válida o está dañado: {str(e)}"

    return metadatos