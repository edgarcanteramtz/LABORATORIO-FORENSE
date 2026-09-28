import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

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
COLOR_DANGER = "#E63946"
COLOR_DANGER_HOVER = "#D62828"
COLOR_SUCCESS = "#2EC4B6"


def aplicar_hover(boton, color_normal, color_hover):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))


# ==========================================
# CONSULTAS Y OPERACIONES EN BASE DE DATOS
# ==========================================
def obtener_unidades_bd():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, unidad, titulo, contenido_teorico FROM temas ORDER BY unidad ASC")
    temas = cursor.fetchall()
    conexion.close()
    return temas


def actualizar_contenido_teorico(tema_id, titulo, contenido):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE temas SET titulo = ?, contenido_teorico = ? WHERE id = ?",
        (titulo, contenido, tema_id)
    )
    conexion.commit()
    conexion.close()


def agregar_pregunta_bd(tema_id, pregunta, op_a, op_b, op_c, op_d, resp_correcta):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tema_id, pregunta, op_a, op_b, op_c, op_d, resp_correcta))
    conexion.commit()
    conexion.close()


def obtener_preguntas_por_tema(tema_id):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta FROM preguntas WHERE tema_id = ?",
        (tema_id,)
    )
    preguntas = cursor.fetchall()
    conexion.close()
    return preguntas


def eliminar_pregunta_bd(pregunta_id):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM preguntas WHERE id = ?", (pregunta_id,))
    conexion.commit()
    conexion.close()


def obtener_usuarios_bd():
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_usuario, rol FROM usuarios ORDER BY id ASC")
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def agregar_usuario_bd(nombre, password, rol):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)",
            (nombre, password, rol)
        )
        conexion.commit()
        conexion.close()
        return True, "Usuario registrado exitosamente."
    except sqlite3.IntegrityError:
        conexion.close()
        return False, "El nombre de usuario ya existe."


def eliminar_usuario_bd(user_id):
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conexion.commit()
    conexion.close()


# ==========================================
# INTERFAZ GRÁFICA DEL ADMINISTRADOR
# ==========================================
def abrir_panel_admin(usuario):
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel de Administración ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg=COLOR_BG_DARK)
    ventana.attributes("-alpha", 0.0)

    def animar_entrada(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            ventana.attributes("-alpha", alpha)
            ventana.after(20, lambda: animar_entrada(alpha))

    # Estilos TTK
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=30)
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("TNotebook", background=COLOR_CARD, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_MUTED, padding=[18, 10],
                    font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", COLOR_CARD)], foreground=[("selected", COLOR_ACCENT)])

    # Contenedor Principal
    container_main = tk.Frame(ventana, bg=COLOR_BG_DARK)
    container_main.pack(fill="both", expand=True, padx=20, pady=20)

    # Header Superior
    header = tk.Frame(container_main, bg=COLOR_CARD, height=60)
    header.pack(fill="x", pady=(0, 15))
    header.pack_propagate(False)

    tk.Label(header, text="⚙️ MÓDULO ADMINISTRADOR DE CONTENIDO Y SISTEMA", font=("Segoe UI", 14, "bold"),
             bg=COLOR_CARD, fg=COLOR_ACCENT).pack(side="left", padx=20)

    btn_cerrar = tk.Button(header, text="CERRAR SESIÓN", command=ventana.destroy, font=("Segoe UI", 10, "bold"),
                           bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_DANGER_HOVER, relief="flat",
                           cursor="hand2", bd=0)
    btn_cerrar.pack(side="right", padx=15, pady=10, ipadx=15)
    aplicar_hover(btn_cerrar, COLOR_DANGER, COLOR_DANGER_HOVER)

    # Pestañas de Navegación
    notebook = ttk.Notebook(container_main)
    notebook.pack(fill="both", expand=True)

    # =============================================================
    # PESTAÑA 1: GESTIÓN DE CONTENIDO TEÓRICO Y SUBTEMAS
    # =============================================================
    tab_teoria = ttk.Frame(notebook)
    notebook.add(tab_teoria, text="📚 Gestión de Teoría y Subtemas")

    f_teoria_main = tk.Frame(tab_teoria, bg=COLOR_CARD)
    f_teoria_main.pack(fill="both", expand=True, padx=15, pady=15)

    # Selector de Unidad
    f_sel_u = tk.Frame(f_teoria_main, bg=COLOR_CARD)
    f_sel_u.pack(fill="x", padx=15, pady=10)

    tk.Label(f_sel_u, text="Seleccionar Unidad:", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD,
             fg=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 10))

    combo_unidades = ttk.Combobox(f_sel_u, state="readonly", font=("Segoe UI", 10), width=45)
    combo_unidades.pack(side="left", padx=5)

    # Título de la unidad
    f_tit_u = tk.Frame(f_teoria_main, bg=COLOR_CARD)
    f_tit_u.pack(fill="x", padx=15, pady=5)

    tk.Label(f_tit_u, text="Título de la Unidad:", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD,
             fg=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 10))

    entry_titulo_u = tk.Entry(f_tit_u, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0, relief="flat")
    entry_titulo_u.pack(side="left", fill="x", expand=True, ipady=4)

    # Editor de texto extenso para teoría y subtemas
    f_txt_u = tk.Frame(f_teoria_main, bg=COLOR_CARD)
    f_txt_u.pack(fill="both", expand=True, padx=15, pady=10)

    tk.Label(f_txt_u, text="Contenido Teórico Completo (Escribe o extiende los subtemas 1.1, 1.2, etc.):",
             font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 5))

    scroll_t = ttk.Scrollbar(f_txt_u)
    scroll_t.pack(side="right", fill="y")

    txt_teoria_editor = tk.Text(f_txt_u, wrap="word", font=("Consolas", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT,
                                relief="flat", bd=0, padx=10, pady=10, yscrollcommand=scroll_t.set)
    txt_teoria_editor = tk.Text(f_txt_u, wrap="word", font=("Consolas", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT,
                                relief="flat", bd=0, padx=10, pady=10, yscrollcommand=scroll_t.set)
    txt_teoria_editor.pack(side="left", fill="both", expand=True)
    scroll_t.config(command=txt_teoria_editor.yview)

    # --- NUEVO: MENÚ CONTEXTUAL PARA COPIAR Y PEGAR CÓMODAMENTE ---
    menu_contextual = tk.Menu(txt_teoria_editor, tearoff=0, bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, bd=0,
                              activebackground=COLOR_ACCENT, activeforeground=COLOR_BG_DARK)
    menu_contextual.add_command(label="✂️ Cortar", command=lambda: txt_teoria_editor.event_generate("<<Cut>>"))
    menu_contextual.add_command(label="📋 Copiar", command=lambda: txt_teoria_editor.event_generate("<<Copy>>"))
    menu_contextual.add_command(label="📝 Pegar", command=lambda: txt_teoria_editor.event_generate("<<Paste>>"))
    menu_contextual.add_separator()
    menu_contextual.add_command(label="Seleccionar Todo",
                                command=lambda: txt_teoria_editor.tag_add("sel", "1.0", "end"))

    def mostrar_menu(event):
        menu_contextual.tk_popup(event.x_root, event.y_root)

    txt_teoria_editor.bind("<Button-3>", mostrar_menu)  # Activa el clic derecho
    # --------------------------------------------------------------

    txt_teoria_editor.pack(side="left", fill="both", expand=True)
    scroll_t.config(command=txt_teoria_editor.yview)

    unidades_datos = []

    def cargar_datos_unidades():
        nonlocal unidades_datos
        unidades_datos = obtener_unidades_bd()
        combo_unidades['values'] = [f"Unidad {u[1]}: {u[2]}" for u in unidades_datos]
        if unidades_datos:
            combo_unidades.current(0)
            al_seleccionar_unidad_combo(None)

    def al_seleccionar_unidad_combo(event):
        idx = combo_unidades.current()
        if 0 <= idx < len(unidades_datos):
            u = unidades_datos[idx]
            entry_titulo_u.delete(0, tk.END)
            entry_titulo_u.insert(0, u[2])

            txt_teoria_editor.delete("1.0", tk.END)
            txt_teoria_editor.insert("1.0", u[3] if u[3] else "")

    combo_unidades.bind("<<ComboboxSelected>>", al_seleccionar_unidad_combo)

    def guardar_teoria_unidad():
        idx = combo_unidades.current()
        if idx < 0:
            messagebox.showwarning("Atención", "Selecciona una unidad primero.")
            return

        tema_id = unidades_datos[idx][0]
        nuevo_titulo = entry_titulo_u.get().strip()
        nuevo_contenido = txt_teoria_editor.get("1.0", tk.END).strip()

        if not nuevo_titulo:
            messagebox.showwarning("Atención", "El título de la unidad no puede estar vacío.")
            return

        actualizar_contenido_teorico(tema_id, nuevo_titulo, nuevo_contenido)
        messagebox.showinfo("Éxito", "¡Contenido teórico guardado exitosamente!\nEstará disponible para todos los docentes y alumnos.")
        cargar_datos_unidades()

    btn_guardar_teoria = tk.Button(f_teoria_main, text="💾 GUARDAR / ACTUALIZAR TEORÍA Y SUBTEMAS",
                                   command=guardar_teoria_unidad, font=("Segoe UI", 10, "bold"),
                                   bg=COLOR_SUCCESS, fg=COLOR_BG_DARK, bd=0, cursor="hand2")
    btn_guardar_teoria.pack(pady=10, ipady=8, ipadx=20)
    aplicar_hover(btn_guardar_teoria, COLOR_SUCCESS, COLOR_ACCENT)

    # =============================================================
    # PESTAÑA 2: BANCO DE PREGUNTAS (SELECCIÓN POR UNIDAD)
    # =============================================================
    tab_preguntas = ttk.Frame(notebook)
    notebook.add(tab_preguntas, text="📝 Banco de Preguntas")

    f_preg_main = tk.Frame(tab_preguntas, bg=COLOR_CARD)
    f_preg_main.pack(fill="both", expand=True, padx=15, pady=15)

    # Selector de unidad destino para preguntas
    f_top_q = tk.Frame(f_preg_main, bg=COLOR_CARD)
    f_top_q.pack(fill="x", padx=15, pady=10)

    tk.Label(f_top_q, text="Seleccionar Unidad Destino:", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD,
             fg=COLOR_ACCENT).pack(side="left", padx=(0, 10))

    combo_q_unidades = ttk.Combobox(f_top_q, state="readonly", font=("Segoe UI", 10), width=45)
    combo_q_unidades.pack(side="left", padx=5)

    # Formulario para agregar preguntas
    f_form_q = tk.LabelFrame(f_preg_main, text=" Agregar Nueva Pregunta ", font=("Segoe UI", 10, "bold"),
                             bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, bd=1, relief="solid")
    f_form_q.pack(fill="x", padx=15, pady=10)

    tk.Label(f_form_q, text="Pregunta:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(
        row=0, column=0, sticky="w", padx=10, pady=5)
    entry_q_texto = tk.Entry(f_form_q, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_q_texto.grid(row=0, column=1, columnspan=3, sticky="ew", padx=10, pady=5, ipady=4)

    tk.Label(f_form_q, text="Opción A:", font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(
        row=1, column=0, sticky="w", padx=10, pady=3)
    entry_op_a = tk.Entry(f_form_q, font=("Segoe UI", 9), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_op_a.grid(row=1, column=1, sticky="ew", padx=10, pady=3, ipady=3)

    tk.Label(f_form_q, text="Opción B:", font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(
        row=1, column=2, sticky="w", padx=10, pady=3)
    entry_op_b = tk.Entry(f_form_q, font=("Segoe UI", 9), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_op_b.grid(row=1, column=3, sticky="ew", padx=10, pady=3, ipady=3)

    tk.Label(f_form_q, text="Opción C:", font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(
        row=2, column=0, sticky="w", padx=10, pady=3)
    entry_op_c = tk.Entry(f_form_q, font=("Segoe UI", 9), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_op_c.grid(row=2, column=1, sticky="ew", padx=10, pady=3, ipady=3)

    tk.Label(f_form_q, text="Opción D:", font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).grid(
        row=2, column=2, sticky="w", padx=10, pady=3)
    entry_op_d = tk.Entry(f_form_q, font=("Segoe UI", 9), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_op_d.grid(row=2, column=3, sticky="ew", padx=10, pady=3, ipady=3)

    tk.Label(f_form_q, text="Respuesta Correcta:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT).grid(
        row=3, column=0, sticky="w", padx=10, pady=5)
    combo_correcta = ttk.Combobox(f_form_q, values=["A", "B", "C", "D"], state="readonly", width=10)
    combo_correcta.set("A")
    combo_correcta.grid(row=3, column=1, sticky="w", padx=10, pady=5)

    f_form_q.columnconfigure(1, weight=1)
    f_form_q.columnconfigure(3, weight=1)

    def guardar_pregunta():
        idx = combo_q_unidades.current()
        if idx < 0:
            messagebox.showwarning("Atención", "Selecciona la unidad destino.")
            return

        tema_id = unidades_datos[idx][0]
        preg = entry_q_texto.get().strip()
        oa = entry_op_a.get().strip()
        ob = entry_op_b.get().strip()
        oc = entry_op_c.get().strip()
        od = entry_op_d.get().strip()
        rc = combo_correcta.get()

        if not (preg and oa and ob and oc and od):
            messagebox.showwarning("Atención", "Escribe la pregunta y todas sus opciones.")
            return

        agregar_pregunta_bd(tema_id, preg, oa, ob, oc, od, rc)
        messagebox.showinfo("Éxito", "Pregunta añadida a la unidad seleccionada.")

        # Limpiar formulario
        entry_q_texto.delete(0, tk.END)
        entry_op_a.delete(0, tk.END)
        entry_op_b.delete(0, tk.END)
        entry_op_c.delete(0, tk.END)
        entry_op_d.delete(0, tk.END)
        cargar_preguntas_unidad_tabla()

    btn_add_q = tk.Button(f_form_q, text="➕ AGREGAR PREGUNTA", command=guardar_pregunta,
                          font=("Segoe UI", 9, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, bd=0, cursor="hand2")
    btn_add_q.grid(row=3, column=3, sticky="e", padx=10, pady=8, ipadx=15, ipady=4)

    # Tabla de preguntas existentes por unidad
    f_tbl_q = tk.Frame(f_preg_main, bg=COLOR_CARD)
    f_tbl_q.pack(fill="both", expand=True, padx=15, pady=10)

    tabla_q = ttk.Treeview(f_tbl_q, columns=("id", "preg", "op_a", "op_b", "op_c", "op_d", "resp"), show="headings", height=6)
    tabla_q.heading("id", text="ID")
    tabla_q.heading("preg", text="Pregunta")
    tabla_q.heading("op_a", text="A")
    tabla_q.heading("op_b", text="B")
    tabla_q.heading("op_c", text="C")
    tabla_q.heading("op_d", text="D")
    tabla_q.heading("resp", text="Correcta")

    tabla_q.column("id", width=40, anchor="center")
    tabla_q.column("preg", width=300)
    tabla_q.column("op_a", width=100)
    tabla_q.column("op_b", width=100)
    tabla_q.column("op_c", width=100)
    tabla_q.column("op_d", width=100)
    tabla_q.column("resp", width=70, anchor="center")
    tabla_q.pack(side="left", fill="both", expand=True)

    scroll_q_tbl = ttk.Scrollbar(f_tbl_q, orient="vertical", command=tabla_q.yview)
    tabla_q.configure(yscrollcommand=scroll_q_tbl.set)
    scroll_q_tbl.pack(side="right", fill="y")

    def cargar_preguntas_unidad_tabla():
        for item in tabla_q.get_children():
            tabla_q.delete(item)

        idx = combo_q_unidades.current()
        if 0 <= idx < len(unidades_datos):
            tema_id = unidades_datos[idx][0]
            pregs = obtener_preguntas_por_tema(tema_id)
            for p in pregs:
                tabla_q.insert("", "end", values=p)

    combo_q_unidades.bind("<<ComboboxSelected>>", lambda e: cargar_preguntas_unidad_tabla())

    def eliminar_pregunta_seleccionada():
        sel = tabla_q.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una pregunta para eliminar.")
            return
        q_id = tabla_q.item(sel[0])["values"][0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar la pregunta ID {q_id}?"):
            eliminar_pregunta_bd(q_id)
            cargar_preguntas_unidad_tabla()

    btn_del_q = tk.Button(f_preg_main, text="🗑️ ELIMINAR PREGUNTA SELECCIONADA", command=eliminar_pregunta_seleccionada,
                          font=("Segoe UI", 9, "bold"), bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2")
    btn_del_q.pack(anchor="e", padx=15, pady=(0, 10), ipady=5, ipadx=15)

    def sincronizar_combos():
        combo_q_unidades['values'] = combo_unidades['values']
        if unidades_datos:
            combo_q_unidades.current(0)
            cargar_preguntas_unidad_tabla()

    # =============================================================
    # PESTAÑA 3: GESTIÓN DE USUARIOS DEL SISTEMA
    # =============================================================
    tab_users = ttk.Frame(notebook)
    notebook.add(tab_users, text="👥 Usuarios del Sistema")

    f_u_main = tk.Frame(tab_users, bg=COLOR_CARD)
    f_u_main.pack(fill="both", expand=True, padx=15, pady=15)

    f_f_user = tk.Frame(f_u_main, bg=COLOR_ENTRY_BG)
    f_f_user.pack(fill="x", padx=15, pady=10)

    tk.Label(f_f_user, text="Nuevo Usuario:", font=("Segoe UI", 9, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(
        side="left", padx=10, pady=10)

    entry_u_name = tk.Entry(f_f_user, font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_u_name.pack(side="left", padx=5, ipady=3)

    tk.Label(f_f_user, text="Contraseña:", font=("Segoe UI", 9, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(
        side="left", padx=10)
    entry_u_pass = tk.Entry(f_f_user, font=("Segoe UI", 9), show="*", bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, bd=0)
    entry_u_pass.pack(side="left", padx=5, ipady=3)

    tk.Label(f_f_user, text="Rol:", font=("Segoe UI", 9, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(
        side="left", padx=10)
    combo_u_rol = ttk.Combobox(f_f_user, values=["alumno", "docente", "administrador"], state="readonly", width=12)
    combo_u_rol.set("alumno")
    combo_u_rol.pack(side="left", padx=5)

    def agregar_usuario():
        u = entry_u_name.get().strip()
        p = entry_u_pass.get().strip()
        r = combo_u_rol.get()

        if not u or not p:
            messagebox.showwarning("Atención", "Escribe usuario y contraseña.")
            return

        ok, msg = agregar_usuario_bd(u, p, r)
        if ok:
            messagebox.showinfo("Éxito", msg)
            entry_u_name.delete(0, tk.END)
            entry_u_pass.delete(0, tk.END)
            cargar_usuarios_tabla()
        else:
            messagebox.showerror("Error", msg)

    btn_add_u = tk.Button(f_f_user, text="REGISTRAR", command=agregar_usuario, font=("Segoe UI", 9, "bold"),
                           bg=COLOR_ACCENT, fg=COLOR_BG_DARK, bd=0, cursor="hand2")
    btn_add_u.pack(side="left", padx=15, ipady=4, ipadx=10)

    tabla_users = ttk.Treeview(f_u_main, columns=("id", "usr", "rol"), show="headings", height=8)
    tabla_users.heading("id", text="ID")
    tabla_users.heading("usr", text="Nombre de Usuario")
    tabla_users.heading("rol", text="Rol de Sistema")
    tabla_users.column("id", width=50, anchor="center")
    tabla_users.column("usr", width=250)
    tabla_users.column("rol", width=150, anchor="center")
    tabla_users.pack(fill="both", expand=True, padx=15, pady=10)

    def cargar_usuarios_tabla():
        for item in tabla_users.get_children():
            tabla_users.delete(item)
        for u in obtener_usuarios_bd():
            tabla_users.insert("", "end", values=u)

    def eliminar_usuario_sel():
        sel = tabla_users.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un usuario.")
            return
        vals = tabla_users.item(sel[0])["values"]
        u_id, u_nom = vals[0], vals[1]

        if u_nom == usuario:
            messagebox.showerror("Error", "No puedes eliminar tu propia cuenta en sesión activa.")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar la cuenta '{u_nom}'?"):
            eliminar_usuario_bd(u_id)
            cargar_usuarios_tabla()

    btn_del_u = tk.Button(f_u_main, text="🗑️ ELIMINAR USUARIO SELECCIONADO", command=eliminar_usuario_sel,
                          font=("Segoe UI", 9, "bold"), bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2")
    btn_del_u.pack(anchor="e", padx=15, pady=(0, 10), ipady=5, ipadx=15)

    # Carga Inicial de Datos
    cargar_datos_unidades()
    sincronizar_combos()
    cargar_usuarios_tabla()

    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.after(100, animar_entrada)
    ventana.mainloop()