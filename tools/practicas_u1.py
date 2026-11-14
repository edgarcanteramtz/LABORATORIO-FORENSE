import tkinter as tk
from tkinter import messagebox, ttk

COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BG_DARK = "#05070A"

def cargar_practica_u1_p1(parent):
    for w in parent.winfo_children(): w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.1: TRIVIA DE PRINCIPIOS FORENSES", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    
    escenario = "Escenario: Eres el perito en una escena corporativa.\nEncuentras un servidor encendido sospechoso de ejecutar malware en memoria RAM."
    tk.Label(card, text=escenario, font=("Segoe UI", 11, "italic"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_MUTED, justify="center").pack(pady=10)
    tk.Label(card, text="Basado en el 'Principio de Mínima Intervención', ¿cuál es la acción inicial correcta?", font=("Segoe UI", 10, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [
        ("A) Apagar el servidor desconectando el cable de corriente inmediatamente.", "A"),
        ("B) Realizar un volcado (dump) de la memoria RAM antes de apagar.", "B"),
        ("C) Conectar un disco duro USB y copiar las carpetas principales.", "C")
    ]
    for texto, valor in opciones:
        tk.Radiobutton(card, text=texto, variable=var_resp, value=valor, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD, activebackground=COLOR_ENTRY_BG, activeforeground=COLOR_ACCENT).pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "B": messagebox.showinfo("¡Correcto!", "¡Excelente! Apagar el equipo destruiría la evidencia volátil en la RAM.")
        elif var_resp.get() == "": messagebox.showwarning("Atención", "Selecciona una opción.")
        else: messagebox.showerror("Incorrecto", "Esa acción alteraría drásticamente el estado del sistema.")
    tk.Button(card, text="VERIFICAR RESPUESTA", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2").pack(pady=20, ipadx=15, ipady=6)

def cargar_practica_u1_p2(parent):
    for w in parent.winfo_children(): w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.2: CUMPLIMIENTO (ISO/IEC 27037)", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    tk.Label(card, text="¿Cuál es una directriz internacional obligatoria para dispositivos móviles en una escena?", font=("Segoe UI", 10, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [
        ("A) Entregarlos al personal de TI local para revisión rápida.", "A"),
        ("B) Aislarlos de redes inalámbricas (jaula de Faraday) e identificarlos.", "B")
    ]
    for texto, valor in opciones:
        tk.Radiobutton(card, text=texto, variable=var_resp, value=valor, font=("Segoe UI", 10), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD).pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "B": messagebox.showinfo("Éxito", "Correcto. Aislar las señales evita el borrado remoto.")
        else: messagebox.showerror("Error", "Incorrecto.")
    tk.Button(card, text="EVALUAR", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0).pack(pady=20, ipadx=15, ipady=6)

def cargar_practica_u1_p3(parent):
    for w in parent.winfo_children(): w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.3: PRINCIPIO DE LOCARD", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    tk.Label(card, text="El principio de Locard aplicado al ámbito digital indica que...", font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [("A) Todo contacto con un sistema deja un rastro (logs, metadatos).", "A"), ("B) Los equipos informáticos no dejan huellas físicas.", "B")]
    for t, v in opciones: tk.Radiobutton(card, text=t, variable=var_resp, value=v, bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD).pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡Exacto!")
        else: messagebox.showerror("Error", "Incorrecto.")
    tk.Button(card, text="VERIFICAR", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0).pack(pady=20, ipadx=15, ipady=6)

def cargar_practica_u1_p4(parent):
    for w in parent.winfo_children(): w.destroy()
    card = tk.Frame(parent, bg=COLOR_ENTRY_BG, bd=0)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(card, text="PRÁCTICA 1.4: ESTÁNDARES RFC 3227", font=("Segoe UI", 12, "bold"), bg=COLOR_ENTRY_BG, fg=COLOR_ACCENT).pack(pady=(20, 15))
    tk.Label(card, text="¿Qué se debe recolectar primero según el orden de volatilidad del RFC 3227?", font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT).pack(pady=10)

    var_resp = tk.StringVar()
    opciones = [("A) Memoria RAM y conexiones de red activas.", "A"), ("B) Discos duros y respaldos en cinta.", "B")]
    for t, v in opciones: tk.Radiobutton(card, text=t, variable=var_resp, value=v, bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT, selectcolor=COLOR_CARD).pack(anchor="w", padx=100, pady=5)

    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡Correcto! Lo más volátil se adquiere primero.")
        else: messagebox.showerror("Error", "Incorrecto.")
    tk.Button(card, text="VERIFICAR", command=verificar, bg=COLOR_ACCENT, fg=COLOR_BG_DARK, font=("Segoe UI", 9, "bold"), bd=0).pack(pady=20, ipadx=15, ipady=6)