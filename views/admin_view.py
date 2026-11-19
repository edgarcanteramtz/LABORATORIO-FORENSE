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

# ==========================================
# CONSULTAS Y OPERACIONES EN BASE DE DATOS (Intactas)
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
# MODAL PERSONALIZADO DE CIERRE DE SESIÓN
# ==========================================
def confirmar_cierre_sesion_hud(parent):
    resultado = {"confirmado": False}
    
    dialog = ctk.CTkToplevel(parent)
    dialog.title("")
    dialog.geometry("440x220")
    dialog.configure(fg_color=COLOR_BG_DARK)
    dialog.overrideredirect(True)  # Sin barra de ventanas de Windows antiestética
    dialog.attributes("-alpha", 0.0)
    dialog.grab_set()  # Bloquea interacciones con la ventana principal de fondo

    # Centrar la ventana flotante respecto a la pantalla principal
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 220
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 110
    dialog.geometry(f"+{x}+{y}")

    # Tarjeta de diseño HUD con bordes y colores de la app
    card_modal = ctk.CTkFrame(dialog, fg_color=COLOR_CARD, border_color=COLOR_ACCENT, border_width=1, corner_radius=12)
    card_modal.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(card_modal, text="⚠️ CONFIRMAR CIERRE DE SESIÓN", font=ctk.CTkFont("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(pady=(22, 8))
    
    ctk.CTkLabel(card_modal, text="¿Estás seguro de que deseas cerrar sesión\ny regresar al panel principal de acceso?", 
                 font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT, justify="center").pack(pady=(0, 20))

    f_btns = ctk.CTkFrame(card_modal, fg_color="transparent")
    f_btns.pack(pady=(0, 15))

    id_anim_dialog = None
    def animar_aparicion(alpha=0.0):
        nonlocal id_anim_dialog
        if alpha < 1.0:
            alpha += 0.1
            dialog.attributes("-alpha", alpha)
            id_anim_dialog = dialog.after(15, lambda: animar_aparicion(alpha))

    def cancelar():
        if id_anim_dialog:
            try: dialog.after_cancel(id_anim_dialog)
            except: pass
        resultado["confirmado"] = False
        dialog.destroy()

    def aceptar():
        if id_anim_dialog:
            try: dialog.after_cancel(id_anim_dialog)
            except: pass
        resultado["confirmado"] = True
        dialog.destroy()

    btn_cancelar = ctk.CTkButton(f_btns, text="Cancelar", command=cancelar, width=130, height=38,
                                 fg_color=COLOR_ENTRY_BG, hover_color=COLOR_BORDER, text_color=COLOR_TEXT_LIGHT, 
                                 font=ctk.CTkFont("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2")
    btn_cancelar.pack(side="left", padx=10)

    btn_aceptar = ctk.CTkButton(f_btns, text="Sí, Cerrar Sesión", command=aceptar, width=140, height=38,
                                fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT, 
                                font=ctk.CTkFont("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2")
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

    def animar_entrada(alpha=0.0):
        nonlocal id_animacion
        if alpha < 1.0 and ventana.winfo_exists():
            alpha += 0.05
            ventana.attributes("-alpha", alpha)
            id_animacion = ventana.after(20, lambda: animar_entrada(alpha))

    def cerrar_sesion():
        # Llamamos a nuestro modal personalizado HUD en lugar de messagebox.askyesno
        if confirmar_cierre_sesion_hud(ventana):
            if id_animacion is not None:
                try:
                    ventana.after_cancel(id_animacion)
                except Exception:
                    pass
            
            sesion_cerrada["estado"] = True
            ventana.quit()
            ventana.destroy()

    # Estilos TTK solo para los Treeview (Tablas), ya que CTk no tiene tablas nativas
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=35, font=("Segoe UI", 10))
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("Treeview.Heading", background=COLOR_CARD, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 10, "bold"), borderwidth=0)

    # Contenedor Principal
    container_main = ctk.CTkFrame(ventana, fg_color=COLOR_BG_DARK)
    container_main.pack(fill="both", expand=True, padx=20, pady=20)

    # Header Superior
    header = ctk.CTkFrame(container_main, fg_color=COLOR_CARD, height=60, corner_radius=10)
    header.pack(fill="x", pady=(0, 15))
    header.pack_propagate(False)

    ctk.CTkLabel(header, text="⚙️ MÓDULO ADMINISTRADOR DE CONTENIDO Y SISTEMA", font=ctk.CTkFont("Segoe UI", 16, "bold"),
                 text_color=COLOR_ACCENT).pack(side="left", padx=20)

    btn_cerrar = ctk.CTkButton(header, text="CERRAR SESIÓN", command=cerrar_sesion, font=ctk.CTkFont("Segoe UI", 12, "bold"),
                               fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, text_color=COLOR_TEXT_LIGHT, corner_radius=8, cursor="hand2")
    btn_cerrar.pack(side="right", padx=15, pady=10)

    btn_ayuda = ctk.CTkButton(header, text="❓ AYUDA / TUTORIAL",
                              command=lambda: open_tutorial(ventana, role="admin", auto=False),
                              font=ctk.CTkFont("Segoe UI", 12, "bold"),
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

    ctk.CTkLabel(f_sel_u, text="Seleccionar Unidad:", font=ctk.CTkFont("Segoe UI", 13, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 10))

    combo_unidades = ctk.CTkComboBox(f_sel_u, state="readonly", font=ctk.CTkFont("Segoe UI", 13), width=400, 
                                     fg_color=COLOR_ENTRY_BG, border_color=COLOR_BORDER, dropdown_fg_color=COLOR_CARD)
    combo_unidades.pack(side="left", padx=5)

    f_tit_u = ctk.CTkFrame(tab_teoria, fg_color="transparent")
    f_tit_u.pack(fill="x", padx=15, pady=5)

    ctk.CTkLabel(f_tit_u, text="Título de la Unidad:", font=ctk.CTkFont("Segoe UI", 13, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=(0, 10))

    entry_titulo_u = ctk.CTkEntry(f_tit_u, font=ctk.CTkFont("Segoe UI", 13), fg_color=COLOR_ENTRY_BG, 
                                  text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER, corner_radius=5)
    entry_titulo_u.pack(side="left", fill="x", expand=True)

    f_txt_u = ctk.CTkFrame(tab_teoria, fg_color="transparent")
    f_txt_u.pack(fill="both", expand=True, padx=15, pady=10)

    ctk.CTkLabel(f_txt_u, text="Contenido Teórico Completo (Escribe o extiende los subtemas 1.1, 1.2, etc.):",
                 font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", pady=(0, 5))

    txt_teoria_editor = ctk.CTkTextbox(f_txt_u, wrap="word", font=ctk.CTkFont("Consolas", 13), fg_color=COLOR_ENTRY_BG, 
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
                                       command=guardar_teoria_unidad, font=ctk.CTkFont("Segoe UI", 13, "bold"),
                                       fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, text_color=COLOR_BG_DARK, 
                                       corner_radius=8, cursor="hand2", height=40)
    btn_guardar_teoria.pack(pady=15)

    # =============================================================
    # PESTAÑA 2: BANCO DE PREGUNTAS (SELECCIÓN POR UNIDAD)
    # =============================================================
    tab_preg = notebook.tab(tab_preguntas_name)

    f_top_q = ctk.CTkFrame(tab_preg, fg_color="transparent")
    f_top_q.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(f_top_q, text="Seleccionar Unidad Destino:", font=ctk.CTkFont("Segoe UI", 13, "bold"), 
                 text_color=COLOR_ACCENT).pack(side="left", padx=(0, 10))

    combo_q_unidades = ctk.CTkComboBox(f_top_q, state="readonly", font=ctk.CTkFont("Segoe UI", 13), width=400,
                                       fg_color=COLOR_ENTRY_BG, border_color=COLOR_BORDER)
    combo_q_unidades.pack(side="left", padx=5)

    f_form_q = ctk.CTkFrame(tab_preg, fg_color=COLOR_ENTRY_BG, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
    f_form_q.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(f_form_q, text="Pregunta:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", padx=15, pady=10)
    entry_q_texto = ctk.CTkEntry(f_form_q, font=ctk.CTkFont("Segoe UI", 13), fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_q_texto.grid(row=0, column=1, columnspan=3, sticky="ew", padx=15, pady=10)

    ctk.CTkLabel(f_form_q, text="Opción A:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=1, column=0, sticky="w", padx=15, pady=5)
    entry_op_a = ctk.CTkEntry(f_form_q, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_a.grid(row=1, column=1, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Opción B:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=1, column=2, sticky="w", padx=15, pady=5)
    entry_op_b = ctk.CTkEntry(f_form_q, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_b.grid(row=1, column=3, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Opción C:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=2, column=0, sticky="w", padx=15, pady=5)
    entry_op_c = ctk.CTkEntry(f_form_q, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_c.grid(row=2, column=1, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Opción D:", font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).grid(row=2, column=2, sticky="w", padx=15, pady=5)
    entry_op_d = ctk.CTkEntry(f_form_q, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0)
    entry_op_d.grid(row=2, column=3, sticky="ew", padx=15, pady=5)

    ctk.CTkLabel(f_form_q, text="Respuesta Correcta:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).grid(row=3, column=0, sticky="w", padx=15, pady=10)
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
                              font=ctk.CTkFont("Segoe UI", 12, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
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
                              font=ctk.CTkFont("Segoe UI", 12, "bold"), fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER,
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

    f_f_user = ctk.CTkFrame(tab_usr, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    f_f_user.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(f_f_user, text="Nuevo Usuario:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=15, pady=15)
    entry_u_name = ctk.CTkEntry(f_f_user, font=ctk.CTkFont("Segoe UI", 12), fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_u_name.pack(side="left", padx=5)

    ctk.CTkLabel(f_f_user, text="Contraseña:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=15)
    entry_u_pass = ctk.CTkEntry(f_f_user, font=ctk.CTkFont("Segoe UI", 12), show="*", fg_color=COLOR_CARD, border_width=0, corner_radius=5)
    entry_u_pass.pack(side="left", padx=5)

    ctk.CTkLabel(f_f_user, text="Rol:", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(side="left", padx=15)
    combo_u_rol = ctk.CTkComboBox(f_f_user, values=["alumno", "docente", "admin"], state="readonly", width=120, fg_color=COLOR_CARD, border_width=0)
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

    btn_add_u = ctk.CTkButton(f_f_user, text="REGISTRAR", command=agregar_usuario, font=ctk.CTkFont("Segoe UI", 12, "bold"),
                              fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK, cursor="hand2")
    btn_add_u.pack(side="left", padx=25)

    f_tbl_u = ctk.CTkFrame(tab_usr, fg_color="transparent")
    f_tbl_u.pack(fill="both", expand=True, padx=15, pady=10)

    tabla_users = ttk.Treeview(f_tbl_u, columns=("id", "usr", "rol"), show="headings", height=8)
    tabla_users.heading("id", text="ID")
    tabla_users.heading("usr", text="Nombre de Usuario")
    tabla_users.heading("rol", text="Rol de Sistema")
    tabla_users.column("id", width=50, anchor="center")
    tabla_users.column("usr", width=250)
    tabla_users.column("rol", width=150, anchor="center")
    tabla_users.pack(side="left", fill="both", expand=True)

    scroll_u_tbl = ctk.CTkScrollbar(f_tbl_u, orientation="vertical", command=tabla_users.yview)
    tabla_users.configure(yscrollcommand=scroll_u_tbl.set)
    scroll_u_tbl.pack(side="right", fill="y")

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

    btn_del_u = ctk.CTkButton(tab_usr, text="🗑️ ELIMINAR USUARIO", command=eliminar_usuario_sel,
                              font=ctk.CTkFont("Segoe UI", 12, "bold"), fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, 
                              text_color=COLOR_TEXT_LIGHT, cursor="hand2")
    btn_del_u.pack(anchor="e", padx=15, pady=(0, 10))

    # Carga Inicial de Datos
    cargar_datos_unidades()
    sincronizar_combos()
    cargar_usuarios_tabla()

    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.after(100, animar_entrada)
    ventana.after(350, lambda: open_tutorial(ventana, role="admin", auto=True))
    
    ventana.mainloop()
    
    return sesion_cerrada["estado"]
