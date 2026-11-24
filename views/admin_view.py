import os
import sys
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

# Asegurar que la ruta raíz esté en el path para importar views sin problemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from views.tutorial_view import open_tutorial
except ImportError:
    def open_tutorial(*args, **kwargs):
        return None

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
COLOR_SUCCESS_HOVER = "#249C91"


def _cancelar_after(widget, after_id):
    if widget is not None and after_id is not None:
        try:
            if widget.winfo_exists():
                widget.after_cancel(after_id)
        except Exception:
            pass


def _obtener_columnas_usuarios(cursor):
    cursor.execute("PRAGMA table_info(usuarios)")
    return {fila[1] for fila in cursor.fetchall()}


def _asegurar_esquema_grupos():
    """Garantiza que existan las tablas grupos y columnas esperadas según db_manager.py."""
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grupos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_grupo TEXT NOT NULL,
            docente_id INTEGER,
            FOREIGN KEY(docente_id) REFERENCES usuarios(id)
        )
    """)

    cols = _obtener_columnas_usuarios(cursor)
    if "grupo_id" not in cols:
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN grupo_id INTEGER NULL")
        except Exception:
            pass

    cursor.execute("SELECT COUNT(*) FROM grupos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM usuarios WHERE rol = 'docente' ORDER BY id ASC LIMIT 1")
        doc = cursor.fetchone()
        doc_id = doc[0] if doc else None
        for nombre_g in ["Grupo 7A", "Grupo 7B"]:
            cursor.execute("INSERT INTO grupos (nombre_grupo, docente_id) VALUES (?, ?)", (nombre_g, doc_id))

    conexion.commit()
    conexion.close()


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


def obtener_grupos_con_docente_bd():
    """Retorna lista de tuplas: (grupo_id, nombre_grupo, docente_id, nombre_docente)."""
    _asegurar_esquema_grupos()
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cols = _obtener_columnas_usuarios(cursor)
    expr_doc = (
        "COALESCE(NULLIF(d.nombre_completo, ''), d.nombre_usuario, 'Sin docente asignado')"
        if "nombre_completo" in cols
        else "COALESCE(d.nombre_usuario, 'Sin docente asignado')"
    )
    cursor.execute(f"""
        SELECT g.id, g.nombre_grupo, g.docente_id, {expr_doc}
        FROM grupos g
        LEFT JOIN usuarios d ON g.docente_id = d.id
        ORDER BY g.nombre_grupo ASC
    """)
    grupos = cursor.fetchall()
    conexion.close()
    return grupos


def crear_grupo_nuevo_bd(nombre_grupo):
    """Crea un grupo nuevo (sin docente aún) y devuelve su id."""
    _asegurar_esquema_grupos()
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM grupos WHERE LOWER(nombre_grupo) = LOWER(?)", (nombre_grupo.strip(),))
    existente = cursor.fetchone()
    if existente:
        grupo_id = existente[0]
    else:
        cursor.execute("INSERT INTO grupos (nombre_grupo, docente_id) VALUES (?, NULL)", (nombre_grupo.strip(),))
        grupo_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return grupo_id


def obtener_usuarios_bd():
    """Retorna: (id, nombre_completo, nombre_usuario, rol, nombre_grupo, nombre_docente, grupo_id, docente_id)."""
    _asegurar_esquema_grupos()
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cols = _obtener_columnas_usuarios(cursor)

    col_nombre = "COALESCE(NULLIF(u.nombre_completo, ''), u.nombre_usuario)" if "nombre_completo" in cols else "u.nombre_usuario"
    col_docente = (
        "COALESCE(NULLIF(d.nombre_completo, ''), d.nombre_usuario, 'Sin docente asignado')"
        if "nombre_completo" in cols
        else "COALESCE(d.nombre_usuario, 'Sin docente asignado')"
    )

    cursor.execute(f"""
        SELECT
            u.id,
            {col_nombre},
            u.nombre_usuario,
            u.rol,
            CASE
                WHEN u.rol = 'admin' THEN 'N/A'
                ELSE COALESCE(g.nombre_grupo, 'Sin grupo')
            END AS info_grupo,
            CASE
                WHEN u.rol = 'admin' THEN 'N/A'
                WHEN u.rol = 'docente' THEN COALESCE((
                    SELECT GROUP_CONCAT(gd.nombre_grupo, ', ')
                    FROM grupos gd
                    WHERE gd.docente_id = u.id
                ), 'Sin grupo asignado')
                ELSE {col_docente}
            END AS info_docente,
            u.grupo_id,
            g.docente_id
        FROM usuarios u
        LEFT JOIN grupos g ON u.grupo_id = g.id
        LEFT JOIN usuarios d ON g.docente_id = d.id
        ORDER BY u.id ASC
    """)
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def agregar_usuario_bd(nombre_completo, nombre_usuario, password, rol, grupo_id=None, crear_grupo_nombre=None):
    _asegurar_esquema_grupos()
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cols = _obtener_columnas_usuarios(cursor)
    col_pass = "password" if "password" in cols else "contrasena"

    grupo_final_id = grupo_id

    try:
        if rol == "docente" and crear_grupo_nombre:
            cursor.execute("SELECT id FROM grupos WHERE LOWER(nombre_grupo) = LOWER(?)", (crear_grupo_nombre.strip(),))
            g_existe = cursor.fetchone()
            if g_existe:
                grupo_final_id = g_existe[0]
            else:
                cursor.execute("INSERT INTO grupos (nombre_grupo, docente_id) VALUES (?, NULL)", (crear_grupo_nombre.strip(),))
                grupo_final_id = cursor.lastrowid

        if "nombre_completo" in cols:
            cursor.execute(
                f"INSERT INTO usuarios (nombre_completo, nombre_usuario, {col_pass}, rol, grupo_id) VALUES (?, ?, ?, ?, ?)",
                (nombre_completo, nombre_usuario, password, rol, grupo_final_id)
            )
        else:
            cursor.execute(
                f"INSERT INTO usuarios (nombre_usuario, {col_pass}, rol, grupo_id) VALUES (?, ?, ?, ?)",
                (nombre_usuario, password, rol, grupo_final_id)
            )

        nuevo_usuario_id = cursor.lastrowid

        if rol == "docente" and grupo_final_id is not None:
            cursor.execute("UPDATE grupos SET docente_id = ? WHERE id = ?", (nuevo_usuario_id, grupo_final_id))
            cursor.execute("UPDATE usuarios SET grupo_id = ? WHERE id = ?", (grupo_final_id, nuevo_usuario_id))

        conexion.commit()
        conexion.close()
        return True, "Usuario registrado exitosamente."
    except sqlite3.IntegrityError:
        conexion.close()
        return False, "El nombre de usuario ya existe."


def actualizar_asignacion_usuario_bd(user_id, rol, grupo_id=None, crear_grupo_nombre=None):
    _asegurar_esquema_grupos()
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    grupo_final_id = grupo_id
    if rol == "docente" and crear_grupo_nombre:
        cursor.execute("SELECT id FROM grupos WHERE LOWER(nombre_grupo) = LOWER(?)", (crear_grupo_nombre.strip(),))
        g_existe = cursor.fetchone()
        if g_existe:
            grupo_final_id = g_existe[0]
        else:
            cursor.execute("INSERT INTO grupos (nombre_grupo, docente_id) VALUES (?, NULL)", (crear_grupo_nombre.strip(),))
            grupo_final_id = cursor.lastrowid

    cursor.execute("UPDATE usuarios SET grupo_id = ? WHERE id = ?", (grupo_final_id, user_id))
    if rol == "docente" and grupo_final_id is not None:
        cursor.execute("UPDATE grupos SET docente_id = ? WHERE id = ?", (user_id, grupo_final_id))

    conexion.commit()
    conexion.close()


def eliminar_usuario_bd(user_id):
    _asegurar_esquema_grupos()
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("UPDATE grupos SET docente_id = NULL WHERE docente_id = ?", (user_id,))
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conexion.commit()
    conexion.close()


# ==========================================
# MODAL PERSONALIZADO DE CIERRE DE SESIÓN
# ==========================================
def confirmar_cierre_sesion_hud(parent):
    resultado = {"confirmado": False}

    dialog = ctk.CTkToplevel(parent)
    dialog.title("")
    dialog.geometry("440x220")
    dialog.configure(fg_color=COLOR_BG_DARK)
    dialog.overrideredirect(True)
    dialog.attributes("-alpha", 0.0)
    dialog.grab_set()

    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 220
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 110
    dialog.geometry(f"+{x}+{y}")

    card_modal = ctk.CTkFrame(dialog, fg_color=COLOR_CARD, border_color=COLOR_ACCENT, border_width=1, corner_radius=12)
    card_modal.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(card_modal, text="⚠️ CONFIRMAR CIERRE DE SESIÓN", font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(pady=(22, 8))

    ctk.CTkLabel(card_modal, text="¿Estás seguro de que deseas cerrar sesión\ny regresar al panel principal de acceso?",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT, justify="center").pack(pady=(0, 20))

    f_btns = ctk.CTkFrame(card_modal, fg_color="transparent")
    f_btns.pack(pady=(0, 15))

    id_anim_dialog = None

    def animar_aparicion(alpha=0.0):
        nonlocal id_anim_dialog
        if alpha < 1.0 and dialog.winfo_exists():
            alpha = min(1.0, alpha + 0.1)
            dialog.attributes("-alpha", alpha)
            id_anim_dialog = dialog.after(15, lambda: animar_aparicion(alpha))

    def cerrar_dialog(confirmado):
        _cancelar_after(dialog, id_anim_dialog)
        resultado["confirmado"] = confirmado
        if dialog.winfo_exists():
            try:
                dialog.grab_release()
            except Exception:
                pass
            dialog.destroy()

    btn_cancelar = ctk.CTkButton(f_btns, text="Cancelar", command=lambda: cerrar_dialog(False), width=130, height=38,
                                 fg_color=COLOR_ENTRY_BG, hover_color=COLOR_BORDER, text_color=COLOR_TEXT_LIGHT,
                                 font=("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2")
    btn_cancelar.pack(side="left", padx=10)

    btn_aceptar = ctk.CTkButton(f_btns, text="Sí, Cerrar Sesión", command=lambda: cerrar_dialog(True), width=140, height=38,
                                fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT,
                                font=("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2")
    btn_aceptar.pack(side="left", padx=10)

    animar_aparicion()
    parent.wait_window(dialog)
    return resultado["confirmado"]


# ==========================================
# INTERFAZ GRÁFICA DEL ADMINISTRADOR
# ==========================================
def abrir_panel_admin(usuario):
    ventana = ctk.CTk()
    ventana.title(f"LAB VISUAL FORENSE - Panel de Administración ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(fg_color=COLOR_BG_DARK)
    ventana.attributes("-alpha", 0.0)

    sesion_cerrada = {"estado": False}
    id_animacion = None
    id_tutorial = None

    def animar_entrada(alpha=0.0):
        nonlocal id_animacion
        if alpha < 1.0 and ventana.winfo_exists():
            alpha = min(1.0, alpha + 0.05)
            ventana.attributes("-alpha", alpha)
            id_animacion = ventana.after(20, lambda: animar_entrada(alpha))

    def salir_limpio():
        _cancelar_after(ventana, id_animacion)
        _cancelar_after(ventana, id_tutorial)
        if ventana.winfo_exists():
            ventana.quit()
            ventana.destroy()

    def cerrar_sesion():
        if confirmar_cierre_sesion_hud(ventana):
            sesion_cerrada["estado"] = True
            salir_limpio()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=35, font=("Segoe UI", 10))
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("Treeview.Heading", background=COLOR_CARD, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 10, "bold"), borderwidth=0)

    container_main = ctk.CTkFrame(ventana, fg_color=COLOR_BG_DARK)
    container_main.pack(fill="both", expand=True, padx=20, pady=20)

    # Header Superior
    header = ctk.CTkFrame(container_main, fg_color=COLOR_CARD, height=60, corner_radius=10)
    header.pack(fill="x", pady=(0, 15))
    header.pack_propagate(False)

    ctk.CTkLabel(header, text="⚙️ MÓDULO ADMINISTRADOR DE CONTENIDO Y SISTEMA", font=("Segoe UI", 16, "bold"),
                 text_color=COLOR_ACCENT).pack(side="left", padx=20)

    btn_cerrar = ctk.CTkButton(header, text="CERRAR SESIÓN", command=cerrar_sesion, font=("Segoe UI", 12, "bold"),
                               fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT, corner_radius=8, cursor="hand2")
    btn_cerrar.pack(side="right", padx=15, pady=10)

    btn_ayuda = ctk.CTkButton(header, text="❓ AYUDA / TUTORIAL",
                              command=lambda: open_tutorial(ventana, role="admin", auto=False),
                              font=("Segoe UI", 12, "bold"),
                              fg_color=COLOR_ENTRY_BG, hover_color=COLOR_BORDER,
                              text_color=COLOR_ACCENT, corner_radius=8, cursor="hand2")
    btn_ayuda.pack(side="right", padx=(0, 8), pady=10)

    # Pestañas de Navegación (CTkTabview)
    notebook = ctk.CTkTabview(container_main, fg_color=COLOR_CARD, segmented_button_selected_color=COLOR_BORDER,
                            segmented_button_selected_hover_color=COLOR_ENTRY_BG, segmented_button_unselected_color=COLOR_ENTRY_BG,
                            text_color=COLOR_TEXT_MUTED, corner_radius=10)
    notebook.pack(fill="both", expand=True)

    tab_teoria_name = "📚 Gestión de Teoría y Subtemas"
    tab_preguntas_name = "📝 Banco de Preguntas"
    tab_users_name = "👥 Usuarios del Sistema"

    notebook.add(tab_teoria_name)
    notebook.add(tab_preguntas_name)
    notebook.add(tab_users_name)

    # =============================================================
    # PESTAÑA 1: GESTIÓN DE CONTENIDO TEÓRICO Y SUBTEMAS
    # =============================================================
    tab_teoria = notebook.tab(tab_teoria_name)

    f_sel_u = ctk.CTkFrame(tab_teoria, fg_color="transparent")
    f_sel_u.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(f_sel_u, text="Seleccionar Unidad:", font=("Segoe UI", 13, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 10))

    combo_unidades = ctk.CTkComboBox(f_sel_u, state="readonly", font=("Segoe UI", 13), width=400,
                                     fg_color=COLOR_ENTRY_BG, border_color=COLOR_BORDER, dropdown_fg_color=COLOR_CARD)
    combo_unidades.pack(side="left", padx=5)

    f_tit_u = ctk.CTkFrame(tab_teoria, fg_color="transparent")
    f_tit_u.pack(fill="x", padx=15, pady=5)

    ctk.CTkLabel(f_tit_u, text="Título de la Unidad:", font=("Segoe UI", 13, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 10))

    entry_titulo_u = ctk.CTkEntry(f_tit_u, font=("Segoe UI", 13), fg_color=COLOR_ENTRY_BG,
                                  text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER, corner_radius=5)
    entry_titulo_u.pack(side="left", fill="x", expand=True)

    f_txt_u = ctk.CTkFrame(tab_teoria, fg_color="transparent")
    f_txt_u.pack(fill="both", expand=True, padx=15, pady=10)

    ctk.CTkLabel(f_txt_u, text="Contenido Teórico Completo (Escribe o extiende los subtemas 1.1, 1.2, etc.):",
                 font=("Segoe UI", 13, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", pady=(0, 5))

    txt_teoria_editor = ctk.CTkTextbox(f_txt_u, wrap="word", font=("Consolas", 13), fg_color=COLOR_ENTRY_BG,
                                       text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER, border_width=1, corner_radius=8)
    txt_teoria_editor.pack(fill="both", expand=True)

    menu_contextual = tk.Menu(txt_teoria_editor, tearoff=0, bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, bd=0,
                              activebackground=COLOR_ACCENT, activeforeground=COLOR_BG_DARK)
    menu_contextual.add_command(label="✂️ Cortar", command=lambda: txt_teoria_editor.event_generate("<<Cut>>"))
    menu_contextual.add_command(label="📋 Copiar", command=lambda: txt_teoria_editor.event_generate("<<Copy>>"))
    menu_contextual.add_command(label="📝 Pegar", command=lambda: txt_teoria_editor.event_generate("<<Paste>>"))
    menu_contextual.add_separator()
    menu_contextual.add_command(label="Seleccionar Todo", command=lambda: txt_teoria_editor.tag_add("sel", "1.0", "end"))

    txt_teoria_editor.bind("<Button-3>", lambda event: menu_contextual.tk_popup(event.x_root, event.y_root))

    unidades_datos = []

    def cargar_datos_unidades():
        nonlocal unidades_datos
        unidades_datos = obtener_unidades_bd()
        valores_combo = [f"Unidad {u[1]}: {u[2]}" for u in unidades_datos]
        combo_unidades.configure(values=valores_combo)
        if valores_combo:
            combo_unidades.set(valores_combo[0])
            al_seleccionar_unidad_combo(None)

    def al_seleccionar_unidad_combo(event):
        seleccion = combo_unidades.get()
        valores = combo_unidades.cget("values")
        if seleccion in valores:
            idx = valores.index(seleccion)
            u = unidades_datos[idx]
            entry_titulo_u.delete(0, tk.END)
            entry_titulo_u.insert(0, u[2])

            txt_teoria_editor.delete("1.0", tk.END)
            txt_teoria_editor.insert("1.0", u[3] if u[3] else "")

    combo_unidades.configure(command=al_seleccionar_unidad_combo)

    def guardar_teoria_unidad():
        seleccion = combo_unidades.get()
        valores = combo_unidades.cget("values")
        if not seleccion or seleccion not in valores:
            messagebox.showwarning("Atención", "Selecciona una unidad primero.")
            return

        idx = valores.index(seleccion)
        tema_id = unidades_datos[idx][0]
        nuevo_titulo = entry_titulo_u.get().strip()
        nuevo_contenido = txt_teoria_editor.get("1.0", tk.END).strip()

        if not nuevo_titulo:
            messagebox.showwarning("Atención", "El título de la unidad no puede estar vacío.")
            return

        actualizar_contenido_teorico(tema_id, nuevo_titulo, nuevo_contenido)
        messagebox.showinfo("Éxito", "¡Contenido teórico guardado exitosamente!")
        cargar_datos_unidades()

    btn_guardar_teoria = ctk.CTkButton(tab_teoria, text="💾 GUARDAR / ACTUALIZAR TEORÍA Y SUBTEMAS",
                                       command=guardar_teoria_unidad, font=("Segoe UI", 13, "bold"),
                                       fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, text_color=COLOR_BG_DARK,
                                       corner_radius=8, cursor="hand2", height=40)
    btn_guardar_teoria.pack(pady=15)

    # =============================================================
    # PESTAÑA 2: BANCO DE PREGUNTAS (SELECCIÓN POR UNIDAD)
    # =============================================================
    tab_preg = notebook.tab(tab_preguntas_name)

    f_top_q = ctk.CTkFrame(tab_preg, fg_color="transparent")
    f_top_q.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(f_top_q, text="Seleccionar Unidad Destino:", font=("Segoe UI", 13, "bold"),
                 text_color=COLOR_ACCENT).pack(side="left", padx=(0, 10))

    combo_q_unidades = ctk.CTkComboBox(f_top_q, state="readonly", font=("Segoe UI", 13), width=400,
                                       fg_color=COLOR_ENTRY_BG, border_color=COLOR_BORDER)
    combo_q_unidades.pack(side="left", padx=5)

    f_form_q = ctk.CTkFrame(tab_preg, fg_color=COLOR_ENTRY_BG, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
    f_form_q.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(f_form_q, text="Pregunta:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", padx=15, pady=10)
    entry_q_texto = ctk.CTkEntry(f_form_q, font=("Segoe UI", 13), fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_q_texto.grid(row=0, column=1, columnspan=3, sticky="ew", padx=15, pady=10)

    ctk.CTkLabel(f_form_q, text="Opción A:", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=1, column=0, sticky="w", padx=15, pady=5)
    entry_op_a = ctk.CTkEntry(f_form_q, font=("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_a.grid(row=1, column=1, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Opción B:", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=1, column=2, sticky="w", padx=15, pady=5)
    entry_op_b = ctk.CTkEntry(f_form_q, font=("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_b.grid(row=1, column=3, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Opción C:", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=2, column=0, sticky="w", padx=15, pady=5)
    entry_op_c = ctk.CTkEntry(f_form_q, font=("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_c.grid(row=2, column=1, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Opción D:", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=2, column=2, sticky="w", padx=15, pady=5)
    entry_op_d = ctk.CTkEntry(f_form_q, font=("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_d.grid(row=2, column=3, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Respuesta Correcta:", font=("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).grid(row=3, column=0, sticky="w", padx=15, pady=10)
    combo_correcta = ctk.CTkComboBox(f_form_q, values=["A", "B", "C", "D"], state="readonly", width=100, fg_color=COLOR_CARD, border_width=0)
    combo_correcta.set("A")
    combo_correcta.grid(row=3, column=1, sticky="w", padx=15, pady=10)

    f_form_q.columnconfigure(1, weight=1)
    f_form_q.columnconfigure(3, weight=1)

    def guardar_pregunta():
        seleccion = combo_q_unidades.get()
        valores = combo_q_unidades.cget("values")
        if not seleccion or seleccion not in valores:
            messagebox.showwarning("Atención", "Selecciona la unidad destino.")
            return

        idx = valores.index(seleccion)
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

        entry_q_texto.delete(0, tk.END)
        entry_op_a.delete(0, tk.END)
        entry_op_b.delete(0, tk.END)
        entry_op_c.delete(0, tk.END)
        entry_op_d.delete(0, tk.END)
        cargar_preguntas_unidad_tabla()

    btn_add_q = ctk.CTkButton(f_form_q, text="➕ AGREGAR PREGUNTA", command=guardar_pregunta,
                              font=("Segoe UI", 12, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                              text_color=COLOR_BG_DARK, cursor="hand2")
    btn_add_q.grid(row=3, column=3, sticky="e", padx=15, pady=10)

    f_tbl_q = ctk.CTkFrame(tab_preg, fg_color="transparent")
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

    scroll_q_tbl = ctk.CTkScrollbar(f_tbl_q, orientation="vertical", command=tabla_q.yview)
    tabla_q.configure(yscrollcommand=scroll_q_tbl.set)
    scroll_q_tbl.pack(side="right", fill="y")

    def cargar_preguntas_unidad_tabla(*args):
        for item in tabla_q.get_children():
            tabla_q.delete(item)

        seleccion = combo_q_unidades.get()
        valores = combo_q_unidades.cget("values")
        if seleccion in valores:
            idx = valores.index(seleccion)
            tema_id = unidades_datos[idx][0]
            pregs = obtener_preguntas_por_tema(tema_id)
            for p in pregs:
                tabla_q.insert("", "end", values=p)

    combo_q_unidades.configure(command=cargar_preguntas_unidad_tabla)

    def eliminar_pregunta_seleccionada():
        sel = tabla_q.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una pregunta para eliminar.")
            return
        q_id = tabla_q.item(sel[0])["values"][0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar la pregunta ID {q_id}?"):
            eliminar_pregunta_bd(q_id)
            cargar_preguntas_unidad_tabla()

    btn_del_q = ctk.CTkButton(tab_preg, text="🗑️ ELIMINAR PREGUNTA", command=eliminar_pregunta_seleccionada,
                              font=("Segoe UI", 12, "bold"), fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER,
                              text_color=COLOR_TEXT_LIGHT, cursor="hand2")
    btn_del_q.pack(anchor="e", padx=15, pady=(0, 10))

    def sincronizar_combos():
        if unidades_datos:
            valores_combo = [f"Unidad {u[1]}: {u[2]}" for u in unidades_datos]
            combo_q_unidades.configure(values=valores_combo)
            combo_q_unidades.set(valores_combo[0])
            cargar_preguntas_unidad_tabla()

    # =============================================================
    # PESTAÑA 3: GESTIÓN DE USUARIOS DEL SISTEMA
    # =============================================================
    tab_usr = notebook.tab(tab_users_name)

    asignacion_pendiente = {
        "grupo_id": None,
        "grupo_nombre": "Sin grupo",
        "docente_nombre": "Sin docente asignado",
        "crear_grupo_nombre": None,
    }
    lbl_resumen_asig = None

    def _resetear_asignacion_pendiente(rol_actual):
        asignacion_pendiente["grupo_id"] = None
        asignacion_pendiente["crear_grupo_nombre"] = None
        if rol_actual == "admin":
            asignacion_pendiente["grupo_nombre"] = "N/A"
            asignacion_pendiente["docente_nombre"] = "N/A"
        else:
            asignacion_pendiente["grupo_nombre"] = "Sin grupo"
            asignacion_pendiente["docente_nombre"] = "Sin docente asignado"
        if lbl_resumen_asig is not None and lbl_resumen_asig.winfo_exists():
            lbl_resumen_asig.configure(
                text=f"Grupo: {asignacion_pendiente['grupo_nombre']} | Docente: {asignacion_pendiente['docente_nombre']}"
            )

    def abrir_modal_asignacion(modo="nuevo", fila_usuario=None):
        rol_objetivo = combo_u_rol.get() if modo == "nuevo" else fila_usuario[3]

        if rol_objetivo == "admin":
            messagebox.showinfo("Administración", "Los usuarios con rol 'admin' no requieren asignación de grupo ni docente.")
            return

        grupos_db = obtener_grupos_con_docente_bd()
        mapa_grupos = {}
        opciones_grupo = []
        for gid, gnom, did, dnom in grupos_db:
            etiqueta = f"{gnom}  —  Docente: {dnom}"
            mapa_grupos[etiqueta] = (gid, gnom, did, dnom)
            opciones_grupo.append(etiqueta)

        modal_asig = ctk.CTkToplevel(ventana)
        modal_asig.title("Asignación Académica")
        modal_asig.geometry("500x310")
        modal_asig.configure(fg_color=COLOR_BG_DARK)
        modal_asig.grab_set()

        card_asig = ctk.CTkFrame(modal_asig, fg_color=COLOR_CARD, border_color=COLOR_ACCENT, border_width=1, corner_radius=12)
        card_asig.pack(fill="both", expand=True, padx=14, pady=14)

        if rol_objetivo == "alumno":
            ctk.CTkLabel(card_asig, text="🎓 ALUMNO: ASIGNAR GRUPO Y SU DOCENTE", font=("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(16, 8))
            ctk.CTkLabel(card_asig, text="Selecciona el grupo (se asignará junto con su docente):", font=("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=24, pady=(4, 4))

            combo_g_alum = ctk.CTkComboBox(
                card_asig,
                values=opciones_grupo if opciones_grupo else ["Sin grupos disponibles"],
                state="readonly",
                width=430,
                fg_color=COLOR_ENTRY_BG,
                border_color=COLOR_BORDER,
                dropdown_fg_color=COLOR_CARD
            )
            combo_g_alum.pack(padx=24, pady=6)

            lbl_doc_vinculado = ctk.CTkLabel(
                card_asig,
                text="Docente del grupo: —",
                font=("Segoe UI", 12, "bold"),
                text_color=COLOR_SUCCESS
            )
            lbl_doc_vinculado.pack(anchor="w", padx=24, pady=(10, 14))

            def actualizar_info_docente(*args):
                sel = combo_g_alum.get()
                if sel in mapa_grupos:
                    _, _, _, dnom = mapa_grupos[sel]
                    lbl_doc_vinculado.configure(text=f"Docente asignado automáticamente: {dnom}")
                else:
                    lbl_doc_vinculado.configure(text="Docente asignado automáticamente: Sin docente asignado")

            combo_g_alum.configure(command=actualizar_info_docente)

            grupo_id_actual = asignacion_pendiente["grupo_id"] if modo == "nuevo" else fila_usuario[6]
            seleccion_inicial = None
            for etq, (gid, _, _, _) in mapa_grupos.items():
                if gid == grupo_id_actual:
                    seleccion_inicial = etq
                    break
            if seleccion_inicial:
                combo_g_alum.set(seleccion_inicial)
            elif opciones_grupo:
                combo_g_alum.set(opciones_grupo[0])
            actualizar_info_docente()

            def guardar_alumno_asig():
                sel = combo_g_alum.get()
                if sel not in mapa_grupos:
                    messagebox.showwarning("Atención", "Selecciona un grupo válido.")
                    return
                gid, gnom, _, dnom = mapa_grupos[sel]
                if modo == "nuevo":
                    asignacion_pendiente["grupo_id"] = gid
                    asignacion_pendiente["grupo_nombre"] = gnom
                    asignacion_pendiente["docente_nombre"] = dnom
                    asignacion_pendiente["crear_grupo_nombre"] = None
                    if lbl_resumen_asig is not None and lbl_resumen_asig.winfo_exists():
                        lbl_resumen_asig.configure(text=f"Grupo: {gnom} | Docente: {dnom}")
                else:
                    actualizar_asignacion_usuario_bd(fila_usuario[0], "alumno", grupo_id=gid)
                    cargar_usuarios_tabla()
                    messagebox.showinfo("Éxito", f"Alumno '{fila_usuario[1]}' asignado al grupo '{gnom}' ({dnom}).")

                if modal_asig.winfo_exists():
                    try:
                        modal_asig.grab_release()
                    except Exception:
                        pass
                    modal_asig.destroy()

            cmd_guardar = guardar_alumno_asig

        else:  # rol_objetivo == "docente"
            ctk.CTkLabel(card_asig, text="👨‍🏫 DOCENTE: ASIGNAR O CREAR GRUPO", font=("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT).pack(pady=(16, 8))

            modo_grupo_var = tk.StringVar(value="existente")

            f_radios = ctk.CTkFrame(card_asig, fg_color="transparent")
            f_radios.pack(fill="x", padx=24, pady=(4, 8))

            combo_g_doc = ctk.CTkComboBox(
                card_asig,
                values=opciones_grupo if opciones_grupo else ["Sin grupos existentes"],
                state="readonly",
                width=430,
                fg_color=COLOR_ENTRY_BG,
                border_color=COLOR_BORDER,
                dropdown_fg_color=COLOR_CARD
            )
            entry_nuevo_grupo = ctk.CTkEntry(
                card_asig,
                placeholder_text="Nombre del nuevo grupo (Ej. Grupo 8A)",
                width=430,
                fg_color=COLOR_ENTRY_BG,
                border_color=COLOR_BORDER
            )

            def alternar_modo_grupo():
                if modo_grupo_var.get() == "existente":
                    combo_g_doc.configure(state="readonly")
                    entry_nuevo_grupo.configure(state="disabled")
                else:
                    combo_g_doc.configure(state="disabled")
                    entry_nuevo_grupo.configure(state="normal")
                    entry_nuevo_grupo.focus_set()

            ctk.CTkRadioButton(
                f_radios, text="Asignar grupo existente", variable=modo_grupo_var, value="existente",
                command=alternar_modo_grupo, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT
            ).pack(side="left", padx=(0, 20))

            ctk.CTkRadioButton(
                f_radios, text="Crear nuevo grupo", variable=modo_grupo_var, value="nuevo",
                command=alternar_modo_grupo, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT
            ).pack(side="left")

            combo_g_doc.pack(padx=24, pady=(4, 8))
            entry_nuevo_grupo.pack(padx=24, pady=(2, 12))

            if opciones_grupo:
                combo_g_doc.set(opciones_grupo[0])

            if modo == "nuevo" and asignacion_pendiente["crear_grupo_nombre"]:
                modo_grupo_var.set("nuevo")
                entry_nuevo_grupo.insert(0, asignacion_pendiente["crear_grupo_nombre"])

            alternar_modo_grupo()

            def guardar_docente_asig():
                if modo_grupo_var.get() == "existente":
                    sel = combo_g_doc.get()
                    if sel not in mapa_grupos:
                        messagebox.showwarning("Atención", "Selecciona un grupo existente o elige crear uno nuevo.")
                        return
                    gid, gnom, _, _ = mapa_grupos[sel]
                    if modo == "nuevo":
                        asignacion_pendiente["grupo_id"] = gid
                        asignacion_pendiente["grupo_nombre"] = gnom
                        asignacion_pendiente["docente_nombre"] = "Este docente"
                        asignacion_pendiente["crear_grupo_nombre"] = None
                        if lbl_resumen_asig is not None and lbl_resumen_asig.winfo_exists():
                            lbl_resumen_asig.configure(text=f"Grupo asignado: {gnom} | Docente: Este docente")
                    else:
                        actualizar_asignacion_usuario_bd(fila_usuario[0], "docente", grupo_id=gid)
                        cargar_usuarios_tabla()
                        messagebox.showinfo("Éxito", f"Docente '{fila_usuario[1]}' asignado al grupo '{gnom}'.")
                else:
                    nuevo_nom = entry_nuevo_grupo.get().strip()
                    if not nuevo_nom:
                        messagebox.showwarning("Atención", "Escribe el nombre del nuevo grupo a crear.")
                        return
                    if modo == "nuevo":
                        asignacion_pendiente["grupo_id"] = None
                        asignacion_pendiente["grupo_nombre"] = f"{nuevo_nom} (Nuevo)"
                        asignacion_pendiente["docente_nombre"] = "Este docente"
                        asignacion_pendiente["crear_grupo_nombre"] = nuevo_nom
                        if lbl_resumen_asig is not None and lbl_resumen_asig.winfo_exists():
                            lbl_resumen_asig.configure(text=f"Nuevo grupo: {nuevo_nom} | Docente: Este docente")
                    else:
                        actualizar_asignacion_usuario_bd(fila_usuario[0], "docente", crear_grupo_nombre=nuevo_nom)
                        cargar_usuarios_tabla()
                        messagebox.showinfo("Éxito", f"Grupo '{nuevo_nom}' creado y asignado a '{fila_usuario[1]}'.")

                if modal_asig.winfo_exists():
                    try:
                        modal_asig.grab_release()
                    except Exception:
                        pass
                    modal_asig.destroy()

            cmd_guardar = guardar_docente_asig

        f_btns_a = ctk.CTkFrame(card_asig, fg_color="transparent")
        f_btns_a.pack(pady=(4, 8))

        ctk.CTkButton(f_btns_a, text="Cancelar", width=120, fg_color=COLOR_ENTRY_BG, hover_color=COLOR_BORDER,
                      text_color=COLOR_TEXT_LIGHT, command=modal_asig.destroy).pack(side="left", padx=8)
        ctk.CTkButton(f_btns_a, text="Confirmar", width=130, fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER,
                      text_color=COLOR_BG_DARK, font=("Segoe UI", 12, "bold"), command=cmd_guardar).pack(side="left", padx=8)

    # Formulario de creación de usuario
    f_f_user = ctk.CTkFrame(tab_usr, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    f_f_user.pack(fill="x", padx=15, pady=10)

    fila1_u = ctk.CTkFrame(f_f_user, fg_color="transparent")
    fila1_u.pack(fill="x", padx=12, pady=(10, 5))

    ctk.CTkLabel(fila1_u, text="Nombre Completo:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 6))
    entry_u_full = ctk.CTkEntry(fila1_u, width=180, placeholder_text="Ej. Juan Pérez", font=("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_u_full.pack(side="left", padx=(0, 12))

    ctk.CTkLabel(fila1_u, text="Usuario:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 6))
    entry_u_name = ctk.CTkEntry(fila1_u, width=140, placeholder_text="Ej. jperez", font=("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_u_name.pack(side="left", padx=(0, 12))

    ctk.CTkLabel(fila1_u, text="Contraseña:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 6))
    entry_u_pass = ctk.CTkEntry(fila1_u, width=130, font=("Segoe UI", 12), show="*", fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_u_pass.pack(side="left", padx=(0, 12))

    ctk.CTkLabel(fila1_u, text="Rol:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 6))
    combo_u_rol = ctk.CTkComboBox(fila1_u, values=["alumno", "docente", "admin"], state="readonly", width=110, fg_color=COLOR_CARD, border_width=0)
    combo_u_rol.set("alumno")
    combo_u_rol.pack(side="left")

    fila2_u = ctk.CTkFrame(f_f_user, fg_color="transparent")
    fila2_u.pack(fill="x", padx=12, pady=(4, 10))

    btn_asignar_rol = ctk.CTkButton(
        fila2_u,
        text="🎓 ASIGNAR GRUPO / DOCENTE",
        command=lambda: abrir_modal_asignacion(modo="nuevo"),
        font=("Segoe UI", 12, "bold"),
        fg_color=COLOR_CARD,
        hover_color=COLOR_BORDER,
        text_color=COLOR_ACCENT,
        border_color=COLOR_ACCENT,
        border_width=1,
        corner_radius=8,
        cursor="hand2"
    )
    btn_asignar_rol.pack(side="left", padx=(0, 12))

    lbl_resumen_asig = ctk.CTkLabel(
        fila2_u,
        text="Grupo: Sin grupo | Docente: Sin docente asignado",
        font=("Segoe UI", 12),
        text_color=COLOR_TEXT_MUTED
    )
    lbl_resumen_asig.pack(side="left")

    def al_cambiar_rol_nuevo(*args):
        rol_sel = combo_u_rol.get()
        _resetear_asignacion_pendiente(rol_sel)
        if rol_sel == "admin":
            btn_asignar_rol.configure(state="disabled")
        elif rol_sel == "docente":
            btn_asignar_rol.configure(state="normal", text="👨‍🏫 GRUPO / CREAR GRUPO")
        else:
            btn_asignar_rol.configure(state="normal", text="🎓 GRUPO Y SU DOCENTE")

    combo_u_rol.configure(command=al_cambiar_rol_nuevo)

    def agregar_usuario():
        u = entry_u_name.get().strip()
        nom_comp = entry_u_full.get().strip() or u
        p = entry_u_pass.get().strip()
        r = combo_u_rol.get()

        if not u or not p:
            messagebox.showwarning("Atención", "Escribe usuario y contraseña.")
            return

        if r == "alumno" and asignacion_pendiente["grupo_id"] is None:
            messagebox.showwarning("Atención", "Selecciona el grupo (y su docente) para el alumno antes de registrar.")
            return

        if r == "docente" and asignacion_pendiente["grupo_id"] is None and not asignacion_pendiente["crear_grupo_nombre"]:
            messagebox.showwarning("Atención", "Selecciona un grupo o indica crear uno nuevo para el docente antes de registrar.")
            return

        ok, msg = agregar_usuario_bd(
            nom_comp,
            u,
            p,
            r,
            grupo_id=asignacion_pendiente["grupo_id"],
            crear_grupo_nombre=asignacion_pendiente["crear_grupo_nombre"]
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            entry_u_full.delete(0, tk.END)
            entry_u_name.delete(0, tk.END)
            entry_u_pass.delete(0, tk.END)
            _resetear_asignacion_pendiente(r)
            cargar_usuarios_tabla()
        else:
            messagebox.showerror("Error", msg)

    btn_add_u = ctk.CTkButton(fila2_u, text="➕ CREAR USUARIO", command=agregar_usuario, font=("Segoe UI", 12, "bold"),
                              fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, corner_radius=8, cursor="hand2")
    btn_add_u.pack(side="right")

    f_tbl_u = ctk.CTkFrame(tab_usr, fg_color="transparent")
    f_tbl_u.pack(fill="both", expand=True, padx=15, pady=10)

    tabla_users = ttk.Treeview(f_tbl_u, columns=("id", "nombre", "usr", "rol", "grupo", "doc"), show="headings", height=8)
    tabla_users.heading("id", text="ID")
    tabla_users.heading("nombre", text="Nombre Completo")
    tabla_users.heading("usr", text="Usuario")
    tabla_users.heading("rol", text="Rol")
    tabla_users.heading("grupo", text="Grupo")
    tabla_users.heading("doc", text="Docente Asignado / Grupos")

    tabla_users.column("id", width=45, anchor="center")
    tabla_users.column("nombre", width=200)
    tabla_users.column("usr", width=130)
    tabla_users.column("rol", width=95, anchor="center")
    tabla_users.column("grupo", width=130, anchor="center")
    tabla_users.column("doc", width=220, anchor="center")
    tabla_users.pack(side="left", fill="both", expand=True)

    scroll_u_tbl = ctk.CTkScrollbar(f_tbl_u, orientation="vertical", command=tabla_users.yview)
    tabla_users.configure(yscrollcommand=scroll_u_tbl.set)
    scroll_u_tbl.pack(side="right", fill="y")

    usuarios_cache = {}

    def cargar_usuarios_tabla():
        usuarios_cache.clear()
        for item in tabla_users.get_children():
            tabla_users.delete(item)
        for u in obtener_usuarios_bd():
            usuarios_cache[str(u[0])] = u
            tabla_users.insert("", "end", values=(u[0], u[1], u[2], u[3], u[4], u[5]))

    def reasignar_usuario_sel():
        sel = tabla_users.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un usuario en la tabla.")
            return
        vals = tabla_users.item(sel[0])["values"]
        fila = usuarios_cache.get(str(vals[0]))
        if fila:
            abrir_modal_asignacion(modo="existente", fila_usuario=fila)

    def eliminar_usuario_sel():
        sel = tabla_users.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un usuario.")
            return
        vals = tabla_users.item(sel[0])["values"]
        u_id, u_nom = vals[0], vals[2]

        if u_nom == usuario:
            messagebox.showerror("Error", "No puedes eliminar tu propia cuenta en sesión activa.")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar la cuenta '{u_nom}'?"):
            eliminar_usuario_bd(u_id)
            cargar_usuarios_tabla()

    f_btns_usr = ctk.CTkFrame(tab_usr, fg_color="transparent")
    f_btns_usr.pack(fill="x", padx=15, pady=(0, 10))

    btn_reasig = ctk.CTkButton(
        f_btns_usr, text="🎓 CAMBIAR ASIGNACIÓN DE SELECCIONADO",
        command=reasignar_usuario_sel,
        font=("Segoe UI", 12, "bold"), fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER,
        text_color=COLOR_BG_DARK, cursor="hand2"
    )
    btn_reasig.pack(side="left")

    btn_del_u = ctk.CTkButton(
        f_btns_usr, text="🗑️ ELIMINAR USUARIO", command=eliminar_usuario_sel,
        font=("Segoe UI", 12, "bold"), fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER,
        text_color=COLOR_TEXT_LIGHT, cursor="hand2"
    )
    btn_del_u.pack(side="right")

    # Carga Inicial de Datos
    cargar_datos_unidades()
    sincronizar_combos()
    cargar_usuarios_tabla()
    al_cambiar_rol_nuevo()

    def disparar_tutorial():
        if ventana.winfo_exists():
            open_tutorial(ventana, role="admin", auto=True)

    ventana.bind("<Escape>", lambda e: salir_limpio())
    id_animacion = ventana.after(100, animar_entrada)
    id_tutorial = ventana.after(350, disparar_tutorial)

    try:
        ventana.mainloop()
    finally:
        _cancelar_after(ventana, id_animacion)
        _cancelar_after(ventana, id_tutorial)

    return sesion_cerrada["estado"]