import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

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


def aplicar_hover(boton, color_normal, color_hover):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))


# ==========================================
# FUNCIONES DE BASE DE DATOS
# ==========================================
def obtener_docentes():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_usuario FROM usuarios WHERE rol = 'docente'")
    res = cursor.fetchall()
    conexion.close()
    return res


def obtener_alumnos_sin_grupo():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_usuario FROM usuarios WHERE rol = 'alumno'")
    res = cursor.fetchall()
    conexion.close()
    return res


def obtener_grupos_con_docente():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("""
                   SELECT g.id, g.nombre_grupo, COALESCE(u.nombre_usuario, 'Sin Docente')
                   FROM grupos g
                            LEFT JOIN usuarios u ON g.docente_id = u.id
                   """)
    res = cursor.fetchall()
    conexion.close()
    return res


def crear_usuario_bd(usuario, clave, rol):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)", (usuario, clave, rol))
        conexion.commit()
        conexion.close()
        return True, "Usuario creado exitosamente."
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya existe."


def crear_grupo_bd(nombre_grupo, docente_id):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO grupos (nombre_grupo, docente_id) VALUES (?, ?)", (nombre_grupo, docente_id))
        conexion.commit()
        conexion.close()
        return True, "Grupo registrado correctamente."
    except sqlite3.IntegrityError:
        return False, "El grupo ya existe."


def asignar_alumno_a_grupo(alumno_id, grupo_id):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("UPDATE usuarios SET grupo_id = ? WHERE id = ?", (grupo_id, alumno_id))
    conexion.commit()
    conexion.close()


# ==========================================
# INTERFAZ ADMIN
# ==========================================
def abrir_panel_admin(usuario):
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel Administrador ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg=COLOR_BG_DARK)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=28)
    style.configure("Treeview.Heading", background=COLOR_BORDER, foreground=COLOR_ACCENT, font=("Segoe UI", 9, "bold"))
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("TNotebook", background=COLOR_BG_DARK, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_MUTED, padding=[20, 10],
                    font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", COLOR_CARD)], foreground=[("selected", COLOR_ACCENT)])

    # Header
    header = tk.Frame(ventana, bg=COLOR_CARD, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    tk.Label(header, text="⚙️ ADMINISTRACIÓN - USUARIOS Y GRUPOS", font=("Segoe UI", 14, "bold"), bg=COLOR_CARD,
             fg=COLOR_ACCENT).pack(side="left", padx=20)
    btn_cerrar = tk.Button(header, text="CERRAR SESIÓN", command=ventana.destroy, font=("Segoe UI", 9, "bold"),
                           bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2")
    btn_cerrar.pack(side="right", padx=20, ipadx=10, ipady=5)

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=20, pady=20)

    # -------------------------------------------------------------
    # PESTAÑA 1: GESTIÓN DE DOCENTES Y GRUPOS
    # -------------------------------------------------------------
    tab_grupos = ttk.Frame(notebook)
    notebook.add(tab_grupos, text="👥 Docentes y Grupos")

    f_left = tk.Frame(tab_grupos, bg=COLOR_CARD, width=420)
    f_left.pack(side="left", fill="both", padx=(0, 10), pady=10)

    f_right = tk.Frame(tab_grupos, bg=COLOR_CARD)
    f_right.pack(side="right", fill="both", expand=True, pady=10)

    # 1. Crear Usuario
    tk.Label(f_left, text="1. REGISTRAR USUARIO", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT).pack(
        pady=(15, 10), padx=15, anchor="w")

    entry_u_nom = tk.Entry(f_left, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_u_nom.pack(fill="x", padx=15, pady=4, ipady=4)
    entry_u_nom.insert(0, "Usuario")

    entry_u_pass = tk.Entry(f_left, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0, show="*")
    entry_u_pass.pack(fill="x", padx=15, pady=4, ipady=4)

    combo_rol = ttk.Combobox(f_left, values=["docente", "alumno"], state="readonly", font=("Segoe UI", 10))
    combo_rol.set("docente")
    combo_rol.pack(fill="x", padx=15, pady=4)

    def action_crear_u():
        u = entry_u_nom.get().strip()
        p = entry_u_pass.get().strip()
        r = combo_rol.get()
        if not u or not p:
            messagebox.showwarning("Atención", "Ingresa usuario y contraseña.")
            return
        ok, msg = crear_usuario_bd(u, p, r)
        messagebox.showinfo("Resultado", msg)
        if ok:
            actualizar_combos()

    tk.Button(f_left, text="CREAR USUARIO", command=action_crear_u, bg=COLOR_ACCENT, fg=COLOR_BG_DARK,
              font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(fill="x", padx=15, pady=10, ipady=5)

    tk.Frame(f_left, bg=COLOR_BORDER, height=1).pack(fill="x", padx=15, pady=10)

    # 2. Crear Grupo y Asignar Docente
    tk.Label(f_left, text="2. CREAR GRUPO Y ASIGNAR DOCENTE", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD,
             fg=COLOR_ACCENT).pack(pady=(5, 10), padx=15, anchor="w")

    entry_g_nom = tk.Entry(f_left, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_g_nom.pack(fill="x", padx=15, pady=4, ipady=4)
    entry_g_nom.insert(0, "Nombre Grupo (ej. 4IV1)")

    combo_docentes = ttk.Combobox(f_left, state="readonly", font=("Segoe UI", 10))
    combo_docentes.pack(fill="x", padx=15, pady=4)

    dict_docentes = {}

    def action_crear_g():
        g = entry_g_nom.get().strip()
        doc_sel = combo_docentes.get()
        if not g or not doc_sel:
            messagebox.showwarning("Atención", "Escribe el nombre del grupo y selecciona un docente.")
            return
        doc_id = dict_docentes[doc_sel]
        ok, msg = crear_grupo_bd(g, doc_id)
        messagebox.showinfo("Resultado", msg)
        if ok:
            actualizar_combos()

    tk.Button(f_left, text="CREAR GRUPO", command=action_crear_g, bg=COLOR_ACCENT, fg=COLOR_BG_DARK,
              font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(fill="x", padx=15, pady=10, ipady=5)

    # Lado Derecho: Asignar Alumnos a Grupos
    tk.Label(f_right, text="3. ASIGNAR ALUMNOS A GRUPOS", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD,
             fg=COLOR_ACCENT).pack(pady=(15, 10), padx=15, anchor="w")

    f_asig = tk.Frame(f_right, bg=COLOR_CARD)
    f_asig.pack(fill="x", padx=15, pady=5)

    tk.Label(f_asig, text="Alumno:", font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(side="left", padx=5)
    combo_alumnos = ttk.Combobox(f_asig, state="readonly", font=("Segoe UI", 10), width=20)
    combo_alumnos.pack(side="left", padx=5)

    tk.Label(f_asig, text="Asignar al Grupo:", font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(
        side="left", padx=5)
    combo_grupos_asig = ttk.Combobox(f_asig, state="readonly", font=("Segoe UI", 10), width=20)
    combo_grupos_asig.pack(side="left", padx=5)

    dict_alumnos = {}
    dict_grupos = {}

    def action_asignar_alum():
        a_sel = combo_alumnos.get()
        g_sel = combo_grupos_asig.get()
        if not a_sel or not g_sel:
            messagebox.showwarning("Atención", "Selecciona un alumno y un grupo.")
            return
        asignar_alumno_a_grupo(dict_alumnos[a_sel], dict_grupos[g_sel])
        messagebox.showinfo("Éxito", f"Alumno {a_sel} asignado al grupo {g_sel}.")
        actualizar_tabla_grupos()

    tk.Button(f_asig, text="ASIGNAR", command=action_asignar_alum, bg=COLOR_ACCENT, fg=COLOR_BG_DARK,
              font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(side="left", padx=10, ipadx=10, ipady=4)

    # Tabla de Grupos
    tabla_g = ttk.Treeview(f_right, columns=("id", "grupo", "docente"), show="headings", height=12)
    tabla_g.heading("id", text="ID")
    tabla_g.heading("grupo", text="Grupo")
    tabla_g.heading("docente", text="Docente Asignado")
    tabla_g.column("id", width=50, anchor="center")
    tabla_g.column("grupo", width=150)
    tabla_g.column("docente", width=250)
    tabla_g.pack(fill="both", expand=True, padx=15, pady=15)

    def actualizar_tabla_grupos():
        for r in tabla_g.get_children():
            tabla_g.delete(r)
        for g in obtener_grupos_con_docente():
            tabla_g.insert("", "end", values=(g[0], g[1], g[2]))

    def actualizar_combos():
        # Docentes
        dict_docentes.clear()
        docentes = obtener_docentes()
        vals_d = [d[1] for d in docentes]
        for d in docentes:
            dict_docentes[d[1]] = d[0]
        combo_docentes["values"] = vals_d
        if vals_d: combo_docentes.set(vals_d[0])

        # Alumnos
        dict_alumnos.clear()
        alumnos = obtener_alumnos_sin_grupo()
        vals_a = [a[1] for a in alumnos]
        for a in alumnos:
            dict_alumnos[a[1]] = a[0]
        combo_alumnos["values"] = vals_a
        if vals_a: combo_alumnos.set(vals_a[0])

        # Grupos
        dict_grupos.clear()
        grupos = obtener_grupos_con_docente()
        vals_g = [g[1] for g in grupos]
        for g in grupos:
            dict_grupos[g[1]] = g[0]
        combo_grupos_asig["values"] = vals_g
        if vals_g: combo_grupos_asig.set(vals_g[0])

        actualizar_tabla_grupos()

    actualizar_combos()
    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.mainloop()