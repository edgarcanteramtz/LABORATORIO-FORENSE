import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

try:
    from tools.hash_calculator import generar_hash_archivo
except ImportError:
    import hashlib

    def generar_hash_archivo(ruta, algoritmo="sha256"):
        hasher = (
            hashlib.md5()
            if algoritmo == "md5"
            else (hashlib.sha1() if algoritmo == "sha1" else hashlib.sha256())
        )
        try:
            with open(ruta, "rb") as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

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

def obtener_temas_bd():
    """Consulta los temas en la base de datos."""
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, unidad, titulo, contenido_teorico FROM temas ORDER BY unidad ASC"
    )
    temas = cursor.fetchall()
    conexion.close()
    return temas

def obtener_preguntas_unidad(unidad_id):
    """Obtiene las preguntas asociadas a una unidad temática."""
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,"
        " respuesta_correcta FROM preguntas WHERE tema_id = ?",
        (unidad_id,),
    )
    preguntas = cursor.fetchall()
    conexion.close()
    return preguntas

def guardar_calificacion(usuario, tema_id, puntaje):
    """Registra el puntaje obtenido por el alumno en SQLite."""
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE nombre_usuario = ?", (usuario,)
    )
    user = cursor.fetchone()
    if user:
        alumno_id = user[0]
        cursor.execute(
            """
                INSERT INTO calificaciones (alumno_id, tema_id, puntaje)
                VALUES (?, ?, ?)
            """,
            (alumno_id, tema_id, puntaje),
        )
        conexion.commit()
    conexion.close()

def abrir_panel_alumno(usuario):
    """Módulo principal del Alumno con 3 pestañas: Teoría, Hashes y Evaluaciones."""
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Módulo Alumno ({usuario})")
    ventana.attributes('-fullscreen', True)  # Pantalla completa
    ventana.configure(bg=COLOR_BG_DARK)

    ventana.attributes("-alpha", 0.0)

    def animar_entrada(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            ventana.attributes("-alpha", alpha)
            ventana.after(20, lambda: animar_entrada(alpha))

    # Configuración de estilos modernos para ttk
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=COLOR_BG_DARK, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_MUTED, padding=[25, 12], font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", 
              background=[("selected", COLOR_CARD)], 
              foreground=[("selected", COLOR_ACCENT)])
    
    style.configure("TFrame", background=COLOR_CARD)
    style.configure("TCombobox", fieldbackground=COLOR_ENTRY_BG, background=COLOR_BORDER, foreground=COLOR_TEXT_LIGHT, borderwidth=0)

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=40, pady=30)

    # -------------------------------------------------------------
    # PESTAÑA 1: TEORÍA
    # -------------------------------------------------------------
    tab_teoria = ttk.Frame(pestanas)
    pestanas.add(tab_teoria, text="📚 Temario y Teoría")

    card_teoria = tk.Frame(tab_teoria, bg=COLOR_CARD, bd=0)
    card_teoria.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    tk.Label(
        card_teoria,
        text="UNIDADES DEL ANÁLISIS FORENSE INFORMÁTICO",
        font=("Segoe UI", 16, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT_LIGHT
    ).pack(pady=(20, 10))

    # Double Frame para el área de texto
    frame_outer_text = tk.Frame(card_teoria, bg=COLOR_BORDER, bd=0)
    frame_outer_text.pack(fill="both", expand=True, padx=40, pady=(10, 30))
    
    frame_inner_text = tk.Frame(frame_outer_text, bg=COLOR_ENTRY_BG, bd=0)
    frame_inner_text.pack(fill="both", expand=True, padx=1, pady=1)

    scroll = ttk.Scrollbar(frame_inner_text)
    scroll.pack(side="right", fill="y")

    area_teoria = tk.Text(
        frame_inner_text, yscrollcommand=scroll.set, wrap="word", 
        font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, 
        relief="flat", bd=0, padx=20, pady=20
    )
    area_teoria.pack(side="left", fill="both", expand=True)
    scroll.config(command=area_teoria.yview)

    # Configurar estilo visual de los títulos de unidad
    area_teoria.tag_configure("titulo", foreground=COLOR_ACCENT, font=("Segoe UI", 13, "bold"))

    temas = obtener_temas_bd()
    if temas:
        for t_id, unidad, titulo, contenido in temas:
            area_teoria.insert(
                "end", f"=== UNIDAD {unidad}: {titulo} ===\n\n", "titulo"
            )
            area_teoria.insert("end", f"{contenido}\n\n")
            area_teoria.insert("end", "-" * 80 + "\n\n")
    area_teoria.config(state="disabled")

    # -------------------------------------------------------------
    # PESTAÑA 2: PRÁCTICA (CALCULADORA DE HASHES)
    # -------------------------------------------------------------
    tab_hashes = ttk.Frame(pestanas)
    pestanas.add(tab_hashes, text="🛠️ Práctica: Hashes")

    card_hashes = tk.Frame(tab_hashes, bg=COLOR_CARD, bd=0)
    card_hashes.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

    tk.Label(
        card_hashes,
        text="VERIFICACIÓN DE INTEGRIDAD DE EVIDENCIAS DIGITALES",
        font=("Segoe UI", 14, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT_LIGHT
    ).pack(pady=(40, 30))

    ruta_archivo_var = tk.StringVar()

    def seleccionar_archivo():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de evidencia"
        )
        if archivo:
            ruta_archivo_var.set(archivo)

    def calcular():
        ruta = ruta_archivo_var.get()
        if not ruta:
            messagebox.showwarning(
                "Atención", "Por favor selecciona un archivo primero."
            )
            return
        algoritmo = combo_algo.get().lower()
        hash_res = generar_hash_archivo(ruta, algoritmo)
        
        # Habilitar temporalmente para insertar, luego volver a read-only visual
        entry_resultado.config(state="normal")
        entry_resultado.delete(0, tk.END)
        entry_resultado.insert(0, hash_res)
        entry_resultado.config(state="readonly")

    # Controles archivo
    frame_controles = tk.Frame(card_hashes, bg=COLOR_CARD)
    frame_controles.pack(pady=10, fill="x", padx=40)

    btn_buscar = tk.Button(frame_controles, text="BUSCAR ARCHIVO", command=seleccionar_archivo, font=("Segoe UI", 10, "bold"), bg=COLOR_BORDER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_ENTRY_BG, relief="flat", cursor="hand2", bd=0)
    btn_buscar.pack(side="left", ipady=8, ipadx=10)
    aplicar_hover(btn_buscar, COLOR_BORDER, COLOR_ENTRY_BG)

    # Input estético para la ruta
    frame_ruta = tk.Frame(frame_controles, bg=COLOR_BORDER, bd=0)
    frame_ruta.pack(side="left", fill="x", expand=True, padx=(10, 0))
    inner_ruta = tk.Frame(frame_ruta, bg=COLOR_ENTRY_BG, bd=0)
    inner_ruta.pack(fill="both", expand=True, padx=1, pady=1)
    
    entry_ruta = tk.Entry(inner_ruta, textvariable=ruta_archivo_var, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED, relief="flat", bd=0, state="readonly")
    entry_ruta.pack(fill="x", padx=10, pady=8)

    # Controles Algoritmo
    tk.Label(card_hashes, text="ALGORITMO DE HASH:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(30, 5))
    
    combo_algo = ttk.Combobox(
        card_hashes, values=["SHA256", "MD5", "SHA1"], state="readonly", font=("Segoe UI", 11)
    )
    combo_algo.set("SHA256")
    combo_algo.pack(ipadx=10, ipady=4)

    # Botón Calcular
    btn_calcular = tk.Button(card_hashes, text="CALCULAR HASH", command=calcular, font=("Segoe UI", 11, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER, relief="flat", cursor="hand2", bd=0)
    btn_calcular.pack(pady=(30, 20), ipady=10, fill="x", padx=200)
    aplicar_hover(btn_calcular, COLOR_ACCENT, COLOR_ACCENT_HOVER)

    # Resultado
    tk.Label(card_hashes, text="RESULTADO DEL ANÁLISIS:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(10, 5))
    
    frame_res = tk.Frame(card_hashes, bg=COLOR_BORDER, bd=0)
    frame_res.pack(fill="x", padx=40)
    inner_res = tk.Frame(frame_res, bg=COLOR_ENTRY_BG, bd=0)
    inner_res.pack(fill="both", expand=True, padx=1, pady=1)
    
    entry_resultado = tk.Entry(inner_res, font=("Consolas", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT, relief="flat", bd=0, justify="center")
    entry_resultado.pack(fill="x", padx=10, pady=12)
    entry_resultado.config(state="readonly")

    # -------------------------------------------------------------
    # PESTAÑA 3: CUESTIONARIOS / EVALUACIONES
    # -------------------------------------------------------------
    tab_eval = ttk.Frame(pestanas)
    pestanas.add(tab_eval, text="📝 Cuestionarios")

    card_eval = tk.Frame(tab_eval, bg=COLOR_CARD, bd=0)
    card_eval.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.9)

    tk.Label(
        card_eval,
        text="EVALUACIÓN TEÓRICA",
        font=("Segoe UI", 16, "bold"),
        bg=COLOR_CARD,
        fg=COLOR_TEXT_LIGHT
    ).pack(pady=(25, 10))

    tk.Label(card_eval, text="SELECCIONA LA UNIDAD A EVALUAR:", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(0, 5))
    combo_unidades = ttk.Combobox(
        card_eval,
        values=[f"Unidad {t[1]}: {t[2]}" for t in temas],
        state="readonly",
        font=("Segoe UI", 11)
    )
    combo_unidades.pack(fill="x", padx=200, pady=(0, 20), ipady=4)

    # Área de las preguntas
    frame_quiz = tk.Frame(card_eval, bg=COLOR_CARD)
    frame_quiz.pack(fill="both", expand=True, padx=40, pady=10)

    respuestas_usuario = {}
    preguntas_actuales = []
    tema_seleccionado_id = [None]

    def evaluar_respuestas():
        if not preguntas_actuales:
            return

        correctas = 0
        total = len(preguntas_actuales)

        for p in preguntas_actuales:
            p_id = p[0]
            resp_correcta = p[6]
            if respuestas_usuario.get(p_id, tk.StringVar()).get() == resp_correcta:
                correctas += 1

        puntaje_final = int((correctas / total) * 100)
        guardar_calificacion(usuario, tema_seleccionado_id[0], puntaje_final)

        messagebox.showinfo(
            "Resultado del Análisis",
            f"Evaluación Finalizada.\nAciertos: {correctas}/{total}\nCalificación:"
            f" {puntaje_final}/100\n\nProtocolo registrado en la base de datos.",
        )

    btn_enviar = tk.Button(card_eval, text="ENVIAR RESPUESTAS", command=evaluar_respuestas, font=("Segoe UI", 11, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER, relief="flat", cursor="hand2", bd=0)
    
    def cargar_cuestionario(event):
        """Muestra las preguntas según la unidad elegida en el ComboBox."""
        for widget in frame_quiz.winfo_children():
            widget.destroy()
        btn_enviar.pack_forget()

        idx = combo_unidades.current()
        if idx == -1:
            return

        tema_actual = temas[idx]
        tema_seleccionado_id[0] = tema_actual[0]
        preguntas_actuales.clear()
        preguntas_actuales.extend(obtener_preguntas_unidad(tema_actual[0]))

        if not preguntas_actuales:
            tk.Label(
                frame_quiz,
                text="No hay datos registrados para esta unidad en el servidor.",
                font=("Segoe UI", 11, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED
            ).pack(pady=40)
            return

        respuestas_usuario.clear()

        for p_idx, p in enumerate(preguntas_actuales):
            p_id, preg, op_a, op_b, op_c, op_d, resp_correcta = p
            tk.Label(
                frame_quiz,
                text=f"{p_idx + 1}. {preg}",
                font=("Segoe UI", 11, "bold"),
                bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT,
                wraplength=800, justify="left"
            ).pack(anchor="w", pady=(15, 8))

            var_resp = tk.StringVar(value="")
            respuestas_usuario[p_id] = var_resp

            opciones = [("A) " + op_a, "A"), ("B) " + op_b, "B"), ("C) " + op_c, "C"), ("D) " + op_d, "D")]
            for txt, val in opciones:
                # Usamos tk.Radiobutton puro para adaptarlo al modo oscuro
                tk.Radiobutton(
                    frame_quiz, text=txt, value=val, variable=var_resp,
                    font=("Segoe UI", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                    selectcolor=COLOR_ENTRY_BG, activebackground=COLOR_CARD, activeforeground=COLOR_ACCENT,
                    cursor="hand2"
                ).pack(anchor="w", padx=20, pady=2)

        # Mostrar el botón enviar solo si hay preguntas
        btn_enviar.pack(pady=25, ipady=12, fill="x", padx=200)
        aplicar_hover(btn_enviar, COLOR_ACCENT, COLOR_ACCENT_HOVER)

    combo_unidades.bind("<<ComboboxSelected>>", cargar_cuestionario)

    # =============================================================
    # BOTÓN GLOBAL: CERRAR SESIÓN
    # =============================================================
    btn_cerrar = tk.Button(
        ventana, 
        text="CERRAR SESIÓN DE ALUMNO", 
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

    # Atajo de teclado
    ventana.bind("<Escape>", lambda e: ventana.destroy())

    ventana.after(100, animar_entrada)
    ventana.mainloop()