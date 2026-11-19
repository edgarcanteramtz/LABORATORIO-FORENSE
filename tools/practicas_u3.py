import os
import hashlib
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog

# Intentar importar ReportLab para generación de PDFs profesionales
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_DISPONIBLE = True
except ImportError:
    REPORTLAB_DISPONIBLE = False

# Intentar importar Pillow para lectura de EXIF real
try:
    from PIL import Image as PILImage
    from PIL.ExifTags import TAGS
    PILLOW_DISPONIBLE = True
except ImportError:
    PILLOW_DISPONIBLE = False

COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ENTRY_BG = "#0E1524"
COLOR_ACCENT = "#00F0FF"
COLOR_ACCENT_HOVER = "#00C4D4"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_SUCCESS = "#2EC4B6"
COLOR_DANGER = "#E63946"


def limpiar(c):
    for w in c.winfo_children():
        w.destroy()


def obtener_ruta_descargas():
    """Retorna la ruta absoluta de la carpeta Descargas del usuario."""
    return os.path.join(os.path.expanduser("~"), "Downloads")


# ==========================================
# MODAL DE MENSAJE HUD PERSONALIZADO
# ==========================================
def mostrar_mensaje_hud(parent, titulo, mensaje, tipo="info"):
    dialog = ctk.CTkToplevel(parent)
    dialog.title("")
    dialog.geometry("480x280")
    dialog.configure(fg_color=COLOR_BG_DARK)
    dialog.overrideredirect(True)
    dialog.attributes("-alpha", 0.0)
    dialog.grab_set()

    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 240
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 140
    dialog.geometry(f"+{x}+{y}")

    borde_color = COLOR_SUCCESS if tipo == "success" else (COLOR_DANGER if tipo == "error" else COLOR_ACCENT)
    titulo_color = COLOR_SUCCESS if tipo == "success" else (COLOR_DANGER if tipo == "error" else COLOR_ACCENT)

    card_modal = ctk.CTkFrame(dialog, fg_color=COLOR_CARD, border_color=borde_color, border_width=1, corner_radius=12)
    card_modal.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(card_modal, text=titulo, font=ctk.CTkFont("Segoe UI", 15, "bold"), text_color=titulo_color).pack(pady=(20, 8))

    lbl_msg = ctk.CTkLabel(card_modal, text=mensaje, font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT, justify="left", wraplength=420)
    lbl_msg.pack(pady=(0, 20), padx=20)

    id_anim_dialog = None

    def animar_aparicion(alpha=0.0):
        nonlocal id_anim_dialog
        if alpha < 1.0:
            alpha += 0.1
            dialog.attributes("-alpha", alpha)
            id_anim_dialog = dialog.after(15, lambda: animar_aparicion(alpha))

    def cerrar():
        if id_anim_dialog:
            try:
                dialog.after_cancel(id_anim_dialog)
            except Exception:
                pass
        dialog.destroy()

    btn_ok = ctk.CTkButton(
        card_modal, text="Aceptar", command=cerrar, width=150, height=38,
        fg_color=borde_color, hover_color=COLOR_ACCENT_HOVER if tipo == "info" else borde_color,
        text_color=COLOR_BG_DARK if tipo != "error" else COLOR_TEXT_LIGHT,
        font=ctk.CTkFont("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2"
    )
    btn_ok.pack(pady=(0, 15))

    animar_aparicion()
    parent.wait_window(dialog)


# ==========================================
# PRÁCTICA 3.1: EXTRACCIÓN REAL DE METADATOS EXIF (Con Archivo de PC)
# ==========================================
def cargar_practica_u3_p1(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🔍 Práctica 3.1: Extracción de Metadatos EXIF de Archivo Real",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Selecciona una fotografía real de tu computadora para extraer sus metadatos ocultos (Pillow / ExifTool) y generar el reporte PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=10)

    lbl_ruta = ctk.CTkLabel(f_file, text="Ningún archivo seleccionado...", font=("Segoe UI", 11),
                            text_color=COLOR_TEXT_MUTED)
    lbl_ruta.pack(side="left", padx=5)

    datos_exif = {"ruta": "", "info": ""}

    txt_resultado = ctk.CTkTextbox(f_card, height=150, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT,
                                   font=("Consolas", 11))
    txt_resultado.pack(fill="both", expand=True, padx=20, pady=5)
    txt_resultado.insert("1.0", "Haz clic en 'Examinar Imagen Real...' para cargar un archivo de tu PC.")
    txt_resultado.configure(state="disabled")

    def examinar_y_extraer():
        ruta = filedialog.askopenfilename(title="Seleccionar imagen real de evidencia",
                                         filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.tiff *.bmp")])
        if not ruta:
            return

        datos_exif["ruta"] = ruta
        lbl_ruta.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        resultado = "--- ANÁLISIS DE ARCHIVO REAL ---\n"
        resultado += f"• Nombre: {os.path.basename(ruta)}\n"
        resultado += f"• Ruta: {ruta}\n"
        resultado += f"• Tamaño en disco: {os.path.getsize(ruta)} bytes\n\n"

        if PILLOW_DISPONIBLE:
            try:
                img = PILImage.open(ruta)
                resultado += f"• Formato / Resolución: {img.format}, {img.size}, Modo: {img.mode}\n"
                exif_data = img._getexif()
                if exif_data:
                    resultado += "• Etiquetas EXIF Encontradas:\n"
                    for tag_id, val in exif_data.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        if isinstance(val, bytes):
                            continue
                        resultado += f"   - {tag_name}: {val}\n"
                else:
                    resultado += "• [Aviso]: El archivo seleccionado no contiene etiquetas EXIF o fueron depuradas.\n"
            except Exception as e:
                resultado += f"• Error leyendo EXIF con Pillow: {str(e)}\n"
        else:
            resultado += "• [Aviso]: Librería Pillow no instalada para lectura profunda de EXIF.\n"

        datos_exif["info"] = resultado
        txt_resultado.configure(state="normal")
        txt_resultado.delete("1.0", "end")
        txt_resultado.insert("end", resultado)
        txt_resultado.configure(state="disabled")

    ctk.CTkButton(f_file, text="Examinar Imagen Real...", command=examinar_y_extraer, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=170).pack(side="right", padx=5)

    def exportar_pdf():
        if not datos_exif["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero debes seleccionar y analizar una imagen de tu computadora.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Reporte_EXIF_Real_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("REPORTE TÉCNICO FORENSE - METADATOS EXIF (ARCHIVO REAL)", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(datos_exif["info"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Reporte Generado", f"El reporte PDF con los metadatos reales se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Reporte PDF con Datos Reales (Descargas)", command=exportar_pdf,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 3.2: AUDITORÍA HEXADECIMAL DE UN ARCHIVO REAL DE LA PC
# ==========================================
def cargar_practica_u3_p2(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="⚙️ Práctica 3.2: Auditoría Hexadecimal y Volcado de Cabecera (Archivo Real)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Selecciona cualquier archivo de tu computadora para inspeccionar sus primeros bytes en formato hexadecimal (Magic Numbers) y generar su bitácora PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=10)

    lbl_ruta_hex = ctk.CTkLabel(f_file, text="Ningún archivo seleccionado...", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED)
    lbl_ruta_hex.pack(side="left", padx=5)

    auditoria_data = {"ruta": "", "detalle": ""}

    txt_hex = ctk.CTkTextbox(f_card, height=140, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=("Consolas", 11))
    txt_hex.pack(fill="both", expand=True, padx=20, pady=5)
    txt_hex.insert("1.0", "Selecciona un archivo de tu PC para leer su estructura interna y cabecera real...")
    txt_hex.configure(state="disabled")

    def auditar_archivo_real():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo para auditoría hexadecimal")
        if not ruta:
            return

        auditoria_data["ruta"] = ruta
        lbl_ruta_hex.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        try:
            with open(ruta, "rb") as f:
                primeros_bytes = f.read(64)

            hex_str = " ".join(f"{b:02X}" for b in primeros_bytes)
            sha = hashlib.sha256()
            with open(ruta, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha.update(chunk)
            hash_val = sha.hexdigest()

            detalle = (
                "--- AUDITORÍA HEXADECIMAL DE ARCHIVO REAL ---\n"
                f"• Archivo: {os.path.basename(ruta)}\n"
                f"• Tamaño: {os.path.getsize(ruta)} bytes\n"
                f"• SHA-256: {hash_val}\n\n"
                f"• Primeros 64 bytes (Cabecera / Magic Numbers):\n{hex_str}"
            )
            auditoria_data["detalle"] = detalle

            txt_hex.configure(state="normal")
            txt_hex.delete("1.0", "end")
            txt_hex.insert("end", detalle)
            txt_hex.configure(state="disabled")
            mostrar_mensaje_hud(container, "✨ Análisis Completo", "Se leyó la cabecera hexadecimal y se calculó el hash SHA-256 del archivo con éxito.", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo leer el archivo: {str(e)}", tipo="error")

    ctk.CTkButton(f_file, text="Examinar Archivo Real...", command=auditar_archivo_real, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=170).pack(side="right", padx=5)

    def exportar_pdf_hex():
        if not auditoria_data["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero selecciona un archivo de tu PC para auditar.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Bitacora_Hex_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("BITÁCORA FORENSE - AUDITORÍA DE CABECERA Y HASH (ARCHIVO REAL)", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(auditoria_data["detalle"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Bitácora Generada", f"El reporte de auditoría se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Bitácora Hexadecimal en PDF (Descargas)", command=exportar_pdf_hex,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 3.3: VERIFICACIÓN DE FIRMA DIGITAL Y CARVING (Con Archivo Real)
# ==========================================
def cargar_practica_u3_p3(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="💻 Práctica 3.3: Verificación de Firma e Integridad (Archivo Real de PC)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Sube un archivo de tu computadora para validar su firma real (Magic Numbers vs extensión) y generar el acta oficial en PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=10)

    lbl_ruta_verif = ctk.CTkLabel(f_file, text="Ningún archivo seleccionado...", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED)
    lbl_ruta_verif.pack(side="left", padx=5)

    verif_data = {"ruta": "", "resumen": ""}

    txt_verif = ctk.CTkTextbox(f_card, height=140, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=("Consolas", 11))
    txt_verif.pack(fill="both", expand=True, padx=20, pady=5)
    txt_verif.insert("1.0", "Selecciona un archivo real de tu PC para verificar su correspondencia de formato...")
    txt_verif.configure(state="disabled")

    def verificar_archivo_real():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo para verificar firma")
        if not ruta:
            return

        verif_data["ruta"] = ruta
        lbl_ruta_verif.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        try:
            with open(ruta, "rb") as f:
                header_bytes = f.read(12)

            ext = os.path.splitext(ruta)[1].lower()
            h_hex = header_bytes.hex().upper()

            tipo_detectado = "Desconocido / Genérico"
            if header_bytes.startswith(b"\xFF\xD8\xFF"):
                tipo_detectado = "Imagen JPEG (.jpg)"
            elif header_bytes.startswith(b"\x89PNG\r\n\x1A\n"):
                tipo_detectado = "Imagen PNG (.png)"
            elif header_bytes.startswith(b"%PDF"):
                tipo_detectado = "Documento PDF (.pdf)"
            elif header_bytes.startswith(b"PK\x03\x04"):
                tipo_detectado = "Contenedor ZIP / Office (.docx, .xlsx, .zip)"

            coincide = "⚠️ Posible archivo renombrado o formato especial"
            if (ext == ".jpg" and "JPEG" in tipo_detectado) or \
               (ext == ".png" and "PNG" in tipo_detectado) or \
               (ext == ".pdf" and "PDF" in tipo_detectado) or \
               (ext in [".docx", ".xlsx", ".zip"] and "ZIP" in tipo_detectado):
                coincide = "✅ La extensión coincide perfectamente con su firma real (Magic Number)."

            resumen = (
                "--- VERIFICACIÓN FORENSE DE FIRMA ---\n"
                f"• Nombre del archivo: {os.path.basename(ruta)}\n"
                f"• Extensión declarada: {ext}\n"
                f"• Firma real (Hex): {h_hex[:24]}...\n"
                f"• Tipo detectado por bytes: {tipo_detectado}\n"
                f"• Diagnóstico de Integridad: {coincide}"
            )
            verif_data["resumen"] = resumen

            txt_verif.configure(state="normal")
            txt_verif.delete("1.0", "end")
            txt_verif.insert("end", resumen)
            txt_verif.configure(state="disabled")
            mostrar_mensaje_hud(container, "✨ Verificación Exitosa", "Se cotejó la extensión del archivo con sus bytes reales de cabecera.", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo analizar el archivo: {str(e)}", tipo="error")

    ctk.CTkButton(f_file, text="Examinar Archivo Real...", command=verificar_archivo_real, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=170).pack(side="right", padx=5)

    def exportar_pdf_verif():
        if not verif_data["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero selecciona un archivo de tu PC para verificar.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Acta_Verificacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("ACTA FORENSE - VERIFICACIÓN DE FIRMA Y CABECERA (ARCHIVO REAL)", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(verif_data["resumen"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Acta Generada", f"El acta de verificación se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Acta de Verificación en PDF (Descargas)", command=exportar_pdf_verif,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 3.4: EXTRACCIÓN DE CADENAS (STRINGS) EN ARCHIVO REAL
# ==========================================
def cargar_practica_u3_p4(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🧩 Práctica 3.4: Extracción de Cadenas (Strings) y Evidencia Oculta",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Carga un archivo real de tu computadora (.txt, .log, .bin, .exe, etc.) para extraer cadenas legibles ASCII y generar su reporte PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=10)

    lbl_ruta_str = ctk.CTkLabel(f_file, text="Ningún archivo seleccionado...", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED)
    lbl_ruta_str.pack(side="left", padx=5)

    strings_data = {"ruta": "", "resumen": ""}

    txt_strings = ctk.CTkTextbox(f_card, height=150, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=("Consolas", 11))
    txt_strings.pack(fill="both", expand=True, padx=20, pady=5)
    txt_strings.insert("1.0", "Selecciona un archivo real de tu PC para buscar secuencias de caracteres imprimibles (mínimo 4 caracteres)...")
    txt_strings.configure(state="disabled")

    def extraer_strings_real():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo para extracción de cadenas")
        if not ruta:
            return

        strings_data["ruta"] = ruta
        lbl_ruta_str.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        try:
            with open(ruta, "rb") as f:
                contenido = f.read(65536)

            cadenas = []
            actual = []
            for b in contenido:
                if 32 <= b <= 126:
                    actual.append(chr(b))
                else:
                    if len(actual) >= 4:
                        cadenas.append("".join(actual))
                    actual = []
            if len(actual) >= 4:
                cadenas.append("".join(actual))

            muestra = cadenas[:25]
            cadenas_str = "\n".join(f"  - {c}" for c in muestra) if muestra else "  [No se encontraron cadenas imprimibles de >= 4 caracteres]"

            resumen = (
                "--- EXTRACCIÓN DE STRINGS (ARCHIVO REAL) ---\n"
                f"• Archivo: {os.path.basename(ruta)}\n"
                f"• Bytes analizados: {len(contenido)} bytes\n"
                f"• Total cadenas detectadas (>=4 chars): {len(cadenas)}\n"
                f"• Primeras cadenas encontradas:\n{cadenas_str}"
            )
            strings_data["resumen"] = resumen

            txt_strings.configure(state="normal")
            txt_strings.delete("1.0", "end")
            txt_strings.insert("end", resumen)
            txt_strings.configure(state="disabled")
            mostrar_mensaje_hud(container, "✨ Extracción Completada", f"Se analizaron {len(contenido)} bytes y se hallaron {len(cadenas)} cadenas legibles.", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo leer el archivo: {str(e)}", tipo="error")

    ctk.CTkButton(f_file, text="Examinar Archivo Real...", command=extraer_strings_real, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=170).pack(side="right", padx=5)

    def exportar_pdf_strings():
        if not strings_data["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero selecciona y analiza un archivo de tu computadora.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Reporte_Strings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("REPORTE FORENSE - EXTRACCIÓN DE CADENAS (STRINGS)", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(strings_data["resumen"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Reporte Generado", f"El reporte de cadenas se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Reporte PDF de Cadenas (Descargas)", command=exportar_pdf_strings,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)
