import os
import re
import hashlib
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog

# Intentar importar ReportLab para generación de PDFs profesionales
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_DISPONIBLE = True
except ImportError:
    REPORTLAB_DISPONIBLE = False

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

    lbl_msg = ctk.CTkLabel(
        card_modal, text=mensaje, font=ctk.CTkFont("Segoe UI", 12),
        text_color=COLOR_TEXT_LIGHT, justify="left", wraplength=420
    )
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
# PRÁCTICA 4.1: LÍNEA TEMPORAL Y RESPUESTA A INCIDENTES (Archivo Real de Log)
# ==========================================
def cargar_practica_u4_p1(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🚨 Práctica 4.1: Línea Temporal y Respuesta a Incidentes (Archivo Real)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Carga un archivo de registro (.log o .txt) de tu PC para ordenar cronológicamente los eventos del incidente y generar el reporte PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=10)

    lbl_ruta = ctk.CTkLabel(f_file, text="Ningún archivo de bitácora seleccionado...", font=("Segoe UI", 11),
                            text_color=COLOR_TEXT_MUTED)
    lbl_ruta.pack(side="left", padx=5)

    timeline_data = {"ruta": "", "resumen": ""}

    txt_timeline = ctk.CTkTextbox(f_card, height=150, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT,
                                  font=("Consolas", 11))
    txt_timeline.pack(fill="both", expand=True, padx=20, pady=5)
    txt_timeline.insert("1.0", "Selecciona un archivo .log o .txt real de tu computadora para reconstruir su línea temporal...")
    txt_timeline.configure(state="disabled")

    def procesar_timeline():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de log o registro",
                                         filetypes=[("Registros / Texto", "*.log *.txt"), ("Todos los archivos", "*.*")])
        if not ruta:
            return

        timeline_data["ruta"] = ruta
        lbl_ruta.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        try:
            with open(ruta, "r", encoding="utf-8", errors="replace") as f:
                lineas = [ln.strip() for ln in f.readlines() if ln.strip()]

            lineas_ordenadas = sorted(lineas)
            muestra = lineas_ordenadas[:30]
            eventos_fmt = "\n".join(f"[{idx+1:02d}] {ev}" for idx, ev in enumerate(muestra))

            resumen = (
                "--- RECONSTRUCCIÓN CRONOLÓGICA DE INCIDENTE ---\n"
                f"• Archivo fuente: {os.path.basename(ruta)}\n"
                f"• Total de entradas procesadas: {len(lineas)}\n"
                f"• Eventos ordenados (primeros {len(muestra)}):\n{eventos_fmt}"
            )
            timeline_data["resumen"] = resumen

            txt_timeline.configure(state="normal")
            txt_timeline.delete("1.0", "end")
            txt_timeline.insert("end", resumen)
            txt_timeline.configure(state="disabled")
            mostrar_mensaje_hud(container, "✨ Línea Temporal Generada", f"Se ordenaron {len(lineas)} registros del archivo '{os.path.basename(ruta)}'.", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo procesar el archivo: {str(e)}", tipo="error")

    ctk.CTkButton(f_file, text="Examinar Log Real...", command=procesar_timeline, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=170).pack(side="right", padx=5)

    def exportar_pdf_timeline():
        if not timeline_data["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero carga un archivo de registro desde tu computadora.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Timeline_Incidente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("REPORTE DE RESPUESTA A INCIDENTES - LÍNEA TEMPORAL (ARCHIVO REAL)", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(timeline_data["resumen"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Reporte Generado", f"La línea temporal en PDF se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Reporte de Línea Temporal en PDF (Descargas)", command=exportar_pdf_timeline,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 4.2: RASTREO DE IP Y PATRONES EN BITÁCORAS (Archivo Real)
# ==========================================
def cargar_practica_u4_p2(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🌐 Práctica 4.2: Evidencias Analizadas y Rastreo de IP en Bitácoras",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Carga un archivo de bitácora o texto de tu PC, filtra por dirección IP o palabra clave sospechosa y exporta los hallazgos en PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=(10, 5))

    lbl_ruta_ip = ctk.CTkLabel(f_file, text="Ningún archivo cargado...", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED)
    lbl_ruta_ip.pack(side="left", padx=5)

    archivo_ip = {"ruta": "", "contenido": "", "reporte": ""}

    def cargar_bitacora():
        ruta = filedialog.askopenfilename(title="Seleccionar bitácora o archivo de texto",
                                         filetypes=[("Bitácoras / Texto", "*.log *.txt *.csv"), ("Todos los archivos", "*.*")])
        if not ruta:
            return
        archivo_ip["ruta"] = ruta
        lbl_ruta_ip.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            archivo_ip["contenido"] = f.read()
        mostrar_mensaje_hud(container, "✨ Bitácora Cargada", f"Se cargó '{os.path.basename(ruta)}'. Ingresa una IP o término a buscar y presiona 'Rastrear Evidencia'.", tipo="success")

    ctk.CTkButton(f_file, text="Examinar Bitácora...", command=cargar_bitacora, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=160).pack(side="right", padx=5)

    f_filtro = ctk.CTkFrame(f_card, fg_color="transparent")
    f_filtro.pack(fill="x", padx=20, pady=5)

    entry_filtro = ctk.CTkEntry(f_filtro, placeholder_text="Ej. 192.168.1.50, failed, error, admin...",
                                fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, height=35)
    entry_filtro.pack(side="left", fill="x", expand=True, padx=(0, 10))

    txt_ips = ctk.CTkTextbox(f_card, height=130, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=("Consolas", 11))
    txt_ips.pack(fill="both", expand=True, padx=20, pady=5)
    txt_ips.insert("1.0", "Carga un archivo real y ejecuta 'Rastrear Evidencia' para detectar direcciones IP y coincidencias...")
    txt_ips.configure(state="disabled")

    def rastrear_evidencia():
        if not archivo_ip["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero selecciona un archivo de bitácora desde tu PC.", tipo="warning")
            return

        termino = entry_filtro.get().strip().lower()
        lineas = archivo_ip["contenido"].splitlines()
        ips_detectadas = sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", archivo_ip["contenido"])))

        if termino:
            coincidencias = [ln for ln in lineas if termino in ln.lower()]
        else:
            coincidencias = lineas[:25]

        coinc_fmt = "\n".join(f"  • {c}" for c in coincidencias[:25]) if coincidencias else "  [Sin coincidencias para el filtro indicado]"
        ips_fmt = ", ".join(ips_detectadas[:20]) if ips_detectadas else "No se detectaron direcciones IPv4."

        reporte = (
            "--- RASTREO DE EVIDENCIA Y ATRIBUCIÓN DE ORIGEN ---\n"
            f"• Archivo analizado: {os.path.basename(archivo_ip['ruta'])}\n"
            f"• Filtro aplicado: '{termino if termino else 'Sin filtro (primeros 25 registros)'}'\n"
            f"• Direcciones IPv4 identificadas: {ips_fmt}\n"
            f"• Coincidencias halladas: {len(coincidencias)}\n"
            f"• Detalle de registros:\n{coinc_fmt}"
        )
        archivo_ip["reporte"] = reporte

        txt_ips.configure(state="normal")
        txt_ips.delete("1.0", "end")
        txt_ips.insert("end", reporte)
        txt_ips.configure(state="disabled")
        mostrar_mensaje_hud(container, "✨ Rastreo Completado", f"Se hallaron {len(coincidencias)} registros relevantes y {len(ips_detectadas)} IP(s).", tipo="success")

    ctk.CTkButton(f_filtro, text="🔎 Rastrear Evidencia", command=rastrear_evidencia, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=150, height=35).pack(side="right")

    def exportar_pdf_ip():
        if not archivo_ip["reporte"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero ejecuta el rastreo de evidencia sobre el archivo cargado.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Rastreo_Atribucion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("REPORTE FORENSE - EVIDENCIAS ANALIZADAS Y RASTREO DE IP", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(archivo_ip["reporte"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Reporte Generado", f"El reporte de rastreo se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Reporte de Atribución en PDF (Descargas)", command=exportar_pdf_ip,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 4.3: HUELLA SHA-256 Y VALIDACIÓN DE EVIDENCIA ATRIBUIDA (Archivo Real)
# ==========================================
def cargar_practica_u4_p3(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🔐 Práctica 4.3: Validación Criptográfica de Evidencia Atribuida",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Carga un archivo de evidencia real de tu PC para calcular su huella SHA-256, cotejarla con un hash de referencia y exportar el certificado PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(f_card, fg_color="transparent")
    f_file.pack(fill="x", padx=20, pady=(10, 5))

    lbl_ruta_h = ctk.CTkLabel(f_file, text="Ningún archivo de evidencia seleccionado...", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED)
    lbl_ruta_h.pack(side="left", padx=5)

    evidencia_hash = {"ruta": "", "hash_calc": "", "resumen": ""}

    def cargar_y_hashear():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de evidencia para validar integridad")
        if not ruta:
            return
        evidencia_hash["ruta"] = ruta
        lbl_ruta_h.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        evidencia_hash["hash_calc"] = h.hexdigest()
        mostrar_mensaje_hud(container, "✨ Hash Calculado", f"SHA-256 generado:\n{evidencia_hash['hash_calc']}", tipo="success")

    ctk.CTkButton(f_file, text="Examinar Evidencia...", command=cargar_y_hashear, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=160).pack(side="right", padx=5)

    ctk.CTkLabel(f_card, text="Hash SHA-256 de Referencia (opcional para cotejo directo):",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=20, pady=(8, 2))
    entry_hash_ref = ctk.CTkEntry(f_card, placeholder_text="Pega aquí un hash SHA-256 de 64 caracteres para comparar...",
                                  fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=("Consolas", 11))
    entry_hash_ref.pack(fill="x", padx=20, pady=4)

    txt_res_h = ctk.CTkTextbox(f_card, height=110, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=("Consolas", 11))
    txt_res_h.pack(fill="both", expand=True, padx=20, pady=8)
    txt_res_h.insert("1.0", "Carga un archivo y haz clic en 'Cotejar Integridad' para generar el dictamen de autenticidad...")
    txt_res_h.configure(state="disabled")

    def cotejar_integridad():
        if not evidencia_hash["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero selecciona un archivo de tu PC.", tipo="warning")
            return

        ref = entry_hash_ref.get().strip().lower()
        calc = evidencia_hash["hash_calc"].lower()

        if ref:
            coincide = (ref == calc)
            estado_str = "✅ COINCIDE EXACTAMENTE (Evidencia íntegra y sin alteraciones)." if coincide else "❌ NO COINCIDE (Posible alteración o archivo distinto al esperado)."
            tipo_hud = "success" if coincide else "error"
        else:
            estado_str = "ℹ️ Sin hash de referencia ingresado; se registró la huella SHA-256 calculada como línea base."
            tipo_hud = "info"

        resumen = (
            "--- VALIDACIÓN CRIPTOGRÁFICA DE EVIDENCIA ---\n"
            f"• Archivo: {os.path.basename(evidencia_hash['ruta'])}\n"
            f"• SHA-256 Calculado: {calc}\n"
            f"• SHA-256 Referencia: {ref if ref else 'N/A'}\n"
            f"• Resultado: {estado_str}"
        )
        evidencia_hash["resumen"] = resumen

        txt_res_h.configure(state="normal")
        txt_res_h.delete("1.0", "end")
        txt_res_h.insert("end", resumen)
        txt_res_h.configure(state="disabled")
        mostrar_mensaje_hud(container, "🔐 Dictamen de Integridad", estado_str, tipo=tipo_hud)

    ctk.CTkButton(f_card, text="⚖️ Cotejar Integridad", command=cotejar_integridad, fg_color=COLOR_ACCENT,
                  text_color="#05070A", height=35).pack(anchor="e", padx=20, pady=(0, 8))

    def exportar_pdf_hash_u4():
        if not evidencia_hash["resumen"]:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Primero realiza el cotejo de integridad del archivo.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Validacion_Evidencia_U4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("CERTIFICADO DE INTEGRIDAD DE EVIDENCIA ATRIBUIDA", styles['Heading2']))
            elementos.append(Spacer(1, 10))
            elementos.append(Paragraph(evidencia_hash["resumen"].replace("\n", "<br/>"), styles['Normal']))

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Certificado Generado", f"El reporte en PDF se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Certificado de Integridad en PDF (Descargas)", command=exportar_pdf_hash_u4,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 4.4: HALLAZGOS FINALES, ATRIBUCIÓN Y FLAG DEL CASO (Archivo Real + Redacción)
# ==========================================
def cargar_practica_u4_p4(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🚩 Práctica 4.4: Hallazgos Finales, Atribución y Conclusión Técnica (Flag)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Adjunta un archivo de evidencia final de tu PC, redacta tus hallazgos y la Flag/conclusión del caso y genera el dictamen final en PDF.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    scroll_form = ctk.CTkScrollableFrame(container, fg_color=COLOR_CARD, corner_radius=8, height=300)
    scroll_form.pack(fill="both", expand=True, padx=5, pady=5)

    f_file = ctk.CTkFrame(scroll_form, fg_color="transparent")
    f_file.pack(fill="x", padx=15, pady=(10, 5))

    lbl_ev_final = ctk.CTkLabel(f_file, text="Archivo de soporte final: Ninguno seleccionado", font=("Segoe UI", 11),
                                text_color=COLOR_TEXT_MUTED)
    lbl_ev_final.pack(side="left", padx=5)

    soporte_final = {"ruta": "", "sha256": ""}

    def seleccionar_soporte():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de evidencia final")
        if not ruta:
            return
        soporte_final["ruta"] = ruta
        lbl_ev_final.configure(text=f"Archivo: {os.path.basename(ruta)}", text_color=COLOR_TEXT_LIGHT)

        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        soporte_final["sha256"] = h.hexdigest()

    ctk.CTkButton(f_file, text="Examinar Evidencia Final...", command=seleccionar_soporte, fg_color=COLOR_ACCENT,
                  text_color="#05070A", width=170).pack(side="right", padx=5)

    ctk.CTkLabel(scroll_form, text="1. Atribución / Vector o Fuente Identificada:",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=(10, 2))
    en_atribucion = ctk.CTkEntry(scroll_form, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_atribucion.pack(fill="x", padx=15, pady=4)
    en_atribucion.insert(0, "Origen rastreado en bitácoras y evidencia verificada mediante SHA-256")

    ctk.CTkLabel(scroll_form, text="2. Hallazgos Clave y Detalles Técnicos:",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=(10, 2))
    txt_hallazgos = ctk.CTkTextbox(scroll_form, height=75, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    txt_hallazgos.pack(fill="x", padx=15, pady=4)
    txt_hallazgos.insert("1.0", "Se correlacionó la secuencia cronológica de eventos con los registros de acceso y se validó la integridad del archivo de soporte.")

    ctk.CTkLabel(scroll_form, text="3. Flag / Conclusión Técnica Final del Caso:",
                 font=("Segoe UI", 11, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    en_flag = ctk.CTkEntry(scroll_form, fg_color=COLOR_ENTRY_BG, text_color=COLOR_SUCCESS, font=("Consolas", 12, "bold"))
    en_flag.pack(fill="x", padx=15, pady=(4, 12))
    en_flag.insert(0, "FLAG{ATRIBUCION_VERIFICADA_INTEGRIDAD_OK}")

    def generar_dictamen_final_pdf():
        if not soporte_final["ruta"]:
            mostrar_mensaje_hud(container, "⚠️ Evidencia Requerida", "Selecciona primero un archivo real de evidencia de tu computadora.", tipo="warning")
            return
        if not REPORTLAB_DISPONIBLE:
            mostrar_mensaje_hud(container, "❌ Error", "La librería 'reportlab' no está instalada.", tipo="error")
            return

        try:
            nombre_pdf = f"Dictamen_Final_U4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta_pdf = os.path.join(obtener_ruta_descargas(), nombre_pdf)

            doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            elementos = []

            elementos.append(Paragraph("<b>INSTITUTO TECNOLÓGICO DE TLALNEPANTLA (ITTLA)</b>", styles['Heading1']))
            elementos.append(Paragraph("DICTAMEN FINAL DE INVESTIGACIÓN FORENSE - ATRIBUCIÓN Y HALLAZGOS", styles['Heading2']))
            elementos.append(Spacer(1, 10))

            t_data = [
                [Paragraph("<b>Fecha de Emisión:</b>", styles['Normal']), Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), styles['Normal'])],
                [Paragraph("<b>Archivo de Evidencia:</b>", styles['Normal']), Paragraph(os.path.basename(soporte_final["ruta"]), styles['Normal'])],
                [Paragraph("<b>Ruta Completa:</b>", styles['Normal']), Paragraph(soporte_final["ruta"], styles['Normal'])],
                [Paragraph("<b>SHA-256:</b>", styles['Normal']), Paragraph(soporte_final["sha256"], styles['Normal'])],
                [Paragraph("<b>Atribución / Fuente:</b>", styles['Normal']), Paragraph(en_atribucion.get().strip(), styles['Normal'])],
                [Paragraph("<b>Hallazgos Técnicos:</b>", styles['Normal']), Paragraph(txt_hallazgos.get("1.0", "end").strip(), styles['Normal'])],
                [Paragraph("<b>Flag / Conclusión:</b>", styles['Normal']), Paragraph(en_flag.get().strip(), styles['Normal'])]
            ]
            t = Table(t_data, colWidths=[145, 345])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#E2E8F0")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ('PADDING', (0, 0), (-1, -1), 8)
            ]))
            elementos.append(t)

            doc.build(elementos)
            mostrar_mensaje_hud(container, "✨ Dictamen Final Generado", f"El reporte final en PDF se guardó en Descargas:\n\n{ruta_pdf}", tipo="success")
        except Exception as e:
            mostrar_mensaje_hud(container, "❌ Error", f"No se pudo generar el PDF: {str(e)}", tipo="error")

    ctk.CTkButton(container, text="📄 Generar Dictamen Final y Flag en PDF (Descargas)", command=generar_dictamen_final_pdf,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=8)
