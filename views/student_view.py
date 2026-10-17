import os
import sqlite3
import tkinter as tk
import re
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk

# Intentar importar la ruta de DB centralizada o calcularla en su defecto
try:
    from database.db_manager import DB_PATH as RUTA_DB
except ImportError:
    DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

# Importación de herramientas
try:
    from tools.hash_calculator import generar_hash_archivo
except ImportError:
    import hashlib

    def generar_hash_archivo(ruta, algoritmo="sha256"):
        hasher = hashlib.md5() if algoritmo == "md5" else (hashlib.sha1() if algoritmo == "sha1" else hashlib.sha256())
        try:
            with open(ruta, "rb") as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

try:
    from tools.exif_extractor import extraer_metadatos_imagen
except ImportError:
    def extraer_metadatos_imagen(ruta):
        return {"Error": "Módulo tools.exif_extractor no encontrado."}

try:
    from tools.report_generator import generar_reporte_txt
except ImportError:
    def generar_reporte_txt(tipo, user, datos):
        return "reporte.txt", "Error: Módulo report_generator no encontrado."

# --- IMPORTACIÓN DE LAS PRÁCTICAS DE LA UNIDAD 1 ---
try:
    from tools.practicas_u1 import cargar_practica_u1_p1, cargar_practica_u1_p2, cargar_practica_u1_p3, cargar_practica_u1_p4
except ImportError:
    cargar_practica_u1_p1 = cargar_practica_u1_p2 = cargar_practica_u1_p3 = cargar_practica_u1_p4 = None

# ==========================================
# PALETA DE COLORES "HUD FORENSIC / HIGH-TECH"
# ==========================================
COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_ACCENT_HOVER = "#00C4D4"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BORDER = "#1E293B"
COLOR_DANGER = "#E63946"
COLOR_DANGER_HOVER = "#D62828"

# ==========================================
# BARRA DE TÍTULO PERSONALIZADA
# ==========================================
def crear_barra_titulo(ventana, bg_color):
    barra_titulo = ctk.CTkFrame(ventana, height=35, fg_color=bg_color, corner_radius=0)
    barra_titulo.pack(side="top", fill="x")
    barra_titulo.pack_propagate(False)

    btn_cerrar = ctk.CTkButton(barra_titulo, text="✕", font=("Segoe UI", 14), width=45, height=35, 
                               fg_color="transparent", hover_color="#E81123", text_color="white", 
                               corner_radius=0, command=ventana.quit)
    btn_cerrar.pack(side="right")

    def toggle_maximizar():
        es_fullscreen = ventana.attributes('-fullscreen')
        ventana.attributes('-fullscreen', not es_fullscreen)
        
    btn_max = ctk.CTkButton(barra_titulo, text="🗗", font=("Segoe UI", 15), width=45, height=35, 
                            fg_color="transparent", hover_color=COLOR_BORDER, text_color="white", 
                            corner_radius=0, command=toggle_maximizar)
    btn_max.pack(side="right")

    btn_min = ctk.CTkButton(barra_titulo, text="—", font=("Segoe UI", 15, "bold"), width=45, height=35, 
                            fg_color="transparent", hover_color=COLOR_BORDER, text_color="white", 
                            corner_radius=0, command=ventana.iconify)
    btn_min.pack(side="right")


# ==========================================
# CONTENIDO TEÓRICO COMPLETO DETALLADO
# ==========================================
TEORIA_DETALLADA = {
    1: [
        ("1.1 Conceptos generales",
         "La informática forense es la disciplina científica y pericial dedicada a la identificación, preservación, extracción, análisis y presentación de evidencias digitales almacenadas en dispositivos electrónicos.\n\n"
         "• Evidencia Digital: Cualquier información en formato binario que pueda ser utilizada para probar un hecho en un proceso judicial o administrativo.\n"
         "• Cadena de Custodia: Proceso riguroso que documenta cronológicamente la extracción, custodia, control, transferencia, análisis y disposición de la evidencia física o digital.\n"
         "• Hash de Integridad: Firma matemática unívoca (MD5, SHA-256) que garantiza que un archivo no ha sufrido modificaciones desde su extracción."),

        ("1.2 Importancia",
         "En el contexto actual de digitalización masiva y cibercrimen, la informática forense cumple un papel determinante:\n\n"
         "1. Garantizar la Inadmisibilidad de Pruebas Alteradas: Permite validar legalmente los hallazgos ante tribunales.\n"
         "2. Respuesta a Incidentes de Seguridad: Ayuda a las organizaciones a determinar la causa raíz, el alcance y el impacto de un ataque informático (ransomware, fuga de datos, accesos no autorizados).\n"
         "3. Recuperación de Evidencia Borrada o Cifrada: Permite reconstruir eventos delictivos a partir de fragmentos en memoria RAM, disco no asignado o metadatos escondidos."),

        ("1.3 Situación actual",
         "El panorama contemporáneo de la informática forense enfrenta múltiples retos emergentes:\n\n"
         "• Entornos en la Nube: La dispersión geográfica de los datos dificulta la adquisición física de los soportes.\n"
         "• Cifrado de Disco Completo (BitLocker, LUKS): Requiere técnicas de análisis en vivo (Live Forensics) y captura de memoria volátil antes del apagado del equipo.\n"
         "• Internet de las Cosas (IoT) y Dispositivos Móviles: Multiplicación de fuentes de evidencia con formatos propietarios y sistemas operativos heterogéneos."),

        ("1.4 Principios fundamentales",
         "Los pilares éticos y procesales que rigen cualquier investigación forense son:\n\n"
         "1. Principio de Mínima Intervención: Trabajar siempre sobre imágenes forenses (copias bit a bit) y nunca sobre la evidencia original.\n"
         "2. Principio de Locard en el Ámbito Digital: Todo contacto deja un rastro. Cualquier interacción con un sistema informático modifica de alguna forma su estado (logs, registros, marcas de tiempo).\n"
         "3. Auditabilidad y Repetibilidad: Los procedimientos aplicados por un perito deben estar documentados de forma tal que otro especialista pueda replicarlos y obtener exactamente los mismos resultados."),

        ("1.5 Estándares y Normativas",
         "Las investigaciones deben alinearse a marcos regulatorios y normas técnicas reconocidas internacionalmente para asegurar su validez procesal."),

        ("1.5.1 Nivel nacional",
         "• Código Nacional de Procedimientos Penales (CNPP): Contempla los requisitos para la incorporación de prueba documental y técnica en juicios oralidades.\n"
         "• Protocolos de la Guardia Nacional / CERT MX: Guías técnicas para el manejo y aseguramiento de indicios digitales en la escena del delito."),

        ("1.5.2 Nivel internacional",
         "• ISO/IEC 27037: Estándar internacional con directrices para la identificación, recolección, adquisición y preservación de evidencia digital.\n"
         "• RFC 3227: Guía de mejores prácticas para la recolección y archivo de evidencia volátil (memoria RAM, conexiones de red activas).\n"
         "• NIST SP 800-86: Guía del Instituto Nacional de Estándares y Tecnología de EE. UU. para la integración de técnicas forenses en la respuesta a incidentes.")
    ]
}

def obtener_temas_bd():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, unidad, titulo, contenido_teorico FROM temas ORDER BY unidad ASC")
    temas = cursor.fetchall()
    conexion.close()
    return temas

def obtener_preguntas_unidad(tema_id):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta FROM preguntas WHERE tema_id = ?",
        (tema_id,))
    preguntas = cursor.fetchall()
    conexion.close()
    return preguntas

def guardar_calificacion(usuario, tema_id, puntaje):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = ?", (usuario,))
    user = cursor.fetchone()
    if user:
        cursor.execute("INSERT INTO calificaciones (alumno_id, tema_id, puntaje) VALUES (?, ?, ?)",
                       (user[0], tema_id, puntaje))
        conexion.commit()
    conexion.close()

def obtener_calificaciones_usuario(usuario):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("""
                   SELECT t.unidad, t.titulo, c.puntaje, c.fecha
                   FROM calificaciones c
                            JOIN usuarios u ON c.alumno_id = u.id
                            JOIN temas t ON c.tema_id = t.id
                   WHERE u.nombre_usuario = ?
                   ORDER BY c.fecha DESC
                   """, (usuario,))
    registros = cursor.fetchall()
    conexion.close()
    return registros


# ==========================================
# INTERFAZ GRÁFICA DEL ESTUDIANTE
# ==========================================
def abrir_panel_alumno(usuario):
    ventana = ctk.CTkToplevel()
    ventana.title(f"LAB VISUAL FORENSE - Módulo Guiado ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(fg_color=COLOR_BG_DARK)

    # --- INSTANCIAR LA BARRA DE TÍTULO ---
    crear_barra_titulo(ventana, COLOR_BG_DARK)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=30)
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("Treeview.Heading", background=COLOR_CARD, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 10, "bold"), borderwidth=0)

    # Layout Principal: Sidebar (Izquierda) + Contenido (Derecha)
    container_main = ctk.CTkFrame(ventana, fg_color=COLOR_BG_DARK)
    container_main.pack(fill="both", expand=True, padx=20, pady=20)

    # -------------------------------------------------------------
    # SIDEBAR: LISTA DEL TEMARIO
    # -------------------------------------------------------------
    sidebar = ctk.CTkFrame(container_main, fg_color=COLOR_CARD, width=320, corner_radius=10)
    sidebar.pack(side="left", fill="y", padx=(0, 15))
    sidebar.pack_propagate(False)

    ctk.CTkLabel(sidebar, text="📚 TEMARIO DEL CURSO", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(
        pady=(20, 10), padx=15, anchor="w")

    # Listbox mantenido por compatibilidad de eventos
    listbox_temas = tk.Listbox(sidebar, bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectbackground=COLOR_BORDER,
                               selectforeground=COLOR_ACCENT, font=("Segoe UI", 11), bd=0, highlightthickness=0)
    listbox_temas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    temas = obtener_temas_bd()
    for t in temas:
        listbox_temas.insert("end", f" Unidad {t[1]}: {t[2]}")

    btn_cerrar = ctk.CTkButton(sidebar, text="CERRAR SESIÓN", command=ventana.quit, font=ctk.CTkFont("Segoe UI", 12, "bold"),
                               fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT, cursor="hand2")
    btn_cerrar.pack(fill="x", padx=15, pady=15, ipady=5)

    # -------------------------------------------------------------
    # PANEL DERECHO: CONTENIDO DEL TEMA
    # -------------------------------------------------------------
    panel_derecho = ctk.CTkFrame(container_main, fg_color=COLOR_CARD, corner_radius=10)
    panel_derecho.pack(side="right", fill="both", expand=True)

    lbl_titulo_tema = ctk.CTkLabel(panel_derecho, text="Selecciona un tema del temario para comenzar",
                                   font=ctk.CTkFont("Segoe UI", 18, "bold"), text_color=COLOR_TEXT_LIGHT)
    lbl_titulo_tema.pack(pady=(20, 10), padx=25, anchor="w")

    sub_pestanas = ctk.CTkTabview(panel_derecho, fg_color=COLOR_ENTRY_BG, segmented_button_selected_color=COLOR_BORDER,
                                  segmented_button_selected_hover_color=COLOR_CARD, segmented_button_unselected_color=COLOR_CARD,
                                  text_color=COLOR_TEXT_MUTED, corner_radius=10)
    sub_pestanas.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    tab_teoria_name = "📖 1. Explicación"
    tab_quiz_name = "📝 2. Cuestionario"
    tab_practica_name = "🛠️ 3. Práctica Aplicada"
    tab_historial_name = "📊 4. Mis Calificaciones"

    sub_pestanas.add(tab_teoria_name)
    sub_pestanas.add(tab_quiz_name)
    sub_pestanas.add(tab_practica_name)
    sub_pestanas.add(tab_historial_name)

    # --- PASO 1: TEORÍA Y EXPLICACIÓN ---
    tab_teoria = sub_pestanas.tab(tab_teoria_name)

    area_teoria = ctk.CTkTextbox(tab_teoria, wrap="word", font=ctk.CTkFont("Segoe UI", 14), fg_color=COLOR_CARD,
                                 text_color=COLOR_TEXT_LIGHT, border_width=0, corner_radius=10)
    area_teoria.pack(fill="both", expand=True, padx=15, pady=15)

    # Etiquetas de formato en CTkTextbox (Corregido sin FONT para evitar AttributeError)
    area_teoria.tag_config("subtitulo", foreground=COLOR_ACCENT)
    area_teoria.tag_config("subsubtitulo", foreground="#00C4D4")
    area_teoria.tag_config("cuerpo", foreground=COLOR_TEXT_LIGHT)

    # --- PASO 2: CUESTIONARIO DE PREGUNTAS ---
    tab_quiz = sub_pestanas.tab(tab_quiz_name)
    scrollable_quiz_inner = ctk.CTkScrollableFrame(tab_quiz, fg_color="transparent")
    scrollable_quiz_inner.pack(fill="both", expand=True, padx=15, pady=15)

    # --- PASO 3: PRÁCTICA APLICADA ---
    tab_practica = sub_pestanas.tab(tab_practica_name)
    menu_practicas = ctk.CTkFrame(tab_practica, fg_color="transparent")
    menu_practicas.pack(fill="x", padx=15, pady=(15, 0))

    container_practica = ctk.CTkFrame(tab_practica, fg_color="transparent")
    container_practica.pack(fill="both", expand=True, padx=15, pady=15)

    # --- PASO 4: HISTORIAL DE CALIFICACIONES ---
    tab_historial = sub_pestanas.tab(tab_historial_name)

    f_hist_tbl = ctk.CTkFrame(tab_historial, fg_color="transparent")
    f_hist_tbl.pack(fill="both", expand=True, padx=15, pady=15)

    tabla_historial = ttk.Treeview(f_hist_tbl, columns=("u", "t", "p", "f"), show="headings", height=10)
    tabla_historial.heading("u", text="Unidad")
    tabla_historial.heading("t", text="Título del Tema")
    tabla_historial.heading("p", text="Calificación")
    tabla_historial.heading("f", text="Fecha de Realización")
    tabla_historial.column("u", width=80, anchor="center")
    tabla_historial.column("t", width=250, anchor="w")
    tabla_historial.column("p", width=100, anchor="center")
    tabla_historial.column("f", width=180, anchor="center")
    tabla_historial.pack(side="left", fill="both", expand=True)

    scroll_hist = ctk.CTkScrollbar(f_hist_tbl, orientation="vertical", command=tabla_historial.yview)
    tabla_historial.configure(yscrollcommand=scroll_hist.set)
    scroll_hist.pack(side="right", fill="y")

    def actualizar_tabla_historial():
        for item in tabla_historial.get_children():
            tabla_historial.delete(item)
        registros = obtener_calificaciones_usuario(usuario)
        for r in registros:
            tabla_historial.insert("", "end", values=(f"Unidad {r[0]}", r[1], f"{r[2]} / 100", r[3]))

    actualizar_tabla_historial()

    # Variables globales de estado del tema activo
    tema_activo = {"id": None, "unidad": None, "titulo": ""}
    respuestas_usuario = {}
    preguntas_actuales = []

    # -------------------------------------------------------------
    # CONSTRUCTORES DE VISTAS PRÁCTICAS
    # -------------------------------------------------------------
    def cargar_practica_hashes(parent):
        for w in parent.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="PRÁCTICA 2.2: VERIFICACIÓN DE HASHES Y CADENA DE CUSTODIA", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))

        ruta_var = tk.StringVar()
        res_var = tk.StringVar()

        def seleccionar():
            arch = filedialog.askopenfilename()
            if arch:
                ruta_var.set(arch)

        def calcular():
            if not ruta_var.get():
                messagebox.showwarning("Atención", "Selecciona un archivo.")
                return
            res = generar_hash_archivo(ruta_var.get(), combo_algo.get().lower())
            res_var.set(res)

        def exportar():
            if not res_var.get():
                messagebox.showwarning("Atención", "Calcula un hash primero.")
                return
            datos = {"Archivo": os.path.basename(ruta_var.get()), "Ruta": ruta_var.get(), "Algoritmo": combo_algo.get(), "Hash": res_var.get()}
            nom, txt = generar_reporte_txt("HASH_INTEGRIDAD", usuario, datos)
            dest = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nom)
            if dest:
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(txt)
                messagebox.showinfo("Éxito", "Reporte guardado correctamente.")

        frame_f = ctk.CTkFrame(card, fg_color="transparent")
        frame_f.pack(pady=10)
        
        btn_b = ctk.CTkButton(frame_f, text="SELECCIONAR ARCHIVO", command=seleccionar, fg_color=COLOR_BORDER, hover_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_b.pack(side="left", padx=5)
        
        entry_r = ctk.CTkEntry(frame_f, textvariable=ruta_var, font=ctk.CTkFont("Segoe UI", 12), width=400, fg_color=COLOR_CARD, text_color=COLOR_TEXT_MUTED, border_width=0)
        entry_r.pack(side="left", padx=5)

        combo_algo = ctk.CTkComboBox(card, values=["SHA256", "MD5", "SHA1"], state="readonly", font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
        combo_algo.set("SHA256")
        combo_algo.pack(pady=10)

        btn_c = ctk.CTkButton(card, text="CALCULAR HASH", command=calcular, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_c.pack(pady=10)

        entry_res = ctk.CTkEntry(card, textvariable=res_var, font=ctk.CTkFont("Consolas", 14, "bold"), fg_color=COLOR_CARD, text_color=COLOR_ACCENT, border_width=0, justify="center", width=500)
        entry_res.pack(pady=10)

        btn_exp = ctk.CTkButton(card, text="📄 EXPORTAR REPORTE", command=exportar, fg_color=COLOR_BORDER, hover_color=COLOR_ENTRY_BG, text_color=COLOR_ACCENT, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_exp.pack(pady=15)

    def cargar_practica_exif(parent):
        for w in parent.winfo_children():
            w.destroy()

        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="PRÁCTICA 3.1: EXTRACTOR DE METADATOS Y CABECERAS EXIF", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(15, 10))

        ruta_img_var = tk.StringVar()
        ultimo_res = {}

        def seleccionar():
            arch = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.tiff")])
            if arch:
                ruta_img_var.set(arch)

        def analizar():
            if not ruta_img_var.get():
                messagebox.showwarning("Atención", "Selecciona una imagen.")
                return
            for item in tabla.get_children():
                tabla.delete(item)
            res = extraer_metadatos_imagen(ruta_img_var.get())
            ultimo_res.clear()
            ultimo_res.update(res)
            for k, v in res.items():
                if k == "EXIF" and isinstance(v, dict):
                    tabla.insert("", "end", values=("--- ETIQUETAS EXIF ---", "------------------"))
                    for sub_k, sub_v in v.items():
                        tabla.insert("", "end", values=(f"EXIF: {sub_k}", sub_v))
                else:
                    tabla.insert("", "end", values=(k, v))

        def exportar():
            if not ultimo_res:
                messagebox.showwarning("Atención", "Analiza una imagen primero.")
                return
            lineas = [f"{k}: {v}" for k, v in ultimo_res.items() if k != "EXIF"]
            if "EXIF" in ultimo_res and isinstance(ultimo_res["EXIF"], dict):
                lineas.append("ETIQUETAS EXIF:")
                for ek, ev in ultimo_res["EXIF"].items():
                    lineas.append(f"  - {ek}: {ev}")
            nom, txt = generar_reporte_txt("METADATOS_EXIF", usuario, lineas)
            dest = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nom)
            if dest:
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(txt)
                messagebox.showinfo("Éxito", "Reporte guardado correctamente.")

        frame_top = ctk.CTkFrame(card, fg_color="transparent")
        frame_top.pack(fill="x", padx=10, pady=5)

        btn_b = ctk.CTkButton(frame_top, text="SELECCIONAR IMAGEN", command=seleccionar, fg_color=COLOR_BORDER, hover_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_b.pack(side="left", padx=5)
        
        entry_r = ctk.CTkEntry(frame_top, textvariable=ruta_img_var, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, text_color=COLOR_TEXT_MUTED, border_width=0)
        entry_r.pack(side="left", fill="x", expand=True, padx=10)
        
        btn_a = ctk.CTkButton(frame_top, text="ANALIZAR", command=analizar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_a.pack(side="right", padx=5)

        tabla_frame = ctk.CTkFrame(card, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tabla = ttk.Treeview(tabla_frame, columns=("p", "v"), show="headings", height=8)
        tabla.heading("p", text="Propiedad")
        tabla.heading("v", text="Valor Extraído")
        tabla.column("p", width=200)
        tabla.column("v", width=450)
        tabla.pack(side="left", fill="both", expand=True)

        scroll_tbl = ctk.CTkScrollbar(tabla_frame, orientation="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_tbl.set)
        scroll_tbl.pack(side="right", fill="y")

        btn_e = ctk.CTkButton(card, text="📄 EXPORTAR REPORTE EXIF", command=exportar, fg_color=COLOR_BORDER, hover_color=COLOR_ENTRY_BG, text_color=COLOR_ACCENT, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_e.pack(pady=(0, 10))

    def cargar_practica_windows_logs(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="PRÁCTICA 4.2: ANÁLISIS DE REGISTROS DE EVENTOS DE WINDOWS", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(15, 10))

        instruccion = (
            "Analiza el fragmento de registros de eventos extraídos de la máquina comprometida.\n"
            "Identifica el Event ID clave que revela la alteración de la seguridad o persistencia del atacante."
        )
        ctk.CTkLabel(card, text=instruccion, font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT, justify="left", wraplength=650).pack(pady=5)

        txt_logs = ctk.CTkTextbox(card, height=130, width=650, fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT, border_width=0, font=ctk.CTkFont("Consolas", 12))
        txt_logs.pack(pady=10)
        
        logs_simulados = (
            "[10:12:04] Event ID: 4624 - An account was successfully logged on. User: SYSTEM\n"
            "[10:15:22] Event ID: 4625 - An account failed to log on. User: Administrator (Password incorrect)\n"
            "[10:15:28] Event ID: 4625 - An account failed to log on. User: Administrator (Password incorrect)\n"
            "[10:20:01] Event ID: 4720 - A user account was created. TargetAccount: 'backdoor_admin'\n"
            "[10:25:40] Event ID: 4672 - Special privileges assigned to new logon. User: backdoor_admin\n"
        )
        txt_logs.insert(tk.END, logs_simulados)
        txt_logs.configure(state="disabled")

        ctk.CTkLabel(card, text="¿Cuál es el Event ID crítico que evidencia la creación de una cuenta no autorizada?", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=5)

        var_respuesta = tk.StringVar(value="")
        opciones = [
            ("4624 - Inicio de sesión exitoso", "4624"),
            ("4625 - Fallo de inicio de sesión masivo", "4625"),
            ("4720 - Creación de una cuenta de usuario", "4720"),
            ("4672 - Asignación de privilegios especiales", "4672")
        ]

        for texto, val in opciones:
            ctk.CTkRadioButton(card, text=texto, variable=var_respuesta, value=val, font=ctk.CTkFont("Segoe UI", 12), 
                               fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)

        def verificar():
            seleccion = var_respuesta.get()
            if seleccion == "4720":
                messagebox.showinfo("¡Correcto!", "¡Excelente análisis forense! El Event ID 4720 confirma que se creó la cuenta 'backdoor_admin', evidenciando el mecanismo de persistencia del atacante.")
            elif seleccion == "":
                messagebox.showwarning("Atención", "Por favor selecciona una opción de la lista.")
            else:
                messagebox.showerror("Incorrecto", "Ese evento muestra otra actividad, pero no es el indicador principal de la creación de la cuenta maliciosa.")

        btn_verificar = ctk.CTkButton(card, text="VERIFICAR HALLAZGO", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold"))
        btn_verificar.pack(pady=15)

    def cargar_practica_u2_p1(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 2.1: IDENTIFICACIÓN DE EVIDENCIA Y VOLATILIDAD", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Escenario: Llegas a una escena y encuentras una PC encendida, un router activo y varias memorias USB.", font=ctk.CTkFont("Segoe UI", 12, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=5)
        ctk.CTkLabel(card, text="Según el RFC 3227, ¿qué evidencia debes recolectar y documentar PRIMERO por su alta volatilidad?", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        var_resp = tk.StringVar(value="")
        opciones = [("A) El disco duro externo guardado en un cajón.", "C"), ("B) La memoria RAM de la PC encendida.", "A"), ("C) Las memorias USB desconectadas sobre la mesa.", "B")]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "A": messagebox.showinfo("Correcto", "Excelente. La RAM es altamente volátil y debe volcarse antes de que el equipo pierda energía.")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona una opción.")
            else: messagebox.showerror("Incorrecto", "Revisa el orden de volatilidad del RFC 3227. Esa evidencia es persistente.")
        ctk.CTkButton(card, text="VERIFICAR", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u2_p3(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 2.3: REGISTRO DE CADENA DE CUSTODIA", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Completa el formulario legal básico para preservar una evidencia digital:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT).pack(pady=5)
        
        frame_form = ctk.CTkFrame(card, fg_color="transparent")
        frame_form.pack(pady=10)
        
        ctk.CTkLabel(frame_form, text="Nombre del Recolector:", text_color=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="e", pady=10, padx=10)
        e1 = ctk.CTkEntry(frame_form, fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT, border_width=0, width=300)
        e1.grid(row=0, column=1, pady=10)
        
        ctk.CTkLabel(frame_form, text="Descripción del Dispositivo:", text_color=COLOR_TEXT_MUTED).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        e2 = ctk.CTkEntry(frame_form, fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT, border_width=0, width=300)
        e2.grid(row=1, column=1, pady=10)
        
        ctk.CTkLabel(frame_form, text="Firma Hash (SHA-256):", text_color=COLOR_TEXT_MUTED).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        e3 = ctk.CTkEntry(frame_form, fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT, border_width=0, width=300)
        e3.grid(row=2, column=1, pady=10)

        def generar():
            if not e1.get() or not e2.get() or not e3.get(): messagebox.showwarning("Error", "Todos los campos de la Cadena de Custodia son obligatorios legalmente.")
            else: messagebox.showinfo("Éxito", f"Cadena de Custodia generada correctamente para el dispositivo:\n{e2.get()}")
        ctk.CTkButton(card, text="GENERAR FORMATO LEGAL", command=generar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u2_p4(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 2.4: ESTRUCTURA DEL INFORME PERICIAL", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Identifica el orden metodológico correcto de las secciones de un informe técnico pericial:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        var_resp = tk.StringVar(value="")
        opciones = [
            ("A) Conclusiones -> Objetivos -> Hallazgos -> Metodología", "A"),
            ("B) Objetivos -> Metodología -> Hallazgos -> Conclusiones", "B"),
            ("C) Hallazgos -> Conclusiones -> Objetivos -> Metodología", "C")
        ]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "B": messagebox.showinfo("Correcto", "¡Exacto! El informe debe iniciar planteando el objetivo, explicar el método usado, mostrar la evidencia encontrada y concluir lógicamente.")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona una opción.")
            else: messagebox.showerror("Incorrecto", "Un informe pericial perdería validez si concluye antes de explicar la metodología y los hallazgos.")
        ctk.CTkButton(card, text="VALIDAR ESTRUCTURA", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u3_p2(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 3.2: ANÁLISIS DE TRÁFICO (WIRESHARK SIMULATOR)", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(15, 5))
        ctk.CTkLabel(card, text="Analiza el siguiente volcado de tráfico HTTP sin cifrar y encuentra la contraseña filtrada.", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(pady=5)
        
        txt_logs = ctk.CTkTextbox(card, height=110, width=550, fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT, border_width=0, font=ctk.CTkFont("Consolas", 12))
        txt_logs.pack(pady=10)
        txt_logs.insert(tk.END, "Frame 41: GET /index.html HTTP/1.1\nFrame 42: POST /login.php HTTP/1.1\n          Host: 192.168.1.10\n          Form item: 'username' = 'admin'\n          Form item: 'password' = 's3cr3t_f0r3ns1c'\nFrame 43: HTTP/1.1 302 Found")
        txt_logs.configure(state="disabled")
        
        ctk.CTkLabel(card, text="Ingresa la contraseña descubierta:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(pady=5)
        e_pass = ctk.CTkEntry(card, fg_color=COLOR_CARD, text_color=COLOR_ACCENT, border_width=0, width=300, justify="center", font=ctk.CTkFont("Consolas", 14))
        e_pass.pack(pady=5)
        
        def verificar():
            if e_pass.get().strip() == "s3cr3t_f0r3ns1c": messagebox.showinfo("Correcto", "¡Contraseña interceptada con éxito! Esto demuestra el peligro de usar HTTP sin cifrar.")
            else: messagebox.showerror("Incorrecto", "Esa no es la contraseña filtrada en el paquete POST.")
        ctk.CTkButton(card, text="EXTRAER DATO", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=15)

    def cargar_practica_u3_p3(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 3.3: TALLER DE FILE CARVING", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Para recuperar un archivo de imagen borrado desde el espacio no asignado (slack space),\ndebes buscar su Firma Hexadecimal (Magic Number) en la cabecera.", font=ctk.CTkFont("Segoe UI", 12, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=5)
        ctk.CTkLabel(card, text="¿Cuál es el Magic Number característico de un archivo JPEG?", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        var_resp = tk.StringVar(value="")
        opciones = [("A) 4D 5A (Cabecera MZ - Ejecutable Windows)", "A"), ("B) 25 50 44 46 (Cabecera %PDF - Documento)", "B"), ("C) FF D8 FF E0 (Cabecera JPEG Standard)", "C")]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Consolas", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "C": messagebox.showinfo("Correcto", "¡File Carving Exitoso! FF D8 FF E0 marca el inicio de una imagen JPEG recuperable.")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona una firma hexadecimal.")
            else: messagebox.showerror("Incorrecto", "Ese magic number pertenece a otro tipo de archivo.")
        ctk.CTkButton(card, text="APLICAR CARVING", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u3_p4(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 3.4: ANÁLISIS DE BASE DE DATOS SQLITE", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Has montado la base de datos 'msgstore.db' extraída de un teléfono móvil incautado.", font=ctk.CTkFont("Segoe UI", 12, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=5)
        ctk.CTkLabel(card, text="¿Qué instrucción SQL te permite visualizar TODOS los mensajes de la tabla 'messages_backup' sin alterarlos?", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        var_resp = tk.StringVar(value="")
        opciones = [("A) DROP TABLE messages_backup;", "A"), ("B) SELECT * FROM messages_backup;", "B"), ("C) UPDATE messages_backup SET status='read';", "C")]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Consolas", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "B": messagebox.showinfo("Consulta Exitosa", "Correcto. El comando SELECT extrae y visualiza la información de forma segura y en modo lectura.")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona un comando.")
            else: messagebox.showerror("Peligro Forense", "¡Comando Destructivo! Ese comando alteraría o eliminaría la evidencia original de la base de datos.")
        ctk.CTkButton(card, text="EJECUTAR QUERY", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u4_p1(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 4.1: SIMULADOR DE TRIAGE E INCIDENTES", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Escenario: Suena la alarma corporativa. Varios servidores muestran un mensaje de cifrado por Ransomware.", font=ctk.CTkFont("Segoe UI", 12, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=5)
        ctk.CTkLabel(card, text="¿Cuál es la medida de contención (Triage) inicial más crítica para frenar el ataque sin destruir RAM?", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        var_resp = tk.StringVar(value="")
        opciones = [("A) Desconectar inmediatamente los cables de red y apagar interfaces Wi-Fi.", "A"), ("B) Apagar todos los servidores desde el botón de encendido.", "B"), ("C) Formatear los discos para borrar el malware.", "C")]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "A": messagebox.showinfo("Contención Exitosa", "¡Correcto! Aislar lógicamente el equipo de la red frena la propagación del Ransomware y mantiene viva la memoria RAM para extraer las claves de cifrado.")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona una opción de Triage.")
            else: messagebox.showerror("Error Crítico", "Esa acción destruiría evidencia vital (RAM) o eliminaría datos corporativos irreversiblemente.")
        ctk.CTkButton(card, text="APLICAR MEDIDA", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u4_p3(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 4.3: LÍNEA DE TIEMPO (TIMELINE ANALYSIS)", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Se han extraído 3 registros de sistemas distintos con las siguientes marcas de tiempo. Ordena la secuencia del ataque:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        txt_logs = ctk.CTkTextbox(card, height=80, width=500, fg_color=COLOR_CARD, text_color=COLOR_TEXT_MUTED, border_width=0, font=ctk.CTkFont("Consolas", 12))
        txt_logs.pack(pady=5)
        txt_logs.insert(tk.END, "Log 1 (Firewall): [14:05:00] Bloqueo de escaneo de puertos.\nLog 2 (Sistema):  [14:15:30] Creación de tarea programada.\nLog 3 (Web DB):   [14:10:12] Inyección SQL exitosa.")
        txt_logs.configure(state="disabled")

        var_resp = tk.StringVar(value="")
        opciones = [
            ("A) Escaneo -> Tarea Programada -> Inyección SQL", "A"),
            ("B) Escaneo -> Inyección SQL -> Tarea Programada", "B"),
            ("C) Inyección SQL -> Tarea Programada -> Escaneo", "C")
        ]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "B": messagebox.showinfo("Timeline Correcto", "¡Exacto! El atacante primero escaneó la red (14:05), luego vulneró la web (14:10) y finalmente implantó persistencia (14:15).")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona una secuencia.")
            else: messagebox.showerror("Incorrecto", "Revisa el orden cronológico estricto de los logs.")
        ctk.CTkButton(card, text="VALIDAR TIMELINE", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    def cargar_practica_u4_p4(parent):
        for w in parent.winfo_children(): w.destroy()
        card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(card, text="PRÁCTICA 4.4: ATRIBUCIÓN Y HUELLAS (IoC)", font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
        ctk.CTkLabel(card, text="Dentro de la inteligencia de amenazas (Threat Intelligence), un IoC sirve para identificar software o actores maliciosos.", font=ctk.CTkFont("Segoe UI", 12, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=5)
        ctk.CTkLabel(card, text="¿Cuál de los siguientes ejemplos es un Indicador de Compromiso (IoC) técnico válido?", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(pady=15)
        
        var_resp = tk.StringVar(value="")
        opciones = [("A) El modelo físico del teclado utilizado en la oficina.", "A"), ("B) La firma hash SHA-256 de un archivo ejecutable no reconocido.", "B"), ("C) El sistema operativo Windows 10.", "C")]
        for t, v in opciones:
            ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=100, pady=5)
        
        def verificar():
            if var_resp.get() == "B": messagebox.showinfo("Atribución Correcta", "¡Correcto! Una firma Hash única asociada a un malware es un IoC clave para rastrear y atribuir ataques en ciberseguridad.")
            elif not var_resp.get(): messagebox.showwarning("Aviso", "Selecciona una opción.")
            else: messagebox.showerror("Incorrecto", "Un IoC debe ser una huella digital técnica y específica de una amenaza, no hardware general o sistemas genéricos.")
        ctk.CTkButton(card, text="IDENTIFICAR IoC", command=verificar, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(pady=20)

    # -------------------------------------------------------------
    # EVENTO AL SELECCIONAR UN TEMA EN LA LISTA
    # -------------------------------------------------------------
    def cargar_detalle_tema(event):
        seleccion = listbox_temas.curselection()
        if not seleccion:
            return

        idx = seleccion[0]
        t = temas[idx]
        tema_activo["id"] = t[0]
        tema_activo["unidad"] = t[1]
        tema_activo["titulo"] = t[2]

        lbl_titulo_tema.configure(text=f"UNIDAD {t[1]}: {t[2]}")

        # 1. Cargar Teoría Formateada con Subtemas
        area_teoria.configure(state="normal")
        area_teoria.delete("1.0", tk.END)

        contenido_bd = t[3]
        num_unidad = t[1]

        if contenido_bd and contenido_bd.strip():
            for linea in contenido_bd.split('\n'):
                if re.match(r'^\d+\.\d+', linea.strip()):
                    tag = "subsubtitulo" if len(linea.strip().split(" ")[0].split(".")) > 2 else "subtitulo"
                    area_teoria.insert(tk.END, f"{linea}\n", tag)
                else:
                    area_teoria.insert(tk.END, f"{linea}\n", "cuerpo")

        elif num_unidad in TEORIA_DETALLADA:
            for sub_titulo, sub_contenido in TEORIA_DETALLADA[num_unidad]:
                tag = "subsubtitulo" if len(sub_titulo.split(" ")[0].split(".")) > 2 else "subtitulo"
                area_teoria.insert(tk.END, f"{sub_titulo}\n", tag)
                area_teoria.insert(tk.END, f"{sub_contenido}\n\n", "cuerpo")
        else:
            area_teoria.insert(tk.END, "Contenido teórico en elaboración. El administrador aún no ha subido información para esta unidad.\n", "cuerpo")

        area_teoria.configure(state="disabled")

        # 2. Cargar Cuestionario
        for w in scrollable_quiz_inner.winfo_children():
            w.destroy()

        preguntas_actuales.clear()
        preguntas_actuales.extend(obtener_preguntas_unidad(t[0]))
        respuestas_usuario.clear()

        if not preguntas_actuales:
            ctk.CTkLabel(scrollable_quiz_inner, text="No hay preguntas registradas para este tema.",
                         font=ctk.CTkFont("Segoe UI", 13, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=30)
        else:
            for p_idx, p in enumerate(preguntas_actuales):
                p_id, preg, op_a, op_b, op_c, op_d, resp_correcta = p

                f_preg = ctk.CTkFrame(scrollable_quiz_inner, fg_color=COLOR_CARD, corner_radius=10)
                f_preg.pack(fill="x", expand=True, pady=10, anchor="w")

                ctk.CTkLabel(f_preg, text=f"{p_idx + 1}. {preg}", font=ctk.CTkFont("Segoe UI", 13, "bold"),
                             text_color=COLOR_TEXT_LIGHT, wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(10, 5))

                var_resp = tk.StringVar(value="")
                respuestas_usuario[p_id] = var_resp

                opciones = [("A) " + op_a, "A"), ("B) " + op_b, "B"), ("C) " + op_c, "C"), ("D) " + op_d, "D")]
                for txt_o, val_o in opciones:
                    ctk.CTkRadioButton(f_preg, text=txt_o, value=val_o, variable=var_resp, font=ctk.CTkFont("Segoe UI", 12),
                                       fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_MUTED).pack(
                        anchor="w", padx=30, pady=5)

            def evaluar():
                sin_responder = sum(1 for p in preguntas_actuales if not respuestas_usuario[p[0]].get())
                if sin_responder > 0:
                    if not messagebox.askyesno("Preguntas pendientes", f"Tienes {sin_responder} pregunta(s) sin responder. ¿Deseas enviar el cuestionario de todos modos?"):
                        return

                correctas = sum(1 for p in preguntas_actuales if respuestas_usuario[p[0]].get() == p[6])
                total = len(preguntas_actuales)
                if total == 0:
                    return
                puntaje = int((correctas / total) * 100)
                guardar_calificacion(usuario, tema_activo["id"], puntaje)
                messagebox.showinfo("Evaluación Finalizada", f"Tema: Unidad {tema_activo['unidad']}\nAciertos: {correctas}/{total}\nCalificación: {puntaje}/100")
                actualizar_tabla_historial()

            btn_enviar = ctk.CTkButton(scrollable_quiz_inner, text="ENVIAR RESPUESTAS DEL TEMA", command=evaluar,
                                       font=ctk.CTkFont("Segoe UI", 13, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, cursor="hand2")
            btn_enviar.pack(pady=20)

        # --- ENRUTAMIENTO DINÁMICO DE LAS 16 PRÁCTICAS ---
        for w in menu_practicas.winfo_children(): w.destroy()
        for w in container_practica.winfo_children(): w.destroy()

        def cargar_practica_generica(parent, titulo, descripcion):
            for w in parent.winfo_children(): w.destroy()
            ctk.CTkLabel(parent, text=titulo, font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 10))
            ctk.CTkLabel(parent, text=descripcion, font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT).pack(pady=5)
            ctk.CTkLabel(parent, text="[Módulo de práctica en desarrollo]", font=ctk.CTkFont("Consolas", 12, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=30)

        RUTAS_PRACTICAS = {
            1: [
                ("1. Trivia", cargar_practica_u1_p1 if cargar_practica_u1_p1 else lambda p: cargar_practica_generica(p, "Práctica 1.1 Trivia", "Archivo no encontrado.")),
                ("2. Normativa ISO", cargar_practica_u1_p2 if cargar_practica_u1_p2 else lambda p: cargar_practica_generica(p, "Práctica 1.2 ISO", "Archivo no encontrado.")),
                ("3. Conceptos", cargar_practica_u1_p3 if cargar_practica_u1_p3 else lambda p: cargar_practica_generica(p, "Práctica 1.3 Conceptos", "Archivo no encontrado.")),
                ("4. Caso Real", cargar_practica_u1_p4 if cargar_practica_u1_p4 else lambda p: cargar_practica_generica(p, "Práctica 1.4 Caso", "Archivo no encontrado."))
            ],
            2: [
                ("1. Identificación", cargar_practica_u2_p1),
                ("2. Hashes", cargar_practica_hashes),
                ("3. Cadena Custodia", cargar_practica_u2_p3),
                ("4. Informes", cargar_practica_u2_p4)
            ],
            3: [
                ("1. ExifTool", cargar_practica_exif),
                ("2. Wireshark", cargar_practica_u3_p2),
                ("3. File Carving", cargar_practica_u3_p3),
                ("4. SQLite DB", cargar_practica_u3_p4)
            ],
            4: [
                ("1. Triage", cargar_practica_u4_p1),
                ("2. Windows Logs", cargar_practica_windows_logs),
                ("3. Timeline", cargar_practica_u4_p3),
                ("4. Indicadores (IoC)", cargar_practica_u4_p4)
            ]
        }
        
        practicas_unidad = RUTAS_PRACTICAS.get(t[1], [])
        
        if practicas_unidad:
            for titulo, func in practicas_unidad:
                btn = ctk.CTkButton(menu_practicas, text=titulo, font=ctk.CTkFont("Segoe UI", 12, "bold"), fg_color=COLOR_BORDER, hover_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, cursor="hand2", command=lambda f=func: f(container_practica))
                btn.pack(side="left", padx=5)
            practicas_unidad[0][1](container_practica) # Carga la primera por defecto
        else:
            ctk.CTkLabel(container_practica, text=f"Prácticas no definidas para la Unidad {t[1]}.", font=ctk.CTkFont("Segoe UI", 13, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=50)

        # Seleccionar por defecto la primera pestaña (Explicación)
        sub_pestanas.set(tab_teoria_name)

    listbox_temas.bind("<<ListboxSelect>>", cargar_detalle_tema)

    # Seleccionar primer tema por defecto si existe
    if temas:
        listbox_temas.selection_set(0)
        listbox_temas.event_generate("<<ListboxSelect>>")

    ventana.bind("<Escape>", lambda e: ventana.quit())

def abrir_practica(self, id_practica, titulo):
    if id_practica == 6: 
        from tools.hash_simulator import HashSimulatorApp
        ventana = ctk.CTkToplevel(self.root)
        HashSimulatorApp(ventana)
    elif id_practica == 14: 
        from tools.windows_logs_simulator import WindowsLogsSimulatorApp
        ventana = ctk.CTkToplevel(self.root)
        WindowsLogsSimulatorApp(ventana)
    else:
        messagebox.showinfo("En desarrollo", f"La práctica '{titulo}' está en proceso de integración.")