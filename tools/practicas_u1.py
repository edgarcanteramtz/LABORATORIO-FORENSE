import tkinter as tk
from tkinter import messagebox, ttk

# Colores importados para mantener el mismo diseño de la app
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BG_DARK = "#05070A"

def cargar_practica_u1_p1(parent):
    for w in parent.winfo_children():
        w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.1: TRIVIA DE PRINCIPIOS FORENSES", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    
    escenario = "Escenario: Eres el primer perito en llegar a una escena corporativa.\nEncuentras un servidor encendido sospechoso de estar ejecutando un malware en memoria RAM."
    tk.Label(card, text=escenario, font=("Segoe UI", 11, "italic"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=10)
    tk.Label(card, text="Basado en el 'Principio de Mínima Intervención', ¿cuál es la acción inicial correcta?", font=("Segoe UI", 10, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [
        ("A) Apagar el servidor desconectando el cable de corriente inmediatamente.", "A"),
        ("B) Realizar un volcado (dump) de la memoria RAM antes de apagar.", "B"),
        ("C) Conectar un disco duro USB y copiar las carpetas principales.", "C"),
        ("D) Reiniciar el servidor en modo seguro.", "D")
    ]
    for texto, valor in opciones:
        tk.Radiobutton(card, text=texto, variable=var_resp, value=valor, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD, activebackground=COLOR_ENTRY_BG, activeforeground=COLOR_ACCENT, cursor="hand2").pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "B":
            messagebox.showinfo("¡Correcto!", "¡Excelente! Apagar el equipo destruiría la evidencia volátil en la RAM. Hacer un volcado primero respeta la mínima alteración.")
        elif var_resp.get() == "":
            messagebox.showwarning("Atención", "Selecciona una opción.")
        else:
            messagebox.showerror("Incorrecto", "Esa acción alteraría drásticamente el estado del sistema o destruiría evidencia clave en memoria.")
    
    btn_verificar = tk.Button(card, text="VERIFICAR RESPUESTA", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
    btn_verificar.pack(pady=20, ipadx=15, ipady=6)

def cargar_practica_u1_p2(parent):
    for w in parent.winfo_children():
        w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.2: SIMULADOR DE CUMPLIMIENTO (ISO/IEC 27037)", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    
    escenario = "Escenario: Durante una intervención, encuentras varios smartphones y tablets.\nDe acuerdo a la norma ISO/IEC 27037 sobre identificación y resguardo..."
    tk.Label(card, text=escenario, font=("Segoe UI", 11, "italic"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=10)
    tk.Label(card, text="¿Cuál de las siguientes es una directriz internacional obligatoria?", font=("Segoe UI", 10, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [
        ("A) Entregar los dispositivos al equipo de TI local para que los revisen.", "A"),
        ("B) Aislarlos de redes inalámbricas (ej. jaula de Faraday) e identificarlos físicamente.", "B"),
        ("C) Intentar desbloquearlos ingresando contraseñas al azar para ahorrar tiempo.", "C")
    ]
    for texto, valor in opciones:
        tk.Radiobutton(card, text=texto, variable=var_resp, value=valor, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD, activebackground=COLOR_ENTRY_BG, activeforeground=COLOR_ACCENT, cursor="hand2").pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "B":
            messagebox.showinfo("Cumplimiento Exitoso", "¡Correcto! Aislar las señales evita el borrado remoto (wiping) y cumple con las directrices de preservación de la ISO 27037.")
        elif var_resp.get() == "":
            messagebox.showwarning("Atención", "Selecciona una directriz.")
        else:
            messagebox.showerror("Fallo de Cumplimiento", "Incorrecto. Esa acción violaría las normas internacionales de aseguramiento de evidencia.")
    
    tk.Button(card, text="EVALUAR DECISIÓN", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(pady=20, ipadx=15, ipady=6)

def cargar_practica_u1_p3(parent):
    for w in parent.winfo_children():
        w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.3: EMPAREJAMIENTO DE TERMINOLOGÍA", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    tk.Label(card, text="Relaciona cada definición con el concepto forense correcto:", font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=5)

    frame_grid = tk.Frame(card, bg=COLOR_ENTRY_BG)
    frame_grid.pack(pady=10)

    conceptos = ["", "Cadena de Custodia", "Evidencia Digital", "Principio de Locard", "Hash"]
    
    tk.Label(frame_grid, text="1. Todo contacto deja un rastro.", font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=5)
    combo1 = ttk.Combobox(frame_grid, values=conceptos, state="readonly", width=20)
    combo1.grid(row=0, column=1, padx=20, pady=5)

    tk.Label(frame_grid, text="2. Información binaria utilizable en juicio.", font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED).grid(row=1, column=0, sticky="w", pady=5)
    combo2 = ttk.Combobox(frame_grid, values=conceptos, state="readonly", width=20)
    combo2.grid(row=1, column=1, padx=20, pady=5)

    tk.Label(frame_grid, text="3. Proceso de documentación rigurosa.", font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED).grid(row=2, column=0, sticky="w", pady=5)
    combo3 = ttk.Combobox(frame_grid, values=conceptos, state="readonly", width=20)
    combo3.grid(row=2, column=1, padx=20, pady=5)

    def verificar():
        if combo1.get() == "Principio de Locard" and combo2.get() == "Evidencia Digital" and combo3.get() == "Cadena de Custodia":
            messagebox.showinfo("¡Perfecto!", "Has emparejado todos los términos forenses correctamente.")
        else:
            messagebox.showerror("Error", "Algunas respuestas no son correctas. Revisa tus conceptos y vuelve a intentarlo.")

    tk.Button(card, text="VERIFICAR CONCEPTOS", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(pady=20, ipadx=15, ipady=6)

def cargar_practica_u1_p4(parent):
    for w in parent.winfo_children():
        w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.4: ANÁLISIS DE CASO REAL JURÍDICO", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    
    caso = (
        "Caso: En un juicio por fraude, la defensa logró anular la prueba pericial.\n"
        "El perito extrajo el disco duro original, lo conectó directamente a su laptop (sin usar un \n"
        "bloqueador de escritura), y arrastró los archivos sospechosos hacia su escritorio para analizarlos."
    )
    tk.Label(card, text=caso, font=("Segoe UI", 11, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, justify="center", padx=10, pady=10).pack(pady=10)
    tk.Label(card, text="¿Por qué el juez declaró la evidencia como inadmisible?", font=("Segoe UI", 10, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [
        ("A) Porque se violó la privacidad del acusado según la LOPD.", "A"),
        ("B) Porque al montarlo sin bloqueador, el SO de la laptop modificó marcas de tiempo.", "B"),
        ("C) Porque no se pidieron permisos al equipo de ciberseguridad.", "C")
    ]
    for texto, valor in opciones:
        tk.Radiobutton(card, text=texto, variable=var_resp, value=valor, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD, activebackground=COLOR_ENTRY_BG, activeforeground=COLOR_ACCENT, cursor="hand2").pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "B":
            messagebox.showinfo("Veredicto Forense", "¡Exacto! Cualquier montaje de disco en modo lectura/escritura altera inmediatamente los metadatos y contamina la evidencia.")
        elif var_resp.get() == "":
            messagebox.showwarning("Atención", "Emite tu veredicto seleccionando una opción.")
        else:
            messagebox.showerror("Objeción", "Incorrecto. La anulación directa se da por la alteración tecnológica de la evidencia original.")
    
    tk.Button(card, text="EMITIR VEREDICTO", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(pady=20, ipadx=15, ipady=6)