import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#64748B"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BORDER = "#1E293B"
COLOR_DANGER = "#E63946"


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

    # Obtener alumnos del grupo
    cursor.execute("SELECT id, nombre_usuario FROM usuarios WHERE grupo_id = ? AND rol = 'alumno'", (grupo_id,))
    alumnos = cursor.fetchall()

    # Obtener todas las calificaciones asociadas
    cursor.execute("""
                   SELECT c.alumno_id, c.tema_id, MAX(c.puntaje)
                   FROM calificaciones c
                   GROUP BY c.alumno_id, c.tema_id
                   """)
    califs = cursor.fetchall()
    conexion.close()

    # Mapear calificaciones por (alumno_id, tema_id)
    mapa_calif = {(c[0], c[1]): c[2] for c in califs}

    return alumnos, mapa_calif


def abrir_panel_docente(usuario):
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel de Docente ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg=COLOR_BG_DARK)

    # Header
    header = tk.Frame(ventana, bg=COLOR_CARD, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    tk.Label(header, text=f"👨‍🏫 PORTAL DOCENTE - {usuario.upper()}", font=("Segoe UI", 14, "bold"), bg=COLOR_CARD,
             fg=COLOR_ACCENT).pack(side="left", padx=20)

    btn_cerrar = tk.Button(header, text="CERRAR SESIÓN", command=ventana.destroy, font=("Segoe UI", 9, "bold"),
                           bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2")
    btn_cerrar.pack(side="right", padx=20, ipadx=10, ipady=5)

    container = tk.Frame(ventana, bg=COLOR_BG_DARK)
    container.pack(fill="both", expand=True, padx=25, pady=20)

    # Barra superior de selección de grupo
    f_select = tk.Frame(container, bg=COLOR_CARD)
    f_select.pack(fill="x", pady=(0, 15), ipady=10)

    tk.Label(f_select, text="SELECCIONAR GRUPO ASIGNADO:", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD,
             fg=COLOR_TEXT_LIGHT).pack(side="left", padx=20)

    combo_grupos = ttk.Combobox(f_select, state="readonly", font=("Segoe UI", 10), width=25)
    combo_grupos.pack(side="left", padx=10)

    grupos = obtener_grupos_de_docente(usuario)
    dict_grupos = {g[1]: g[0] for g in grupos}
    combo_grupos["values"] = list(dict_grupos.keys())

    # Contenedor para la tabla dinámica
    frame_tabla = tk.Frame(container, bg=COLOR_CARD)
    frame_tabla.pack(fill="both", expand=True)

    def cargar_reporte_grupo(event=None):
        g_nom = combo_grupos.get()
        if not g_nom:
            return

        for w in frame_tabla.winfo_children():
            w.destroy()

        g_id = dict_grupos[g_nom]
        temas = obtener_temas()
        alumnos, mapa_calif = obtener_calificaciones_grupo(g_id)

        # Definir columnas dinámicas del Treeview (Alumno, U1, U2, ..., Promedio)
        cols = ["alumno"] + [f"u_{t[0]}" for t in temas] + ["promedio"]

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT,
                        fieldbackground=COLOR_ENTRY_BG, rowheight=30)
        style.configure("Treeview.Heading", background=COLOR_BORDER, foreground=COLOR_ACCENT,
                        font=("Segoe UI", 9, "bold"))

        tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")

        tabla.heading("alumno", text="Alumno / Estudiante")
        tabla.column("alumno", width=250)

        for t in temas:
            tabla.heading(f"u_{t[0]}", text=f"Unidad {t[1]}")
            tabla.column(f"u_{t[0]}", width=100, anchor="center")

        tabla.heading("promedio", text="PROMEDIO")
        tabla.column("promedio", width=120, anchor="center")

        tabla.pack(fill="both", expand=True, padx=15, pady=15)

        # Insertar datos de alumnos
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

    combo_grupos.bind("<<ComboboxSelected>>", cargar_reporte_grupo)

    if grupos:
        combo_grupos.set(grupos[0][1])
        cargar_reporte_grupo()
    else:
        tk.Label(frame_tabla, text="No tienes grupos asignados actualmente.", font=("Segoe UI", 12, "italic"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=50)

    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.mainloop()