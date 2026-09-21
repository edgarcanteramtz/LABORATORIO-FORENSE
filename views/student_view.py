import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

# Importación de herramientas
try:
    from tools.hash_calculator import generar_hash_archivo
except ImportError:
    import hashlib


    def generar_hash_archivo(ruta, algoritmo="sha256"):
        hasher = hashlib.md5() if algoritmo == "md5" else (hashlib.sha1() if algoritmo == "sha1" else hashlib.sha256())
        try:
            with open(ruta, "rb") as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"

try:
    from tools.exif_extractor import extraer_metadatos_imagen
except ImportError:
    def extraer_metadatos_imagen(ruta):
        return {"Error": "Módulo tools.exif_extractor no encontrado."}

try:
    from tools.report_generator import generar_reporte_txt
except ImportError:
    def generar_reporte_txt(tipo, user, datos):
        return "reporte.txt", "Error: Módulo report_generator no encontrado."

# ==========================================
# PALETA DE COLORES "HUD FORENSIC / HIGH-TECH"
# ==========================================
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


def abrir_panel_alumno(usuario):
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Módulo Guiado ({usuario})")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg=COLOR_BG_DARK)
    ventana.attributes("-alpha", 0.0)

    def animar_entrada(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            ventana.attributes("-alpha", alpha)
            ventana.after(20, lambda: animar_entrada(alpha))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_LIGHT, fieldbackground=COLOR_ENTRY_BG,
                    borderwidth=0, rowheight=30)
    style.map('Treeview', background=[('selected', COLOR_BORDER)], foreground=[('selected', COLOR_ACCENT)])
    style.configure("TNotebook", background=COLOR_CARD, borderwidth=0)
    style.configure("TNotebook.Tab", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT_MUTED, padding=[15, 8],
                    font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", COLOR_CARD)], foreground=[("selected", COLOR_ACCENT)])

    # Layout Principal: Sidebar (Izquierda) + Contenido (Derecha)
    container_main = tk.Frame(ventana, bg=COLOR_BG_DARK)
    container_main.pack(fill="both", expand=True, padx=20, pady=20)

    # -------------------------------------------------------------
    # SIDEBAR: LISTA DEL TEMARIO
    # -------------------------------------------------------------
    sidebar = tk.Frame(container_main, bg=COLOR_CARD, width=320)
    sidebar.pack(side="left", fill="y", padx=(0, 15))
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="📚 TEMARIO DEL CURSO", font=("Segoe UI", 12, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT).pack(
        pady=(20, 10), padx=15, anchor="w")

    listbox_temas = tk.Listbox(sidebar, bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectbackground=COLOR_BORDER,
                               selectforeground=COLOR_ACCENT, font=("Segoe UI", 10), bd=0, highlightthickness=0)
    listbox_temas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    temas = obtener_temas_bd()
    for t in temas:
        listbox_temas.insert("end", f" Unidad {t[1]}: {t[2]}")

    btn_cerrar = tk.Button(sidebar, text="CERRAR SESIÓN", command=ventana.destroy, font=("Segoe UI", 10, "bold"),
                           bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_DANGER_HOVER, relief="flat",
                           cursor="hand2", bd=0)
    btn_cerrar.pack(fill="x", padx=15, pady=15, ipady=8)
    aplicar_hover(btn_cerrar, COLOR_DANGER, COLOR_DANGER_HOVER)

    # -------------------------------------------------------------
    # PANEL DERECHO: CONTENIDO DEL TEMA
    # -------------------------------------------------------------
    panel_derecho = tk.Frame(container_main, bg=COLOR_CARD)
    panel_derecho.pack(side="right", fill="both", expand=True)

    lbl_titulo_tema = tk.Label(panel_derecho, text="Selecciona un tema del temario para comenzar",
                               font=("Segoe UI", 14, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT)
    lbl_titulo_tema.pack(pady=(20, 10), padx=25, anchor="w")

    sub_pestanas = ttk.Notebook(panel_derecho)
    sub_pestanas.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # --- PASO 1: TEORÍA Y EXPLICACIÓN ---
    tab_teoria = ttk.Frame(sub_pestanas)
    sub_pestanas.add(tab_teoria, text="📖 1. Explicación")

    area_teoria = tk.Text(tab_teoria, wrap="word", font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT,
                          relief="flat", bd=0, padx=20, pady=20)
    area_teoria.pack(fill="both", expand=True, padx=15, pady=15)

    # --- PASO 2: CUESTIONARIO DE 10 PREGUNTAS ---
    tab_quiz = ttk.Frame(sub_pestanas)
    sub_pestanas.add(tab_quiz, text="📝 2. Cuestionario (10 Preguntas)")

    frame_scroll_quiz = tk.Canvas(tab_quiz, bg=COLOR_CARD, highlightthickness=0)
    scrollbar_quiz = ttk.Scrollbar(tab_quiz, orient="vertical", command=frame_scroll_quiz.yview)
    scrollable_quiz_inner = tk.Frame(frame_scroll_quiz, bg=COLOR_CARD)

    scrollable_quiz_inner.bind(
        "<Configure>",
        lambda e: frame_scroll_quiz.configure(scrollregion=frame_scroll_quiz.bbox("all"))
    )

    frame_scroll_quiz.create_window((0, 0), window=scrollable_quiz_inner, anchor="nw")
    frame_scroll_quiz.configure(yscrollcommand=scrollbar_quiz.set)

    frame_scroll_quiz.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar_quiz.pack(side="right", fill="y", pady=15)

    # --- PASO 3: PRÁCTICA GUIADA ---
    tab_practica = ttk.Frame(sub_pestanas)
    sub_pestanas.add(tab_practica, text="🛠️ 3. Práctica Aplicada")

    container_practica = tk.Frame(tab_practica, bg=COLOR_CARD)
    container_practica.pack(fill="both", expand=True, padx=15, pady=15)

    # Variables globales de estado del tema activo
    tema_activo = {"id": None, "unidad": None, "titulo": ""}
    respuestas_usuario = {}
    preguntas_actuales = []

    # -------------------------------------------------------------
    # CONSTRUCTORES DE VISTAS PRÁCTICAS
    # -------------------------------------------------------------
    def cargar_practica_hashes(parent):
        for w in parent.winfo_children():
            w.destroy()

        card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(card, text="PRÁCTICA: VERIFICACIÓN DE HASHES Y CADENA DE CUSTODIA", font=("Segoe UI", 12, "bold"),
                 bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))

        ruta_var = tk.StringVar()
        res_var = tk.StringVar()

        def seleccionar():
            arch = filedialog.askopenfilename()
            if arch:
                ruta_var.set(arch)

        def calcular():
            if not ruta_var.get():
                messagebox.showwarning("Atención", "Selecciona un archivo.")
                return
            res = generar_hash_archivo(ruta_var.get(), combo_algo.get().lower())
            res_var.set(res)

        def exportar():
            if not res_var.get():
                messagebox.showwarning("Atención", "Calcula un hash primero.")
                return
            datos = {"Archivo": os.path.basename(ruta_var.get()), "Ruta": ruta_var.get(), "Algoritmo": combo_algo.get(),
                     "Hash": res_var.get()}
            nom, txt = generar_reporte_txt("HASH_INTEGRIDAD", usuario, datos)
            dest = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nom)
            if dest:
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(txt)
                messagebox.showinfo("Éxito", "Reporte guardado correctamente.")

        frame_f = tk.Frame(card, bg=COLOR_ENTRY_BG)
        frame_f.pack(pady=10)
        btn_b = tk.Button(frame_f, text="SELECCIONAR ARCHIVO", command=seleccionar, bg=COLOR_BORDER,
                          fg=COLOR_TEXT_LIGHT, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
        btn_b.pack(side="left", padx=5, ipady=5, ipadx=10)
        entry_r = tk.Entry(frame_f, textvariable=ruta_var, font=("Segoe UI", 10), width=40, bg=COLOR_CARD,
                           fg=COLOR_TEXT_MUTED, bd=0)
        entry_r.pack(side="left", padx=5, ipady=5)

        combo_algo = ttk.Combobox(card, values=["SHA256", "MD5", "SHA1"], state="readonly", font=("Segoe UI", 10))
        combo_algo.set("SHA256")
        combo_algo.pack(pady=10)

        btn_c = tk.Button(card, text="CALCULAR HASH", command=calcular, bg=COLOR_ACCENT, fg=COLOR_BG_DARK,
                          font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2")
        btn_c.pack(pady=10, ipadx=20, ipady=6)

        entry_res = tk.Entry(card, textvariable=res_var, font=("Consolas", 11, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT,
                             bd=0, justify="center", width=50)
        entry_res.pack(pady=10, ipady=6)

        btn_exp = tk.Button(card, text="📄 EXPORTAR REPORTE DE CADENA DE CUSTODIA", command=exportar, bg=COLOR_BORDER,
                            fg=COLOR_ACCENT, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
        btn_exp.pack(pady=15, ipady=8, ipadx=15)

    def cargar_practica_exif(parent):
        for w in parent.winfo_children():
            w.destroy()

        card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(card, text="PRÁCTICA: EXTRACTOR DE METADATOS Y CABECERAS EXIF", font=("Segoe UI", 12, "bold"),
                 bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(15, 10))

        ruta_img_var = tk.StringVar()
        ultimo_res = {}

        def seleccionar():
            arch = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.tiff")])
            if arch:
                ruta_img_var.set(arch)

        def analizar():
            if not ruta_img_var.get():
                messagebox.showwarning("Atención", "Selecciona una imagen.")
                return
            for item in tabla.get_children():
                tabla.delete(item)
            res = extraer_metadatos_imagen(ruta_img_var.get())
            ultimo_res.clear()
            ultimo_res.update(res)
            for k, v in res.items():
                if k == "EXIF" and isinstance(v, dict):
                    tabla.insert("", "end", values=("--- ETIQUETAS EXIF ---", "------------------"))
                    for sub_k, sub_v in v.items():
                        tabla.insert("", "end", values=(f"EXIF: {sub_k}", sub_v))
                else:
                    tabla.insert("", "end", values=(k, v))

        def exportar():
            if not ultimo_res:
                messagebox.showwarning("Atención", "Analiza una imagen primero.")
                return
            lineas = [f"{k}: {v}" for k, v in ultimo_res.items() if k != "EXIF"]
            if "EXIF" in ultimo_res and isinstance(ultimo_res["EXIF"], dict):
                lineas.append("ETIQUETAS EXIF:")
                for ek, ev in ultimo_res["EXIF"].items():
                    lineas.append(f"  - {ek}: {ev}")
            nom, txt = generar_reporte_txt("METADATOS_EXIF", usuario, lineas)
            dest = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nom)
            if dest:
                with open(dest, "w", encoding="utf-8") as f:
                    f.write(txt)
                messagebox.showinfo("Éxito", "Reporte guardado correctamente.")

        frame_top = tk.Frame(card, bg=COLOR_ENTRY_BG)
        frame_top.pack(fill="x", padx=10, pady=5)

        btn_b = tk.Button(frame_top, text="SELECCIONAR IMAGEN", command=seleccionar, bg=COLOR_BORDER,
                          fg=COLOR_TEXT_LIGHT, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
        btn_b.pack(side="left", ipadx=10, ipady=5)
        tk.Entry(frame_top, textvariable=ruta_img_var, font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 bd=0).pack(side="left", fill="x", expand=True, padx=10, ipady=5)
        btn_a = tk.Button(frame_top, text="ANALIZAR", command=analizar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK,
                          font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
        btn_a.pack(side="right", ipadx=15, ipady=5)

        tabla = ttk.Treeview(card, columns=("p", "v"), show="headings", height=8)
        tabla.heading("p", text="Propiedad")
        tabla.heading("v", text="Valor Extraído")
        tabla.column("p", width=200)
        tabla.column("v", width=450)
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        btn_e = tk.Button(card, text="📄 EXPORTAR REPORTE EXIF", command=exportar, bg=COLOR_BORDER, fg=COLOR_ACCENT,
                          font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
        btn_e.pack(pady=(0, 10), ipady=6, ipadx=15)

    # -------------------------------------------------------------
    # EVENTO AL SELECCIONAR UN TEMA EN LA LISTA
    # -------------------------------------------------------------
    def cargar_detalle_tema(event):
        seleccion = listbox_temas.curselection()
        if not seleccion:
            return

        idx = seleccion[0]
        t = temas[idx]
        tema_activo["id"] = t[0]
        tema_activo["unidad"] = t[1]
        tema_activo["titulo"] = t[2]

        lbl_titulo_tema.config(text=f"UNIDAD {t[1]}: {t[2]}")

        # 1. Cargar Teoría
        area_teoria.config(state="normal")
        area_teoria.delete("1.0", tk.END)
        area_teoria.insert("1.0", t[3] if t[3] else "Contenido teórico en elaboración.")
        area_teoria.config(state="disabled")

        # 2. Cargar Cuestionario
        for w in scrollable_quiz_inner.winfo_children():
            w.destroy()

        preguntas_actuales.clear()
        preguntas_actuales.extend(obtener_preguntas_unidad(t[0]))
        respuestas_usuario.clear()

        if not preguntas_actuales:
            tk.Label(scrollable_quiz_inner, text="No hay preguntas registradas para este tema.",
                     font=("Segoe UI", 11, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=30)
        else:
            for p_idx, p in enumerate(preguntas_actuales):
                p_id, preg, op_a, op_b, op_c, op_d, resp_correcta = p

                f_preg = tk.Frame(scrollable_quiz_inner, bg=COLOR_CARD)
                f_preg.pack(fill="x", expand=True, pady=10, anchor="w")

                tk.Label(f_preg, text=f"{p_idx + 1}. {preg}", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD,
                         fg=COLOR_TEXT_LIGHT, wraplength=700, justify="left").pack(anchor="w")

                var_resp = tk.StringVar(value="")
                respuestas_usuario[p_id] = var_resp

                opciones = [("A) " + op_a, "A"), ("B) " + op_b, "B"), ("C) " + op_c, "C"), ("D) " + op_d, "D")]
                for txt_o, val_o in opciones:
                    tk.Radiobutton(f_preg, text=txt_o, value=val_o, variable=var_resp, font=("Segoe UI", 9),
                                   bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, selectcolor=COLOR_ENTRY_BG,
                                   activebackground=COLOR_CARD, activeforeground=COLOR_ACCENT, cursor="hand2").pack(
                        anchor="w", padx=15, pady=2)

            def evaluar():
                correctas = sum(1 for p in preguntas_actuales if respuestas_usuario[p[0]].get() == p[6])
                total = len(preguntas_actuales)
                puntaje = int((correctas / total) * 100)
                guardar_calificacion(usuario, tema_activo["id"], puntaje)
                messagebox.showinfo("Evaluación Finalizada",
                                    f"Tema: Unidad {tema_activo['unidad']}\nAciertos: {correctas}/{total}\nCalificación: {puntaje}/100")

            btn_enviar = tk.Button(scrollable_quiz_inner, text="ENVIAR RESPUESTAS DEL TEMA", command=evaluar,
                                   font=("Segoe UI", 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG_DARK, relief="flat",
                                   cursor="hand2", bd=0)
            btn_enviar.pack(pady=20, ipady=8, ipadx=20)
            aplicar_hover(btn_enviar, COLOR_ACCENT, COLOR_ACCENT_HOVER)

        # 3. Cargar Práctica específica según la unidad
        if t[1] == 1:
            cargar_practica_hashes(container_practica)
        elif t[1] == 2:
            cargar_practica_exif(container_practica)
        else:
            for w in container_practica.winfo_children():
                w.destroy()
            tk.Label(container_practica, text=f"Práctica en desarrollo para la Unidad {t[1]}.",
                     font=("Segoe UI", 11, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=50)

        # Seleccionar por defecto la primera pestaña (Explicación)
        sub_pestanas.select(0)

    listbox_temas.bind("<<ListboxSelect>>", cargar_detalle_tema)

    # Seleccionar primer tema por defecto si existe
    if temas:
        listbox_temas.selection_set(0)
        listbox_temas.event_generate("<<ListboxSelect>>")

    ventana.bind("<Escape>", lambda e: ventana.destroy())
    ventana.after(100, animar_entrada)
    ventana.mainloop()