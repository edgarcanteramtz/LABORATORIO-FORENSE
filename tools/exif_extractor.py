import os

def extraer_metadatos_imagen(ruta_imagen):
    """
    Extrae metadatos generales, cabeceras EXIF y datos de información de una imagen.
    Soporta JPG, JPEG, PNG, TIFF, etc.
    """
    metadatos = {}

    if not os.path.exists(ruta_imagen):
        return {"Error": "El archivo especificado no existe."}

    # Metadatos a nivel de sistema de archivos
    tamaño_bytes = os.path.getsize(ruta_imagen)
    metadatos["Nombre Archivo"] = os.path.basename(ruta_imagen)
    metadatos["Ruta"] = ruta_imagen
    metadatos["Tamaño"] = f"{round(tamaño_bytes / 1024, 2)} KB"

    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        with Image.open(ruta_imagen) as img:
            metadatos["Formato"] = img.format
            metadatos["Modo de Color"] = img.mode
            metadatos["Dimensiones"] = f"{img.width} x {img.height} px"

            datos_exif = {}

            # 1. Extraer EXIF con método moderno (Pillow 7+)
            try:
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, valor in exif_data.items():
                        etiqueta = TAGS.get(tag_id, tag_id)
                        if isinstance(valor, bytes) and len(valor) > 40:
                            valor = "<Datos Binarios Omitidos>"
                        datos_exif[str(etiqueta)] = str(valor)
            except Exception:
                pass

            # 2. Respaldar con método legacy para JPEGs si el primero no devolvió datos
            if not datos_exif and hasattr(img, '_getexif'):
                try:
                    exif_raw = img._getexif()
                    if exif_raw:
                        for tag_id, valor in exif_raw.items():
                            etiqueta = TAGS.get(tag_id, tag_id)
                            if isinstance(valor, bytes) and len(valor) > 40:
                                valor = "<Datos Binarios Omitidos>"
                            datos_exif[str(etiqueta)] = str(valor)
                except Exception:
                    pass

            # 3. Extraer bloque .info (útil para PNG, software de edición, comentarios)
            if hasattr(img, 'info') and img.info:
                for k, v in img.info.items():
                    if k.lower() != 'exif' and isinstance(v, (str, int, float)):
                        datos_exif[f"Info ({k})"] = str(v)

            metadatos["EXIF"] = datos_exif if datos_exif else "Sin datos EXIF (imagen comprimida, PNG o web)."

    except ImportError:
        metadatos["Nota"] = "Para extracción EXIF avanzada instala Pillow (pip install pillow)."
    except Exception as e:
        metadatos["Error EXIF"] = f"No se pudieron leer datos EXIF: {str(e)}"

    return metadatos