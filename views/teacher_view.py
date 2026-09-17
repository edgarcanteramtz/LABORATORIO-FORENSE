import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Ruta absoluta hacia la base de datos
DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

# ==========================================
# PALETA DE COLORES "HUD FORENSIC / HIGH-TECH"
# ==========================================
COLOR_BG_DARK = "#05070A"      # Negro abisal
COLOR_CARD = "#090D18"         # Gris naval ultra oscuro
COLOR_ACCENT = "#00F0FF"       # Cian neón principal
COLOR_ACCENT_HOVER = "#00C4D4" # Cian de respuesta hover
COLOR_TEXT_LIGHT = "#FFFFFF"   # Blanco puro
COLOR_TEXT_MUTED = "#64748B"   # Gris técnico sutil
COLOR_ENTRY_BG = "#0E1524"     # Fondo de entradas más oscuro que la tarjeta
COLOR_BORDER = "#1E293B"       # Borde base de componentes
COLOR_BORDER_FOCUS = "#00F0FF" # Borde activo al enfocar
COLOR_DANGER = "#E63946"       # Rojo alerta elegante
COLOR_DANGER_HOVER = "#D62828"

def aplicar_hover(boton, color_normal, color_hover):
    """Efecto visual hover para botones."""
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))

def obtener_conexion():
    return sqlite3.connect(RUTA_DB)

def abrir_panel_docente(usuario):
    """Ventana principal para el rol de Docente."""
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel Docente ({usuario})")
    ventana.attributes('-fullscreen', True)  # Pantalla completa
    ventana.configure(bg=COLOR_BG_DARK)

    ventana.attributes("-alpha", 0.0)

    def animar_entrada(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            ventana.attributes("-alpha", alpha)
            ventana.after(20, lambda: animar_entrada(alpha))

    # Configuración de estilos modernos para ttk (Pestañas y Treeview)
    style = ttk.Style()
    style.theme_use("clam")

    # Estilo de Pestañas
    style.configure("TNotebook", background=COLOR_BG_DARK, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_MUTED, padding=[25, 12], font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", 
              background=[("selected", COLOR_CARD)], 
              foreground=[("selected", COLOR_ACCENT)])
    
    style.configure("TFrame", background=COLOR_CARD)

    # Estilo HUD para la Tabla de Datos (Treeview)
    style.configure("Treeview", 
                    background=COLOR_ENTRY_BG, 
                    foreground=COLOR_TEXT_LIGHT, 
                    fieldbackground=COLOR_ENTRY_BG, 
                    borderwidth=0, 
                    rowheight=35, # Filas más anchas para que respiren
                    font=("Segoe UI", 10))
    
    # Iluminar la fila seleccionada
    style.map('Treeview', 
              background=[('selected', COLOR_BORDER)], 
              foreground=[('selected', COLOR_ACCENT)])
    
    # Estilo de las cabeceras de la tabla
    style.configure("Treeview.Heading", 
                    background=COLOR_CARD, 
                    foreground=COLOR_TEXT_MUTED, 
                    borderwidth=1, 
                    relief="flat",
                    font=("Segoe UI", 9, "bold"))
    style.map("Treeview.Heading", background=[('active', COLOR_BORDER)])

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=40, pady=30)

    # -------------------------------------------------------------
    # PESTAÑA 1: REPORTE DE CALIFICACIONES DE ALUMNOS
    # -------------------------------------------------------------
    tab_notas = ttk.Frame(pestanas)
    pestanas.add(tab_notas, text="📊 Calificaciones de Alumnos")

    card_notas = tk.Frame(tab_notas, bg=COLOR_CARD, bd=0)
    card_notas.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    tk.Label(card_notas, text="HISTORIAL DE EVALUACIONES FORENSES", font=("Segoe UI", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(pady=(20, 15))

    # Marco externo e interno para efecto visual
    frame_tabla_notas = tk.Frame(card_notas, bg=COLOR_BORDER, bd=0)
    frame_tabla_notas.pack(fill="both", expand=True, padx=40, pady=(5, 15))
    inner_tabla_notas = tk.Frame(frame_tabla_notas, bg=COLOR_ENTRY_BG, bd=0)
    inner_tabla_notas.pack(fill="both", expand=True, padx=1, pady=1)

    # Scrollbar para la tabla
    scroll_notas = ttk.Scrollbar(inner_tabla_notas)
    scroll_notas.pack(side="right", fill="y")

    # Tabla de datos (Treeview)
    columnas = ("alumno", "unidad", "puntaje", "fecha")
    tabla_notas = ttk.Treeview(inner_tabla_notas, columns=columnas, show="headings", yscrollcommand=scroll_notas.set)

    tabla_notas.heading("alumno", text="ALUMNO")
    tabla_notas.heading("unidad", text="UNIDAD / TEMA")
    tabla_notas.heading("puntaje", text="CALIFICACIÓN")
    tabla_notas.heading("fecha", text="FECHA DE REALIZACIÓN")

    tabla_notas.column("alumno", width=250, anchor="w")
    tabla_notas.column("unidad", width=300, anchor="w")
    tabla_notas.column("puntaje", width=100, anchor="center")
    tabla_notas.column("fecha", width=180, anchor="center")

    tabla_notas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scroll_notas.config(command=tabla_notas.yview)

    def cargar_calificaciones():
        """Obtiene las notas registradas uniendo la tabla de calificaciones, usuarios y temas."""
        for item in tabla_notas.get_children():
            tabla_notas.delete(item)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nombre_completo, t.titulo, c.puntaje, c.fecha
            FROM calificaciones c
            JOIN usuarios u ON c.alumno_id = u.id
            JOIN temas t ON c.tema_id = t.id
            ORDER BY c.fecha DESC
        ''')
        filas = cursor.fetchall()
        conn.close()

        for fila in filas:
            # Formatear el puntaje visualmente
            fila_formateada = (fila[0], fila[1], f"{fila[2]} / 100", fila[3])
            tabla_notas.insert("", "end", values=fila_formateada)

    btn_actualizar_n = tk.Button(card_notas, text="ACTUALIZAR TABLA DE REGISTROS", command=cargar_calificaciones, font=("Segoe UI", 11, "bold"), bg=COLOR_BORDER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_ENTRY_BG, relief="flat", cursor="hand2", bd=0)
    btn_actualizar_n.pack(fill="x", padx=300, pady=(10, 25), ipady=8)
    aplicar_hover(btn_actualizar_n, COLOR_BORDER, COLOR_ENTRY_BG)

    # -------------------------------------------------------------
    # PESTAÑA 2: LISTA DE ALUMNOS REGISTRADOS
    # -------------------------------------------------------------
    tab_alumnos = ttk.Frame(pestanas)
    pestanas.add(tab_alumnos, text="👥 Lista de Alumnos")

    card_alumnos = tk.Frame(tab_alumnos, bg=COLOR_CARD, bd=0)
    card_alumnos.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    tk.Label(card_alumnos, text="ALUMNOS REGISTRADOS EN EL SISTEMA", font=("Segoe UI", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(pady=(20, 15))

    frame_tabla_alumnos = tk.Frame(card_alumnos, bg=COLOR_BORDER, bd=0)
    frame_tabla_alumnos.pack(fill="both", expand=True, padx=80, pady=(5, 15))
    inner_tabla_alumnos = tk.Frame(frame_tabla_alumnos, bg=COLOR_ENTRY_BG, bd=0)
    inner_tabla_alumnos.pack(fill="both", expand=True, padx=1, pady=1)

    scroll_alumnos = ttk.Scrollbar(inner_tabla_alumnos)
    scroll_alumnos.pack(side="right", fill="y")

    tabla_alumnos = ttk.Treeview(inner_tabla_alumnos, columns=("id", "nombre", "usuario"), show="headings", yscrollcommand=scroll_alumnos.set)
    tabla_alumnos.heading("id", text="ID")
    tabla_alumnos.heading("nombre", text="NOMBRE COMPLETO")
    tabla_alumnos.heading("usuario", text="IDENTIFICADOR (USUARIO)")

    tabla_alumnos.column("id", width=80, anchor="center")
    tabla_alumnos.column("nombre", width=400, anchor="w")
    tabla_alumnos.column("usuario", width=250, anchor="center")

    tabla_alumnos.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scroll_alumnos.config(command=tabla_alumnos.yview)

    def cargar_alumnos():
        for item in tabla_alumnos.get_children():
            tabla_alumnos.delete(item)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_completo, nombre_usuario FROM usuarios WHERE rol = 'alumno'")
        filas = cursor.fetchall()
        conn.close()

        for fila in filas:
            # Formatear el ID visualmente (ej. "USR-001")
            fila_formateada = (f"USR-{str(fila[0]).zfill(3)}", fila[1], fila[2])
            tabla_alumnos.insert("", "end", values=fila_formateada)

    btn_actualizar_a = tk.Button(card_alumnos, text="ACTUALIZAR LISTADO DE ALUMNOS", command=cargar_alumnos, font=("Segoe UI", 11, "bold"), bg=COLOR_BORDER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_ENTRY_BG, relief="flat", cursor="hand2", bd=0)
    btn_actualizar_a.pack(fill="x", padx=300, pady=(10, 25), ipady=8)
    aplicar_hover(btn_actualizar_a, COLOR_BORDER, COLOR_ENTRY_BG)

    # Cargar datos al abrir
    cargar_calificaciones()
    cargar_alumnos()

    # =============================================================
    # BOTÓN GLOBAL: CERRAR SESIÓN
    # =============================================================
    btn_cerrar = tk.Button(
        ventana, 
        text="CERRAR SESIÓN DE DOCENTE", 
        command=ventana.destroy, 
        font=("Segoe UI", 10, "bold"), 
        bg=COLOR_DANGER, 
        fg=COLOR_TEXT_LIGHT, 
        activebackground=COLOR_DANGER_HOVER, 
        activeforeground=COLOR_TEXT_LIGHT,
        relief="flat", 
        cursor="hand2",
        bd=0
    )
    btn_cerrar.pack(fill="x", padx=40, pady=(0, 25), ipady=12)
    aplicar_hover(btn_cerrar, COLOR_DANGER, COLOR_DANGER_HOVER)

    # Atajos de teclado
    ventana.bind("<Escape>", lambda e: ventana.destroy())

    ventana.after(100, animar_entrada)
    ventana.mainloop()