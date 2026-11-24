import os
import sys
import sqlite3
import tkinter as tk
import re
from tkinter import ttk
import customtkinter as ctk

# Asegurar que la ruta raíz esté en el path para importar la carpeta tools y views sin problemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from views.tutorial_view import open_tutorial
except ImportError:
    def open_tutorial(*args, **kwargs):
        return None

# Importar los módulos de prácticas desde la carpeta tools
try:
    from tools import practicas_u1, practicas_u2, practicas_u3, practicas_u4
except ImportError as e:
    print(f"Advertencia: No se pudo importar algún módulo de prácticas desde tools: {e}")

# Intentar importar la ruta de DB centralizada o calcularla en su defecto
try:
    from database.db_manager import DB_PATH as RUTA_DB
except ImportError:
    DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

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
COLOR_SUCCESS = "#2EC4B6"
COLOR_DANGER = "#E63946"
COLOR_DANGER_HOVER = "#D62828"


def _cancelar_after(widget, after_id):
    if widget is not None and after_id is not None:
        try:
            if widget.winfo_exists():
                widget.after_cancel(after_id)
        except Exception:
            pass


def _cerrar_ventana_seguro(ventana, after_ids=None):
    if after_ids:
        for aid in after_ids:
            _cancelar_after(ventana, aid)
    try:
        if ventana.winfo_exists():
            ventana.quit()
    except Exception:
        pass
    try:
        if ventana.winfo_exists():
            ventana.destroy()
    except Exception:
        pass


# ==========================================
# MODAL HUD REUTILIZABLE (ESTILO DE LA APP)
# ==========================================
def mostrar_modal_hud(parent, titulo, mensaje, tipo="info", confirmar=False):
    resultado = {"valor": False if confirmar else True}

    if parent is None:
        return resultado["valor"]
    try:
        if not parent.winfo_exists():
            return resultado["valor"]
    except Exception:
        return resultado["valor"]

    try:
        modal = ctk.CTkToplevel(parent)
    except Exception:
        return resultado["valor"]

    modal.title("")
    modal.geometry("460x235")
    modal.configure(fg_color=COLOR_BG_DARK)
    modal.overrideredirect(True)

    try:
        modal.attributes("-alpha", 0.0)
    except Exception:
        pass

    try:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 230
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 117
        modal.geometry(f"+{x}+{y}")
    except Exception:
        pass

    borde = COLOR_DANGER if tipo == "error" else (COLOR_SUCCESS if tipo == "success" else COLOR_ACCENT)
    color_tit = COLOR_DANGER if tipo == "error" else (COLOR_SUCCESS if tipo == "success" else COLOR_ACCENT)

    card_m = ctk.CTkFrame(
        modal, fg_color=COLOR_CARD, border_color=borde, border_width=1, corner_radius=12
    )
    card_m.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(
        card_m, text=titulo, font=("Segoe UI", 15, "bold"), text_color=color_tit
    ).pack(pady=(20, 8))

    ctk.CTkLabel(
        card_m, text=mensaje, font=("Segoe UI", 12),
        text_color=COLOR_TEXT_LIGHT, justify="center", wraplength=400
    ).pack(pady=(0, 18), padx=16)

    anim_id = None
    cerrado = {"hecho": False}

    def fade_in(a=0.0):
        nonlocal anim_id
        if cerrado["hecho"]:
            return
        try:
            if a < 1.0 and modal.winfo_exists():
                a = min(1.0, a + 0.12)
                modal.attributes("-alpha", a)
                anim_id = modal.after(15, lambda: fade_in(a))
        except Exception:
            pass

    def cerrar(val):
        nonlocal anim_id
        if cerrado["hecho"]:
            return
        cerrado["hecho"] = True
        _cancelar_after(modal, anim_id)
        anim_id = None
        resultado["valor"] = val
        try:
            if modal.winfo_exists():
                try:
                    modal.grab_release()
                except Exception:
                    pass
                modal.destroy()
        except Exception:
            pass

    f_btns = ctk.CTkFrame(card_m, fg_color="transparent")
    f_btns.pack(pady=(0, 14))

    if confirmar:
        ctk.CTkButton(
            f_btns, text="CANCELAR", command=lambda: cerrar(False), width=130, height=36,
            fg_color=COLOR_ENTRY_BG, hover_color=COLOR_BORDER, text_color=COLOR_TEXT_LIGHT,
            font=("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2"
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            f_btns, text="CONFIRMAR", command=lambda: cerrar(True), width=140, height=36,
            fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT,
            font=("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2"
        ).pack(side="left", padx=8)
    else:
        ctk.CTkButton(
            f_btns, text="ACEPTAR", command=lambda: cerrar(True), width=140, height=36,
            fg_color=borde, hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT_LIGHT if tipo == "error" else COLOR_BG_DARK,
            font=("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2"
        ).pack()

    modal.protocol("WM_DELETE_WINDOW", lambda: cerrar(False if confirmar else True))
    modal.bind("<Return>", lambda e: cerrar(True))
    modal.bind("<Escape>", lambda e: cerrar(False if confirmar else True))

    try:
        modal.grab_set()
    except Exception:
        pass

    fade_in()

    try:
        if parent.winfo_exists() and modal.winfo_exists():
            parent.wait_window(modal)
    except Exception:
        pass

    return resultado["valor"]


# ==========================================
# BARRA DE TÍTULO PERSONALIZADA
# ==========================================
def crear_barra_titulo(ventana, bg_color, on_salir=None):
    barra_titulo = ctk.CTkFrame(ventana, height=35, fg_color=bg_color, corner_radius=0)
    barra_titulo.pack(side="top", fill="x")
    barra_titulo.pack_propagate(False)

    comando_cerrar = on_salir if on_salir else lambda: _cerrar_ventana_seguro(ventana)

    btn_cerrar = ctk.CTkButton(
        barra_titulo, text="✕", font=("Segoe UI", 14), width=45, height=35,
        fg_color="transparent", hover_color="#E81123", text_color="white",
        corner_radius=0, command=comando_cerrar
    )
    btn_cerrar.pack(side="right")

    def toggle_maximizar():
        try:
            if ventana.winfo_exists():
                es_fullscreen = ventana.attributes('-fullscreen')
                ventana.attributes('-fullscreen', not es_fullscreen)
        except Exception:
            pass

    btn_max = ctk.CTkButton(
        barra_titulo, text="🗗", font=("Segoe UI", 15), width=45, height=35,
        fg_color="transparent", hover_color=COLOR_BORDER, text_color="white",
        corner_radius=0, command=toggle_maximizar
    )
    btn_max.pack(side="right")

    btn_min = ctk.CTkButton(
        barra_titulo, text="—", font=("Segoe UI", 15, "bold"), width=45, height=35,
        fg_color="transparent", hover_color=COLOR_BORDER, text_color="white",
        corner_radius=0, command=ventana.iconify
    )
    btn_min.pack(side="right")


# ==========================================
# CONTENIDO TEÓRICO COMPLETO DETALLADO POR UNIDADES
# ==========================================
TEORIA_DETALLADA = {
    1: [
        ("1.1 Conceptos generales",
         "La informática forense es la disciplina científica y pericial dedicada a la identificación, preservación, extracción, análisis y presentación de evidencias digitales almacenadas en dispositivos electrónicos.\n\n"
         "• Evidencia Digital: Cualquier información en formato binario que pueda ser utilizada para probar un hecho en un proceso judicial o administrativo.\n"
         "• Cadena de Custodia: Proceso riguroso que documenta cronológicamente la extracción, custodia, control, transferencia, análisis y disposición de la evidencia física o digital.\n"
         "• Hash de Integridad: Firma matemática unívoca (MD5, SHA-256) que garantiza que un archivo no ha sufrido modificaciones desde su extracción."),
        ("1.2 Importancia",
         "En el contexto actual de digitalización masiva y cibercrimen, la informática forense cumple un papel determinante para garantizar la admisibilidad de pruebas y la respuesta efectiva a incidentes."),
        ("1.3 Situación actual",
         "El panorama contemporáneo enfrenta retos como entornos en la nube, cifrado de disco completo y proliferación de dispositivos IoT."),
        ("1.4 Principios",
         "Los pilares éticos y procesales son el Principio de Mínima Intervención, el Principio de Locard digital y la auditabilidad/repetibilidad."),
        ("1.5 Estándares y Normativas",
         "Cumplimiento de normativas internacionales como ISO/IEC 27037 y RFC 3227.")
    ],
    2: [
        ("2 Metodología del Análisis Forense Informático",
         "La metodología forense estandarizada asegura que el manejo de la evidencia digital no comprometa su integridad ni su valor probatorio ante un juez."),
        ("2.1 Identificación de la evidencia",
         "Consiste en reconocer, localizar y documentar todas las posibles fuentes de información digital dentro de la escena."),
        ("2.2 Adquisición de la evidencia",
         "Proceso de obtención de una copia bit a bit exacta del medio original (imagen forense) empleando herramientas de bloqueo de escritura."),
        ("2.3 Preservación de la evidencia",
         "Aseguramiento físico y lógico de los indicios recolectados calculando hashes criptográficos inmediatos."),
        ("2.4 Análisis de la evidencia",
         "Examen técnico profundo de los datos adquiridos, recuperación de archivos y revisión de artefactos.")
    ],
    3: [
        ("3 Herramientas de Análisis Forense",
         "El uso de software especializado es clave para automatizar la extracción y examen forense sin alterar la integridad de los datos."),
        ("3.1 Software Libre",
         "• Autopsy: Suite forense digital de código abierto.\n• Wireshark: Analizador de protocolos de red.\n• ExifTool: Utilidad para metadatos."),
        ("3.2 Recuperación de datos",
         "Técnicas de file carving y recuperación de bases de datos SQLite.")
    ],
    4: [
        ("4 Evidencia y Atribución del ataque Digital",
         "La fase terminal de una investigación se centra en correlacionar los hallazgos técnicos para explicar cómo ocurrió el ataque."),
        ("4.1 Respuesta a incidentes", "Contención, mitigación y análisis retrospectivo de brechas."),
        ("4.2 Hallazgos y atribución", "Generación de Indicadores de Compromiso (IoCs) y líneas de tiempo.")
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
# MODAL PERSONALIZADO DE CIERRE DE SESIÓN
# ==========================================
def confirmar_cierre_sesion_hud(parent):
    return mostrar_modal_hud(
        parent,
        "⚠️ CONFIRMAR CIERRE DE SESIÓN",
        "¿Estás seguro de que deseas cerrar sesión\ny regresar al panel principal de acceso?",
        tipo="info",
        confirmar=True
    )


# ==========================================
# INTERFAZ GRÁFICA DEL ESTUDIANTE
# ==========================================
def abrir_panel_alumno(usuario):
    ventana = ctk.CTk()
    ventana.title(f"LAB VISUAL FORENSE - Módulo Guiado ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(fg_color=COLOR_BG_DARK)
    ventana.attributes("-alpha", 0.0)

    sesion_cerrada = {"estado": False}
    cerrando = {"activo": False}
    id_animacion = None
    id_tutorial = None

    def animar_entrada(alpha=0.0):
        nonlocal id_animacion
        if cerrando["activo"]:
            return
        try:
            if alpha < 1.0 and ventana.winfo_exists():
                alpha = min(1.0, alpha + 0.05)
                ventana.attributes("-alpha", alpha)
                id_animacion = ventana.after(20, lambda: animar_entrada(alpha))
        except Exception:
            pass

    def disparar_tutorial_auto():
        nonlocal id_tutorial
        id_tutorial = None
        if cerrando["activo"]:
            return
        try:
            if ventana.winfo_exists():
                open_tutorial(ventana, role="alumno", auto=True)
        except Exception:
            pass

    def salir_directo():
        if cerrando["activo"]:
            return
        cerrando["activo"] = True
        _cerrar_ventana_seguro(ventana, [id_animacion, id_tutorial])

    def cerrar_sesion():
        if cerrando["activo"]:
            return
        try:
            if not ventana.winfo_exists():
                return
        except Exception:
            return

        if confirmar_cierre_sesion_hud(ventana):
            cerrando["activo"] = True
            sesion_cerrada["estado"] = True
            _cerrar_ventana_seguro(ventana, [id_animacion, id_tutorial])

    ventana.protocol("WM_DELETE_WINDOW", cerrar_sesion)
    crear_barra_titulo(ventana, COLOR_BG_DARK, on_salir=cerrar_sesion)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=30)
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("Treeview.Heading", background=COLOR_CARD, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 10, "bold"), borderwidth=0)

    container_main = ctk.CTkFrame(ventana, fg_color=COLOR_BG_DARK)
    container_main.pack(fill="both", expand=True, padx=20, pady=20)

    # SIDEBAR
    sidebar = ctk.CTkFrame(container_main, fg_color=COLOR_CARD, border_color=COLOR_BORDER, border_width=1, width=320, corner_radius=12)
    sidebar.pack(side="left", fill="y", padx=(0, 15))
    sidebar.pack_propagate(False)

    ctk.CTkLabel(sidebar, text="UNIDADES DEL CURSO", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_MUTED).pack(
        pady=(22, 10), padx=18, anchor="w")

    temas = obtener_temas_bd()
    temas_por_unidad = {}
    for t in temas:
        match_u = re.search(r'\d+', str(t[1]))
        num_u = int(match_u.group()) if match_u else 1
        if num_u not in temas_por_unidad:
            temas_por_unidad[num_u] = t

    f_unidades = ctk.CTkFrame(sidebar, fg_color="transparent")
    f_unidades.pack(fill="x", padx=14, pady=(0, 14))

    espacio_sidebar = ctk.CTkFrame(sidebar, fg_color="transparent")
    espacio_sidebar.pack(fill="both", expand=True)

    # PANEL DERECHO
    panel_derecho = ctk.CTkFrame(container_main, fg_color=COLOR_CARD, border_color=COLOR_BORDER, border_width=1, corner_radius=12)
    panel_derecho.pack(side="right", fill="both", expand=True)

    lbl_titulo_tema = ctk.CTkLabel(panel_derecho, text="Selecciona un tema del temario para comenzar",
                                   font=("Segoe UI", 18, "bold"), text_color=COLOR_TEXT_LIGHT)
    lbl_titulo_tema.pack(pady=(20, 10), padx=25, anchor="w")

    sub_pestanas = ctk.CTkTabview(panel_derecho, fg_color=COLOR_ENTRY_BG, segmented_button_selected_color=COLOR_BORDER,
                                  segmented_button_selected_hover_color=COLOR_CARD, segmented_button_unselected_color=COLOR_CARD,
                                  text_color=COLOR_TEXT_MUTED, corner_radius=12)
    sub_pestanas.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    tab_teoria_name = "📖 1. Explicación"
    tab_quiz_name = "📝 2. Cuestionario"
    tab_practica_name = "🛠️ 3. Práctica Aplicada"
    tab_historial_name = "📊 4. Mis Calificaciones"

    sub_pestanas.add(tab_teoria_name)
    sub_pestanas.add(tab_quiz_name)
    sub_pestanas.add(tab_practica_name)
    sub_pestanas.add(tab_historial_name)

    # TABS SETUP
    tab_teoria = sub_pestanas.tab(tab_teoria_name)
    area_teoria = ctk.CTkTextbox(tab_teoria, wrap="word", font=("Segoe UI", 14), fg_color=COLOR_CARD,
                                 text_color=COLOR_TEXT_LIGHT, border_width=0, corner_radius=10)
    area_teoria.pack(fill="both", expand=True, padx=15, pady=15)
    area_teoria.tag_config("subtitulo", foreground=COLOR_ACCENT)
    area_teoria.tag_config("subsubtitulo", foreground="#00C4D4")
    area_teoria.tag_config("cuerpo", foreground=COLOR_TEXT_LIGHT)

    tab_quiz = sub_pestanas.tab(tab_quiz_name)
    scrollable_quiz_inner = ctk.CTkScrollableFrame(tab_quiz, fg_color="transparent")
    scrollable_quiz_inner.pack(fill="both", expand=True, padx=15, pady=15)

    tab_practica = sub_pestanas.tab(tab_practica_name)

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

    tema_activo = {"id": None, "unidad": None, "titulo": ""}
    respuestas_usuario = {}
    preguntas_actuales = []
    botones_unidad = {}

    # =============================================================
    # EVENTO AL SELECCIONAR UNA UNIDAD (U1 - U4)
    # =============================================================
    def cargar_detalle_tema(num_unidad):
        for u_key, btn_u in botones_unidad.items():
            if u_key == num_unidad:
                btn_u.configure(fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK)
            else:
                btn_u.configure(fg_color=COLOR_ENTRY_BG, text_color=COLOR_ACCENT)

        t = temas_por_unidad.get(num_unidad)
        if t:
            tema_id = t[0]
            titulo_tema = t[2]
        else:
            tema_id = num_unidad
            titulo_tema = f"Unidad {num_unidad}"

        tema_activo["id"] = tema_id
        tema_activo["unidad"] = num_unidad
        tema_activo["titulo"] = titulo_tema

        lbl_titulo_tema.configure(text=f"UNIDAD {num_unidad}: {titulo_tema}")

        # 1. Cargar Teoría Formateada con Subtemas
        area_teoria.configure(state="normal")
        area_teoria.delete("1.0", tk.END)
        if num_unidad in TEORIA_DETALLADA:
            for sub_titulo, sub_contenido in TEORIA_DETALLADA[num_unidad]:
                tag = "subsubtitulo" if len(sub_titulo.split(" ")[0].split(".")) > 2 else "subtitulo"
                area_teoria.insert(tk.END, f"{sub_titulo}\n", tag)
                area_teoria.insert(tk.END, f"{sub_contenido}\n\n", "cuerpo")
        else:
            area_teoria.insert(tk.END, "Contenido teórico en elaboración.\n", "cuerpo")
        area_teoria.configure(state="disabled")

        # 2. Cargar Cuestionario
        for w in scrollable_quiz_inner.winfo_children():
            w.destroy()
        preguntas_actuales.clear()
        preguntas_actuales.extend(obtener_preguntas_unidad(tema_id))
        respuestas_usuario.clear()

        if not preguntas_actuales:
            ctk.CTkLabel(scrollable_quiz_inner, text="No hay preguntas registradas para este tema.",
                         font=("Segoe UI", 13, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=30)
        else:
            for p_idx, p in enumerate(preguntas_actuales):
                p_id, preg, op_a, op_b, op_c, op_d, resp_correcta = p

                f_preg = ctk.CTkFrame(scrollable_quiz_inner, fg_color=COLOR_CARD, border_color=COLOR_BORDER, border_width=1, corner_radius=10)
                f_preg.pack(fill="x", expand=True, pady=10, anchor="w")

                ctk.CTkLabel(f_preg, text=f"{p_idx + 1}. {preg}", font=("Segoe UI", 13, "bold"),
                             text_color=COLOR_TEXT_LIGHT, wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(10, 5))

                var_resp = tk.StringVar(value="")
                respuestas_usuario[p_id] = var_resp

                opciones = [("A) " + op_a, "A"), ("B) " + op_b, "B"), ("C) " + str(op_c), "C"), ("D) " + str(op_d), "D")]
                for txt_o, val_o in opciones:
                    if val_o == "C" and not op_c:
                        continue
                    if val_o == "D" and not op_d:
                        continue
                    ctk.CTkRadioButton(f_preg, text=txt_o, value=val_o, variable=var_resp, font=("Segoe UI", 12),
                                       fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_TEXT_MUTED).pack(
                                   anchor="w", padx=30, pady=5)

            def evaluar():
                correctas = sum(1 for p in preguntas_actuales if respuestas_usuario[p[0]].get() == p[6])
                total = len(preguntas_actuales)
                if total == 0:
                    return
                puntaje = int((correctas / total) * 100)
                guardar_calificacion(usuario, tema_activo["id"], puntaje)
                mostrar_modal_hud(
                    ventana,
                    "✅ EVALUACIÓN FINALIZADA",
                    f"Tema: Unidad {tema_activo['unidad']}\nAciertos: {correctas}/{total}\nCalificación: {puntaje}/100",
                    tipo="success",
                    confirmar=False
                )
                actualizar_tabla_historial()

            ctk.CTkButton(scrollable_quiz_inner, text="ENVIAR RESPUESTAS DEL TEMA", command=evaluar,
                          font=("Segoe UI", 13, "bold"), fg_color=COLOR_SUCCESS, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, corner_radius=8, cursor="hand2").pack(pady=20)

        # 3. EXTRACCIÓN DINÁMICA DE PRÁCTICAS DESDE LA CARPETA TOOLS
        for w in tab_practica.winfo_children():
            w.destroy()

        menu_p = ctk.CTkFrame(tab_practica, fg_color="transparent")
        menu_p.pack(fill="x", padx=10, pady=(10, 5))

        cont_p = ctk.CTkFrame(tab_practica, fg_color="transparent")
        cont_p.pack(fill="both", expand=True, padx=10, pady=5)

        RUTAS_PRACTICAS_TOOLS = {
            1: [
                ("Práctica 1", lambda p: practicas_u1.cargar_practica_u1_p1(p)),
                ("Práctica 2", lambda p: practicas_u1.cargar_practica_u1_p2(p)),
                ("Práctica 3", lambda p: practicas_u1.cargar_practica_u1_p3(p)),
                ("Práctica 4", lambda p: practicas_u1.cargar_practica_u1_p4(p))
            ],
            2: [
                ("Práctica 1", lambda p: practicas_u2.cargar_practica_u2_p1(p)),
                ("Práctica 2", lambda p: practicas_u2.cargar_practica_u2_p2(p)),
                ("Práctica 3", lambda p: practicas_u2.cargar_practica_u2_p3(p)),
                ("Práctica 4", lambda p: practicas_u2.cargar_practica_u2_p4(p))
            ],
            3: [
                ("Práctica 1", lambda p: practicas_u3.cargar_practica_u3_p1(p)),
                ("Práctica 2", lambda p: practicas_u3.cargar_practica_u3_p2(p)),
                ("Práctica 3", lambda p: practicas_u3.cargar_practica_u3_p3(p)),
                ("Práctica 4", lambda p: practicas_u3.cargar_practica_u3_p4(p))
            ],
            4: [
                ("Práctica 1", lambda p: practicas_u4.cargar_practica_u4_p1(p)),
                ("Práctica 2", lambda p: practicas_u4.cargar_practica_u4_p2(p)),
                ("Práctica 3", lambda p: practicas_u4.cargar_practica_u4_p3(p)),
                ("Práctica 4", lambda p: practicas_u4.cargar_practica_u4_p4(p))
            ]
        }

        practicas_unidad = RUTAS_PRACTICAS_TOOLS.get(num_unidad, [])
        if practicas_unidad:
            for titulo, func in practicas_unidad:
                ctk.CTkButton(
                    menu_p,
                    text=titulo,
                    font=("Segoe UI", 11, "bold"),
                    fg_color=COLOR_CARD,
                    hover_color=COLOR_BORDER,
                    text_color=COLOR_ACCENT,
                    corner_radius=8,
                    cursor="hand2",
                    command=lambda f=func: f(cont_p)
                ).pack(side="left", padx=5, expand=True, fill="x")

            practicas_unidad[0][1](cont_p)

        sub_pestanas.set(tab_teoria_name)

    for u in [1, 2, 3, 4]:
        btn_u = ctk.CTkButton(
            f_unidades,
            text=f"U{u}",
            width=56,
            height=38,
            command=lambda num=u: cargar_detalle_tema(num),
            fg_color=COLOR_ENTRY_BG,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_ACCENT,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8,
            cursor="hand2"
        )
        btn_u.pack(side="left", padx=3, expand=True)
        botones_unidad[u] = btn_u

    btn_ayuda = ctk.CTkButton(
        sidebar, text="❓ AYUDA / TUTORIAL",
        command=lambda: open_tutorial(ventana, role="alumno", auto=False),
        font=("Segoe UI", 12, "bold"),
        fg_color=COLOR_ENTRY_BG, hover_color=COLOR_BORDER,
        text_color=COLOR_ACCENT, corner_radius=8, cursor="hand2"
    )
    btn_ayuda.pack(fill="x", padx=15, pady=(0, 8), ipady=5)

    btn_cerrar = ctk.CTkButton(
        sidebar, text="CERRAR SESIÓN", command=cerrar_sesion,
        font=("Segoe UI", 12, "bold"), fg_color=COLOR_DANGER,
        hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT,
        corner_radius=8, cursor="hand2"
    )
    btn_cerrar.pack(fill="x", padx=15, pady=(0, 15), ipady=5)

    cargar_detalle_tema(1)

    ventana.bind("<Escape>", lambda e: salir_directo())
    id_animacion = ventana.after(100, animar_entrada)
    id_tutorial = ventana.after(350, disparar_tutorial_auto)

    try:
        ventana.mainloop()
    finally:
        cerrando["activo"] = True
        _cancelar_after(ventana, id_animacion)
        _cancelar_after(ventana, id_tutorial)

    return sesion_cerrada["estado"]


if __name__ == "__main__":
    abrir_panel_alumno("AlumnoDemo")