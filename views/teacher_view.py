import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_ACCENT_HOVER = "#00C4D4"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#64748B"
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

def obtener_grupos_de_docente(nombre_docente):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("""
                   SELECT g.id, g.nombre_grupo
                   FROM grupos g
                            JOIN usuarios u ON g.docente_id = u.id
                   WHERE u.nombre_usuario = ?
                   """, (nombre_docente,))
    grupos = cursor.fetchall()
    conexion.close()
    return grupos

def obtener_temas():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, unidad, titulo FROM temas ORDER BY unidad ASC")
    temas = cursor.fetchall()
    conexion.close()
    return temas

def obtener_calificaciones_grupo(grupo_id):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_usuario FROM usuarios WHERE grupo_id = ? AND rol = 'alumno'", (grupo_id,))
    alumnos = cursor.fetchall()
    cursor.execute("""
                   SELECT c.alumno_id, c.tema_id, MAX(c.puntaje)
                   FROM calificaciones c
                   GROUP BY c.alumno_id, c.tema_id
                   """)
    califs = cursor.fetchall()
    conexion.close()
    mapa_calif = {(c[0], c[1]): c[2] for c in califs}
    return alumnos, mapa_calif

def abrir_panel_docente(usuario):
    ventana = ctk.CTkToplevel()
    ventana.title(f"LAB VISUAL FORENSE - Panel de Docente ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(fg_color=COLOR_BG_DARK)

    # --- INSTANCIAR LA BARRA DE TÍTULO ---
    crear_barra_titulo(ventana, COLOR_BG_DARK)

    header = ctk.CTkFrame(ventana, height=60, fg_color=COLOR_CARD, corner_radius=0)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    ctk.CTkLabel(header, text=f"👨‍🏫 PORTAL DOCENTE - {usuario.upper()}", font=ctk.CTkFont("Segoe UI", 16, "bold"), 
                 text_color=COLOR_ACCENT).pack(side="left", padx=20)

    btn_cerrar = ctk.CTkButton(header, text="CERRAR SESIÓN", command=ventana.quit, 
                               font=ctk.CTkFont("Segoe UI", 12, "bold"), fg_color=COLOR_DANGER, 
                               hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT, cursor="hand2")
    btn_cerrar.pack(side="right", padx=20)

    container = ctk.CTkFrame(ventana, fg_color=COLOR_BG_DARK)
    container.pack(fill="both", expand=True, padx=25, pady=20)

    f_select = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10)
    f_select.pack(fill="x", pady=(0, 15), ipady=10)

    ctk.CTkLabel(f_select, text="SELECCIONAR GRUPO ASIGNADO:", font=ctk.CTkFont("Segoe UI", 12, "bold"), 
                 text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=20, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, 
                    fieldbackground=COLOR_ENTRY_BG, borderwidth=0, rowheight=30)
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("Treeview.Heading", background=COLOR_BORDER, foreground=COLOR_TEXT_MUTED, 
                    font=("Segoe UI", 10, "bold"), borderwidth=0)

    frame_tabla = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10)
    frame_tabla.pack(fill="both", expand=True)

    def cargar_reporte_grupo(seleccion=None):
        g_nom = combo_grupos.get()
        if not g_nom or g_nom == "Sin grupos":
            return

        for w in frame_tabla.winfo_children():
            w.destroy()

        g_id = dict_grupos[g_nom]
        temas = obtener_temas()
        alumnos, mapa_calif = obtener_calificaciones_grupo(g_id)

        ctk.CTkLabel(frame_tabla, text=f"📊 Reporte de Calificaciones - Grupo: {g_nom}", 
                     font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=(15, 5), anchor="w", padx=20)

        cols = ["alumno"] + [f"u_{t[0]}" for t in temas] + ["promedio"]

        inner_table_frame = ctk.CTkFrame(frame_tabla, fg_color="transparent")
        inner_table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tabla = ttk.Treeview(inner_table_frame, columns=cols, show="headings")
        tabla.heading("alumno", text="Alumno / Estudiante")
        tabla.column("alumno", width=250)

        for t in temas:
            tabla.heading(f"u_{t[0]}", text=f"Unidad {t[1]}")
            tabla.column(f"u_{t[0]}", width=100, anchor="center")

        tabla.heading("promedio", text="PROMEDIO")
        tabla.column("promedio", width=120, anchor="center")
        tabla.pack(side="left", fill="both", expand=True)

        scroll_tbl = ctk.CTkScrollbar(inner_table_frame, orientation="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_tbl.set)
        scroll_tbl.pack(side="right", fill="y")

        if not alumnos:
            messagebox.showinfo("Información", f"El grupo {g_nom} aún no tiene alumnos asignados.")
            return

        for a_id, a_nom in alumnos:
            valores = [a_nom]
            suma = 0
            cont = 0
            for t in temas:
                calif = mapa_calif.get((a_id, t[0]), "N/A")
                valores.append(f"{calif}%" if isinstance(calif, int) else calif)
                if isinstance(calif, int):
                    suma += calif
                    cont += 1
            prom = f"{round(suma / cont, 1)}%" if cont > 0 else "N/A"
            valores.append(prom)
            tabla.insert("", "end", values=valores)

    combo_grupos = ctk.CTkOptionMenu(f_select, font=ctk.CTkFont("Segoe UI", 12), width=250,
                                     fg_color=COLOR_ENTRY_BG, button_color=COLOR_ACCENT, 
                                     button_hover_color=COLOR_ACCENT_HOVER, dropdown_fg_color=COLOR_CARD, 
                                     dropdown_hover_color=COLOR_ENTRY_BG, dropdown_text_color=COLOR_TEXT_LIGHT,
                                     command=cargar_reporte_grupo)
    combo_grupos.pack(side="left", padx=10, pady=10)

    grupos = obtener_grupos_de_docente(usuario)
    dict_grupos = {g[1]: g[0] for g in grupos}
    
    if dict_grupos:
        combo_grupos.configure(values=list(dict_grupos.keys()))
        combo_grupos.set(list(dict_grupos.keys())[0])
        cargar_reporte_grupo()
    else:
        combo_grupos.configure(values=["Sin grupos"])
        combo_grupos.set("Sin grupos")
        ctk.CTkLabel(frame_tabla, text="No tienes grupos asignados actualmente.", 
                     font=ctk.CTkFont("Segoe UI", 14, "italic"), text_color=COLOR_TEXT_MUTED).pack(pady=50)

    ventana.bind("<Escape>", lambda e: ventana.quit())