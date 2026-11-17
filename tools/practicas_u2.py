import os
import hashlib
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Intentar importar ReportLab para generación de PDFs profesionales
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors

    REPORTLAB_DISPONIBLE = True
except ImportError:
    REPORTLAB_DISPONIBLE = False

COLOR_CARD = "#090D18"
COLOR_ENTRY_BG = "#0E1524"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_SUCCESS = "#2EC4B6"
COLOR_DANGER = "#E63946"


def limpiar(c):
    for w in c.winfo_children(): w.destroy()


def obtener_ruta_descargas():
    """Retorna la ruta absoluta de la carpeta Descargas del usuario."""
    return os.path.join(os.path.expanduser("~"), "Downloads")


# ==========================================
# PRÁCTICA 2.1: RECOLECCIÓN DE EVIDENCIA Y ACTA EN PDF (Con Imagen y Celdas Ajustadas)
# ==========================================
def cargar_practica_u2_p1(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🛠️ Práctica 2.1: Recolección y Acta de Indicios (Cadena de Custodia)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Sube una imagen de evidencia de tu PC, ingresa su nombre y descripción para generar el acta oficial en PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    # Selección de archivo
    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=10)

    lbl_ruta_archivo = ctk.CTkLabel(f_file, text="Ningún archivo seleccionado...", font=("Segoe UI", 11),
                                    text_color=COLOR_TEXT_MUTED)
    lbl_ruta_archivo.pack(side="left", padx=5)

    path_almacenado = {"ruta": ""}

    def examinar_img():
        ruta = filedialog.askopenfilename(title="Seleccionar evidencia digital",
                                          filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")])
        if ruta:
            path_almacenado["ruta"] = ruta
            lbl_ruta_archivo.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

    ctk.CTkButton(f_file, text="Examinar Imagen...", command=examinar_img, fg_color=COLOR_ACCENT, text_color="#05070A",
                  width=140).pack(side="right", padx=5)

    # Campos de Formulario
    ctk.CTkLabel(f_card, text="Nombre de la Evidencia:", font=("Segoe UI", 12, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=20, pady=(10, 2))
    entry_nombre = ctk.CTkEntry(f_card, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, height=35)
    entry_nombre.pack(fill="x", padx=20, pady=5)

    ctk.CTkLabel(f_card, text="Descripción del Dispositivo / Estado:", font=("Segoe UI", 12, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=20, pady=(10, 2))
    txt_desc = ctk.CTkTextbox(f_card, height=70, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    txt_desc.pack(fill="x", padx=20, pady=5)
    txt_desc.insert("1.0", "Ej: Dispositivo asegurado en encendido, con aislamiento de red perimetral...")

    def generar_acta_pdf():
        if not path_almacenado["ruta"] or not entry_nombre.get().strip():
            messagebox.showwarning("Atención", "Debes seleccionar una imagen y escribir un nombre para la evidencia.")
            return

        if not REPORTLAB_DISPONIBLE:
            messagebox.showerror("Error", "La librería 'reportlab' no está instalada. Ejecuta: pip install reportlab")
            return

        try:
            nombre_archivo_pdf = f"Acta_Recoleccion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_archivo_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()

            style_celda = ParagraphStyle(
                'CeldaTabla',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                leading=12,
                textColor=colors.HexColor("#1E293B")
            )
            style_celda_bold = ParagraphStyle(
                'CeldaTablaBold',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=10,
                leading=12,
                textColor=colors.HexColor("#0F172A")
            )

            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(
                Paragraph("LABORATORIO VISUAL FORENSE - ACTA DE RECOLECCIÓN DE INDICIOS", styles['Heading2']))
            elementos.append(Spacer(1, 10))

            t_data = [
                [Paragraph("Fecha y Hora:", style_celda_bold),
                 Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style_celda)],
                [Paragraph("Nombre de Evidencia:", style_celda_bold),
                 Paragraph(entry_nombre.get().strip(), style_celda)],
                [Paragraph("Ruta de Archivo Original:", style_celda_bold),
                 Paragraph(path_almacenado["ruta"], style_celda)],
                [Paragraph("Descripción:", style_celda_bold),
                 Paragraph(txt_desc.get("1.0", "end").strip(), style_celda)],
                [Paragraph("Institución:", style_celda_bold),
                 Paragraph("ITTLA - División de Estudios Profesionales en TICs", style_celda)]
            ]

            t = Table(t_data, colWidths=[150, 340])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#E2E8F0")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1"))
            ]))
            elementos.append(t)
            elementos.append(Spacer(1, 15))

            elementos.append(Paragraph("<b>Evidencia Gráfica Adjunta:</b>", styles['Heading3']))
            elementos.append(Spacer(1, 5))
            try:
                img_pdf = RLImage(path_almacenado["ruta"], width=250, height=180)
                img_pdf.hAlign = 'CENTER'
                elementos.append(img_pdf)
            except Exception:
                elementos.append(Paragraph("<i>[No se pudo renderizar la vista previa de la imagen en el PDF]</i>",
                                           styles['Normal']))

            elementos.append(Spacer(1, 15))
            elementos.append(Paragraph(
                "<b>Observación Legal:</b> El presente documento valida la cadena de custodia inicial conforme a los estándares internacionales ISO/IEC 27037.",
                styles['Normal']))

            doc.build(elementos)
            messagebox.showinfo("Reporte Generado con Éxito",
                                f"El acta en PDF se guardó correctamente en tu carpeta de Descargas:\n\n{ruta_pdf}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    ctk.CTkButton(container, text="📄 Generar Acta de Recolección en PDF (Descargas)", command=generar_acta_pdf,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x",
                                                                                                               padx=5,
                                                                                                               pady=10)


# ==========================================
# PRÁCTICA 2.2: SIMULADOR DE INTEGRIDAD Y ALTERACIÓN DE ARCHIVO
# ==========================================
estado_u2_p2 = {"hash_base": None, "nombre_base": None}


def cargar_practica_u2_p2(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🛡️ Práctica 2.2: Prueba de Integridad y Detección de Modificaciones",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Paso 1: Sube un archivo de texto original para registrar su huella SHA-256 base.\nPaso 2: Edita ese mismo archivo en tu PC, guárdalo y súbelo de nuevo para verificar su integridad.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    lbl_estado = ctk.CTkLabel(f_card, text="Estado actual: Ningún archivo base registrado.",
                              font=("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT)
    lbl_estado.pack(anchor="w", padx=20, pady=15)

    txt_info = ctk.CTkTextbox(f_card, height=120, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT,
                              font=("Consolas", 11))
    txt_info.pack(fill="both", expand=True, padx=20, pady=5)
    txt_info.insert("1.0",
                    "Instrucciones:\n1. Crea un archivo .txt en tu computadora con cualquier texto.\n2. Haz clic en 'Registrar Archivo Original' para calcular su SHA-256.\n3. Abre tu archivo de texto, cámbiale una letra o palabra y guárdalo.\n4. Haz clic en 'Verificar Archivo Modificado'.")
    txt_info.configure(state="disabled")

    f_btns = ctk.CTkFrame(f_card, fg_color="transparent")
    f_btns.pack(fill="x", padx=20, pady=15)

    def calcular_sha256(ruta):
        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def registrar_base():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de texto original",
                                          filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")])
        if not ruta: return
        try:
            nuevo_hash = calcular_sha256(ruta)
            estado_u2_p2["hash_base"] = nuevo_hash
            estado_u2_p2["nombre_base"] = os.path.basename(ruta)
            lbl_estado.configure(text=f"Base Registrada: {estado_u2_p2['nombre_base']}", text_color=COLOR_SUCCESS)
            messagebox.showinfo("Base Registrada",
                                f"Archivo original registrado con éxito.\nSHA-256 Base:\n{nuevo_hash}\n\nAhora edita el archivo en tu PC y presiona 'Verificar Modificación'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def verificar_modificado():
        if not estado_u2_p2["hash_base"]:
            messagebox.showwarning("Atención", "Primero debes registrar el archivo original (Paso 1).")
            return

        ruta = filedialog.askopenfilename(title="Seleccionar archivo para verificar integridad",
                                          filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")])
        if not ruta: return

        try:
            hash_actual = calcular_sha256(ruta)
            hash_base = estado_u2_p2["hash_base"]

            if hash_actual != hash_base:
                messagebox.showerror("Alerta de Fraude / Modificación",
                                     f"⚠️ Este archivo ya no es factible porque fue editado.\n\nHash Base:\n{hash_base}\n\nHash Actual:\n{hash_actual}\n\nResultado: La información ha sido alterada y ya no es confiable.")
            else:
                messagebox.showinfo("Integridad Verificada",
                                    f"✅ El SHA-256 sigue siendo el mismo. La información sigue siendo confiable y no ha sufrido alteraciones.\n\nHash:\n{hash_actual}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(f_btns, text="1️⃣ Registrar Archivo Original (Base)", command=registrar_base, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=220).pack(side="left", padx=5)
    ctk.CTkButton(f_btns, text="2️⃣ Verificar Archivo Modificado", command=verificar_modificado, fg_color="#F77F00",
                  text_color="#05070A", width=220).pack(side="right", padx=5)


# ==========================================
# PRÁCTICA 2.3: GENERADOR DE HASHES Y REPORTE PDF EN DESCARGAS
# ==========================================
def cargar_practica_u2_p3(container):
    limpiar(container)

    ctk.CTkLabel(container, text="🛠️ Laboratorio Práctico 2.3: Generador y Explicador de Hashes (MD5 / SHA-256)",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=(0, 5), anchor="w")
    ctk.CTkLabel(container,
                 text="Calcula las huellas digitales de un archivo y genera un reporte PDF educativo guardado en Descargas.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 10))

    f_input = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    f_input.pack(fill="x", pady=5, ipady=5)

    lbl_ruta = ctk.CTkLabel(f_input, text="Selecciona un archivo de evidencia...", font=("Segoe UI", 11),
                            text_color=COLOR_TEXT_MUTED)
    lbl_ruta.pack(side="left", padx=15, pady=10)

    datos_hashes = {"md5": "", "sha256": "", "archivo": ""}

    txt_salida = ctk.CTkTextbox(container, font=("Consolas", 11), fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT,
                                height=130)
    txt_salida.pack(fill="both", expand=True, pady=5)
    txt_salida.configure(state="disabled")

    def calcular():
        ruta = filedialog.askopenfilename(title="Seleccionar evidencia digital")
        if not ruta: return
        lbl_ruta.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        try:
            h_md5 = hashlib.md5()
            h_sha256 = hashlib.sha256()
            with open(ruta, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    h_md5.update(chunk)
                    h_sha256.update(chunk)

            m_val, s_val = h_md5.hexdigest(), h_sha256.hexdigest()
            datos_hashes["md5"], datos_hashes["sha256"], datos_hashes["archivo"] = m_val, s_val, os.path.basename(ruta)

            txt_salida.configure(state="normal")
            txt_salida.delete("1.0", "end")
            txt_salida.insert("end", f"Archivo: {os.path.basename(ruta)}\n\nMD5    : {m_val}\nSHA-256: {s_val}\n")
            txt_salida.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(f_input, text="Examinar Archivo...", command=calcular, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(side="right", padx=15)

    def exportar_pdf_hashes():
        if not datos_hashes["md5"]:
            messagebox.showwarning("Atención", "Primero calcula los hashes de un archivo.")
            return

        if not REPORTLAB_DISPONIBLE:
            messagebox.showerror("Error", "La librería 'reportlab' no está instalada. Ejecuta: pip install reportlab")
            return

        try:
            nombre_pdf = f"Reporte_Hashes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()

            style_celda = ParagraphStyle(
                'CeldaTabla',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                leading=12,
                textColor=colors.HexColor("#1E293B")
            )
            style_celda_bold = ParagraphStyle(
                'CeldaTablaBold',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=10,
                leading=12,
                textColor=colors.HexColor("#0F172A")
            )

            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("REPORTE TÉCNICO DE INTEGRIDAD - HASHES CRIPTOGRÁFICOS", styles['Heading2']))
            elementos.append(Spacer(1, 10))

            info_tabla = [
                [Paragraph("Archivo Analizado:", style_celda_bold), Paragraph(datos_hashes["archivo"], style_celda)],
                [Paragraph("Hash MD5:", style_celda_bold), Paragraph(datos_hashes["md5"], style_celda)],
                [Paragraph("Hash SHA-256:", style_celda_bold), Paragraph(datos_hashes["sha256"], style_celda)],
                [Paragraph("Fecha de Análisis:", style_celda_bold),
                 Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style_celda)]
            ]

            t = Table(info_tabla, colWidths=[120, 370])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#E2E8F0")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6)
            ]))
            elementos.append(t)
            elementos.append(Spacer(1, 15))

            elementos.append(Paragraph("<b>Explicación Técnica y Conceptual:</b>", styles['Heading3']))
            explicacion = (
                "<b>¿Qué es MD5?</b><br/>"
                "Es un algoritmo de resumen criptográfico que genera una huella digital única de 128 bits (expresada en 32 caracteres hexadecimales). "
                "Aunque hoy en día es vulnerable a ataques de colisión (dos archivos distintos con el mismo hash), sigue siendo útil para verificaciones rápidas de integridad no maliciosa.<br/><br/>"
                "<b>¿Qué es SHA-256?</b><br/>"
                "Pertenece a la familia SHA-2 y produce una firma de 256 bits (64 caracteres hexadecimales). Es altamente seguro, resistente a colisiones y es el estándar de oro en informática forense para garantizar que una evidencia digital no ha sufrido alteraciones."
            )
            elementos.append(Paragraph(explicacion, styles['Normal']))

            doc.build(elementos)
            messagebox.showinfo("Reporte Guardado",
                                f"El reporte PDF de hashes se ha guardado en tu carpeta de Descargas:\n\n{ruta_pdf}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    ctk.CTkButton(container, text="📄 Generar Reporte PDF con Explicación de Hashes (Descargas)",
                  command=exportar_pdf_hashes, font=("Segoe UI", 12, "bold"), fg_color="#2EC4B6", text_color="#05070A",
                  height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 2.4: FORMULARIO ESTÁNDAR DE DICTAMEN PERICIAL Y PDF
# ==========================================
def cargar_practica_u2_p4(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 5))
    ctk.CTkLabel(header, text="📋 Práctica 2.4: Formulario Técnico de Dictamen Pericial", font=("Segoe UI", 15, "bold"),
                 text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(8, 2))
    ctk.CTkLabel(header,
                 text="Llena el formulario con redacción rigurosa y objetiva para emitir el dictamen técnico pericial en PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 8))

    scroll_form = ctk.CTkScrollableFrame(container, fg_color=COLOR_CARD, corner_radius=8, height=300)
    scroll_form.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(scroll_form, text="1. Evidencia Analizada (Ej. Disco Duro / Imagen / Registro):",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=10, pady=(5, 2))
    en_evidencia = ctk.CTkEntry(scroll_form, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_evidencia.pack(fill="x", padx=10, pady=2)
    en_evidencia.insert(0, "Disco Duro Western Digital 1TB (Modelo WD10EZEX)")

    ctk.CTkLabel(scroll_form, text="2. Encontrada en (Ubicación física o lógica exacta):",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=10, pady=(5, 2))
    en_ubicacion = ctk.CTkEntry(scroll_form, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_ubicacion.pack(fill="x", padx=10, pady=2)
    en_ubicacion.insert(0, "Gabinete principal del servidor central del área de finanzas")

    ctk.CTkLabel(scroll_form, text="3. En la zona de (Contexto o departamento):", font=("Segoe UI", 11, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=10, pady=(5, 2))
    en_zona = ctk.CTkEntry(scroll_form, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_zona.pack(fill="x", padx=10, pady=2)
    en_zona.insert(0, "Departamento de Tecnologías de la Información (Edificio C)")

    ctk.CTkLabel(scroll_form, text="4. Hallazgos Técnicos Verificables (Objetivos y sin juicios de valor):",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=10, pady=(5, 2))
    txt_hallazgos = ctk.CTkTextbox(scroll_form, height=60, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    txt_hallazgos.pack(fill="x", padx=10, pady=2)
    txt_hallazgos.insert("1.0",
                         "Se identificaron particiones con formato NTFS y archivos con marcas de borrado lógico en sectores no contiguos.")

    ctk.CTkLabel(scroll_form, text="5. Conclusión Técnica Preliminar:", font=("Segoe UI", 11, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=10, pady=(5, 2))
    txt_concl = ctk.CTkTextbox(scroll_form, height=60, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    txt_concl.pack(fill="x", padx=10, pady=2)
    txt_concl.insert("1.0",
                     "Los datos analizados coinciden con los hashes registrados en el acta inicial, verificando la ausencia de alteraciones maliciosas en el medio.")

    def generar_dictamen_pdf():
        if not REPORTLAB_DISPONIBLE:
            messagebox.showerror("Error", "La librería 'reportlab' no está instalada. Ejecuta: pip install reportlab")
            return

        try:
            nombre_pdf = f"Dictamen_Pericial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("DICTAMEN TÉCNICO PERICIAL INFORMÁTICO", styles['Heading2']))
            elementos.append(Spacer(1, 10))

            texto_cuerpo = (
                f"<b>Fecha de Emisión:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/><br/>"
                f"A solicitud de la autoridad competente, se presenta la evidencia <b>{en_evidencia.get()}</b> "
                f"encontrada en <b>{en_ubicacion.get()}</b> en la zona de <b>{en_zona.get()}</b>.<br/><br/>"
                f"<b>HALLAZGOS TÉCNICOS VERIFICABLES:</b><br/>"
                f"{txt_hallazgos.get('1.0', 'end').strip()}<br/><br/>"
                f"<b>CONCLUSIÓN TÉCNICA PRELIMINAR:</b><br/>"
                f"{txt_concl.get('1.0', 'end').strip()}<br/><br/>"
                "<i>Nota: Este dictamen se basa estrictamente en la evidencia verificable y disponible, evitando juicios de valor u opiniones subjetivas.</i>"
            )

            elementos.append(Paragraph(texto_cuerpo, styles['Normal']))
            elementos.append(Spacer(1, 35))
            elementos.append(Paragraph(
                "__________________________________________<br/>Firma del Perito Informático Forense<br/>Laboratorio Visual Forense - ITTLA",
                styles['Normal']))

            doc.build(elementos)
            messagebox.showinfo("Dictamen Generado",
                                f"El dictamen técnico en PDF se ha guardado en tu carpeta de Descargas:\n\n{ruta_pdf}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    ctk.CTkButton(container, text="📄 Generar Dictamen Pericial en PDF (Descargas)", command=generar_dictamen_pdf,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_ACCENT, text_color="#05070A", height=38).pack(fill="x",
                                                                                                              padx=5,
                                                                                                              pady=5)