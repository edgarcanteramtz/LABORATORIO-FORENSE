import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Calculamos la ruta absoluta hacia la base de datos
DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

# ==========================================
# PALETA DE COLORES "HUD FORENSIC / HIGH-TECH"
# (Ajustada para máxima elegancia)
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

def obtener_conexion():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect(RUTA_DB)

# Función auxiliar global para efectos hover de botones
def aplicar_hover(boton, color_normal, color_hover):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))

def abrir_panel_admin(usuario):
    """Ventana principal del Administrador en Pantalla Completa con diseño HUD y animaciones."""
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel Administrador ({usuario})")
    ventana.attributes('-fullscreen', True)  # Pantalla completa real
    ventana.configure(bg=COLOR_BG_DARK)

    # Iniciar completamente transparente para aplicar efecto Fade-In fluido
    ventana.attributes("-alpha", 0.0)

    def animar_entrada(alpha=0.0):
        """Efecto de aparición gradual tipo HUD militar/tecnológico."""
        if alpha < 1.0:
            alpha += 0.05
            ventana.attributes("-alpha", alpha)
            ventana.after(20, lambda: animar_entrada(alpha))

    # Configuración de estilos modernos para ttk (Pestañas, Combobox, etc.)
    style = ttk.Style()
    style.theme_use("clam")

    # Estilo refinado del Notebook (Pestañas)
    style.configure("TNotebook", background=COLOR_BG_DARK, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_MUTED, padding=[25, 12], font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", 
              background=[("selected", COLOR_CARD)], 
              foreground=[("selected", COLOR_ACCENT)])
    
    style.configure("TFrame", background=COLOR_CARD)
    style.configure("TCombobox", fieldbackground=COLOR_ENTRY_BG, background=COLOR_BORDER, foreground=COLOR_TEXT_LIGHT, borderwidth=0)

    # Contenedor principal de pestañas
    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=40, pady=30)

    # Función auxiliar para crear inputs estilizados con borde dinámico (Doble Frame)
    def crear_campo_form(parent, label_text, is_password=False, is_combo=False, combo_values=None):
        lbl = tk.Label(parent, text=label_text, font=("Segoe UI", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        lbl.pack(fill="x", padx=50, pady=(10, 5))
        
        frame_entry = tk.Frame(parent, bg=COLOR_BORDER, bd=0)
        frame_entry.pack(fill="x", padx=50, pady=(0, 5))

        inner_frame = tk.Frame(frame_entry, bg=COLOR_ENTRY_BG, bd=0)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

        if is_combo:
            widget = ttk.Combobox(inner_frame, values=combo_values, state="readonly", font=("Segoe UI", 11))
            widget.set(combo_values[0])
            widget.pack(fill="x", padx=5, pady=5)
        else:
            widget = tk.Entry(inner_frame, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_ACCENT, relief="flat", bd=0)
            if is_password:
                widget.config(show="●")
            widget.pack(fill="x", padx=12, pady=10)

            def on_focus_in(e):
                frame_entry.config(bg=COLOR_BORDER_FOCUS)
                lbl.config(fg=COLOR_ACCENT)
            def on_focus_out(e):
                frame_entry.config(bg=COLOR_BORDER)
                lbl.config(fg=COLOR_TEXT_MUTED)

            widget.bind("<FocusIn>", on_focus_in)
            widget.bind("<FocusOut>", on_focus_out)
            
        return widget

    # =============================================================
    # PESTAÑA 1: GESTIÓN DE USUARIOS
    # =============================================================
    tab_usuarios = ttk.Frame(pestanas)
    pestanas.add(tab_usuarios, text="👤 Registrar Usuarios")

    card_user = tk.Frame(tab_usuarios, bg=COLOR_CARD, bd=0)
    card_user.place(relx=0.5, rely=0.5, anchor="center", width=600, height=560)

    tk.Label(card_user, text="ALTA DE NUEVOS USUARIOS", font=("Segoe UI", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(pady=(40, 20))

    entry_nombre = crear_campo_form(card_user, "NOMBRE COMPLETO")
    entry_user = crear_campo_form(card_user, "NOMBRE DE USUARIO")
    entry_pass = crear_campo_form(card_user, "CONTRASEÑA", is_password=True)
    combo_rol = crear_campo_form(card_user, "ROL DEL USUARIO", is_combo=True, combo_values=["alumno", "docente", "admin"])

    def guardar_usuario():
        nom = entry_nombre.get().strip()
        usr = entry_user.get().strip()
        pwd = entry_pass.get().strip()
        rol = combo_rol.get()

        if not nom or not usr or not pwd:
            messagebox.showwarning("Atención", "Por favor completa todos los campos requeridos.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre_completo, nombre_usuario, password, rol) VALUES (?, ?, ?, ?)",
                (nom, usr, pwd, rol)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", f"Usuario '{usr}' registrado correctamente como {rol}.")
            entry_nombre.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe en el sistema.")

    btn_guardar_u = tk.Button(card_user, text="REGISTRAR USUARIO", command=guardar_usuario, font=("Segoe UI", 11, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER, relief="flat", cursor="hand2", bd=0)
    btn_guardar_u.pack(fill="x", padx=50, pady=(35, 20), ipady=12)
    aplicar_hover(btn_guardar_u, COLOR_ACCENT, COLOR_ACCENT_HOVER)

    # =============================================================
    # PESTAÑA 2: GESTIÓN DEL TEMARIO
    # =============================================================
    tab_temario = ttk.Frame(pestanas)
    pestanas.add(tab_temario, text="📚 Agregar Temas")

    card_tema = tk.Frame(tab_temario, bg=COLOR_CARD, bd=0)
    card_tema.place(relx=0.5, rely=0.5, anchor="center", width=700, height=600)

    tk.Label(card_tema, text="GESTIÓN DE UNIDADES Y TEMARIO", font=("Segoe UI", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(pady=(35, 15))

    # Helper local para campos de Temario (reutiliza el estilo doble frame)
    def crear_campo_temario(parent, label_text, is_text_area=False):
        lbl = tk.Label(parent, text=label_text, font=("Segoe UI", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w")
        lbl.pack(fill="x", padx=50, pady=(10, 5))
        
        frame_entry = tk.Frame(parent, bg=COLOR_BORDER, bd=0)
        frame_entry.pack(fill="x", padx=50, pady=(0, 5))
        
        inner_frame = tk.Frame(frame_entry, bg=COLOR_ENTRY_BG, bd=0)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

        if is_text_area:
            widget = tk.Text(inner_frame, height=6, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_ACCENT, relief="flat", bd=0)
            widget.pack(fill="x", padx=12, pady=10)
        else:
            widget = tk.Entry(inner_frame, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_ACCENT, relief="flat", bd=0)
            widget.pack(fill="x", padx=12, pady=10)

        def on_focus_in(e):
            frame_entry.config(bg=COLOR_BORDER_FOCUS)
            lbl.config(fg=COLOR_ACCENT)
        def on_focus_out(e):
            frame_entry.config(bg=COLOR_BORDER)
            lbl.config(fg=COLOR_TEXT_MUTED)

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)
        return widget

    entry_unidad = crear_campo_temario(card_tema, "NÚMERO DE UNIDAD")
    entry_titulo_tema = crear_campo_temario(card_tema, "TÍTULO DE LA UNIDAD")
    text_contenido_tema = crear_campo_temario(card_tema, "CONTENIDO TEÓRICO / SUBTEMAS", is_text_area=True)

    def guardar_tema():
        num_u = entry_unidad.get().strip()
        tit = entry_titulo_tema.get().strip()
        cont = text_contenido_tema.get("1.0", tk.END).strip()

        if not num_u.isdigit() or not tit or not cont:
            messagebox.showwarning("Atención", "Ingresa un número válido de unidad, título y contenido.")
            return

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO temas (unidad, titulo, contenido_teorico) VALUES (?, ?, ?)",
            (int(num_u), tit, cont)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Unidad {num_u} agregada correctamente.")
        entry_unidad.delete(0, tk.END)
        entry_titulo_tema.delete(0, tk.END)
        text_contenido_tema.delete("1.0", tk.END)
        actualizar_combo_temas()

    btn_guardar_t = tk.Button(card_tema, text="GUARDAR UNIDAD", command=guardar_tema, font=("Segoe UI", 11, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER, relief="flat", cursor="hand2", bd=0)
    btn_guardar_t.pack(fill="x", padx=50, pady=(25, 20), ipady=12)
    aplicar_hover(btn_guardar_t, COLOR_ACCENT, COLOR_ACCENT_HOVER)


    # =============================================================
    # PESTAÑA 3: GESTIÓN DE PREGUNTAS
    # =============================================================
    tab_preguntas = ttk.Frame(pestanas)
    pestanas.add(tab_preguntas, text="📝 Agregar Preguntas")

    card_preg = tk.Frame(tab_preguntas, bg=COLOR_CARD, bd=0)
    card_preg.place(relx=0.5, rely=0.5, anchor="center", width=760, height=720)

    tk.Label(card_preg, text="BANCO DE PREGUNTAS DE EVALUACIÓN", font=("Segoe UI", 16, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(pady=(30, 15))

    tk.Label(card_preg, text="SELECCIONAR UNIDAD / TEMA", font=("Segoe UI", 8, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(fill="x", padx=40, pady=(0, 5))
    combo_temas_preg = ttk.Combobox(card_preg, state="readonly", font=("Segoe UI", 10))
    combo_temas_preg.pack(fill="x", padx=40, pady=(0, 20))

    lista_temas_ids = []

    def actualizar_combo_temas():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, unidad, titulo FROM temas ORDER BY unidad ASC")
        filas = cursor.fetchall()
        conn.close()

        lista_temas_ids.clear()
        opciones = []
        for f_id, u, t in filas:
            lista_temas_ids.append(f_id)
            opciones.append(f"Unidad {u}: {t}")

        combo_temas_preg["values"] = opciones
        if opciones:
            combo_temas_preg.current(0)

    # Estilo refinado para las filas de preguntas (Doble Frame horizontal)
    def crear_fila_input(parent, label_text):
        f = tk.Frame(parent, bg=COLOR_CARD)
        f.pack(fill="x", padx=40, pady=6)
        
        lbl = tk.Label(f, text=label_text, font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, width=12, anchor="w")
        lbl.pack(side="left")
        
        frame_entry = tk.Frame(f, bg=COLOR_BORDER, bd=0)
        frame_entry.pack(side="right", expand=True, fill="x")
        
        inner_frame = tk.Frame(frame_entry, bg=COLOR_ENTRY_BG, bd=0)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

        ent = tk.Entry(inner_frame, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_ACCENT, relief="flat", bd=0)
        ent.pack(fill="x", padx=10, pady=8)

        def on_focus_in(e):
            frame_entry.config(bg=COLOR_BORDER_FOCUS)
            lbl.config(fg=COLOR_ACCENT)
        def on_focus_out(e):
            frame_entry.config(bg=COLOR_BORDER)
            lbl.config(fg=COLOR_TEXT_MUTED)

        ent.bind("<FocusIn>", on_focus_in)
        ent.bind("<FocusOut>", on_focus_out)
        return ent

    entry_preg = crear_fila_input(card_preg, "Pregunta:")
    entry_op_a = crear_fila_input(card_preg, "Opción A:")
    entry_op_b = crear_fila_input(card_preg, "Opción B:")
    entry_op_c = crear_fila_input(card_preg, "Opción C:")
    entry_op_d = crear_fila_input(card_preg, "Opción D:")

    # Fila para respuesta correcta
    f_rc = tk.Frame(card_preg, bg=COLOR_CARD)
    f_rc.pack(fill="x", padx=40, pady=(15, 10))
    tk.Label(f_rc, text="Correcta:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, width=12, anchor="w").pack(side="left")
    combo_correcta = ttk.Combobox(f_rc, values=["A", "B", "C", "D"], state="readonly", font=("Segoe UI", 10), width=15)
    combo_correcta.set("A")
    combo_correcta.pack(side="left")

    def guardar_pregunta():
        idx = combo_temas_preg.current()
        if idx == -1 or not lista_temas_ids:
            messagebox.showwarning("Atención", "Selecciona un tema primero.")
            return

        tema_id = lista_temas_ids[idx]
        p = entry_preg.get().strip()
        a = entry_op_a.get().strip()
        b = entry_op_b.get().strip()
        c = entry_op_c.get().strip()
        d = entry_op_d.get().strip()
        rc = combo_correcta.get()

        if not p or not a or not b or not c or not d:
            messagebox.showwarning("Atención", "Completa la pregunta y todas las opciones.")
            return

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (tema_id, p, a, b, c, d, rc)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Pregunta registrada correctamente.")
        entry_preg.delete(0, tk.END)
        entry_op_a.delete(0, tk.END)
        entry_op_b.delete(0, tk.END)
        entry_op_c.delete(0, tk.END)
        entry_op_d.delete(0, tk.END)

    btn_guardar_p = tk.Button(card_preg, text="GUARDAR PREGUNTA", command=guardar_pregunta, font=("Segoe UI", 11, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER, relief="flat", cursor="hand2", bd=0)
    btn_guardar_p.pack(fill="x", padx=40, pady=(20, 15), ipady=12)
    aplicar_hover(btn_guardar_p, COLOR_ACCENT, COLOR_ACCENT_HOVER)

    actualizar_combo_temas()

    # Botón inferior para Cerrar Sesión (Ahora con hover rojo intenso)
    btn_cerrar = tk.Button(
        ventana, 
        text="CERRAR SESIÓN DE ADMINISTRADOR", 
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

    # Atajo global de teclado para salir de pantalla completa con ESC
    ventana.bind("<Escape>", lambda e: ventana.destroy())

    # Ejecutar animación de entrada
    ventana.after(100, animar_entrada)

    ventana.mainloop()