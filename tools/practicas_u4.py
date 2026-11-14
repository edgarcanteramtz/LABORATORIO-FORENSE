import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BG_DARK = "#05070A"

def cargar_practica_u4_p1(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 4.1: RESPUESTA A INCIDENTES Y TRIAGE", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="Ante un ataque activo de Ransomware en red corporativa, ¿cuál es la prioridad inmediata?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Aislar lógicamente los equipos afectados de la red para frenar el cifrado lateral.", "A"), ("B) Apagar todos los routers de la empresa y vaciar la papelera.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "El aislamiento frena la propagación del ransomware.")
        else: messagebox.showerror("Incorrecto", "Apagar routers sin protocolo puede empeorar el incidente.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u4_p2(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 4.2: ANÁLISIS DE EVENT LOGS", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Qué Event ID de Windows indica la creación exitosa de una nueva cuenta de usuario (posible backdoor)?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Event ID 4720", "A"), ("B) Event ID 7001", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡El ID 4720 registra la creación de usuarios!")
        else: messagebox.showerror("Incorrecto", "Ese ID corresponde a otro evento.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u4_p3(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 4.3: CONSTRUCCIÓN DE LÍNEA DE TIEMPO", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Para qué sirve ordenar cronológicamente los artefactos en una investigación forense?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Para reconstruir paso a paso la secuencia exacta de cómo ocurrió el ataque.", "A"), ("B) Para ordenar alfabéticamente los archivos del disco.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "Permite entender el vector de entrada y la línea temporal de intrusión.")
        else: messagebox.showerror("Incorrecto", "No tiene relación con orden alfabético.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u4_p4(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 4.4: ATRIBUCIÓN E INDICADORES (IOC)", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Cuál de los siguientes elementos representa un Indicador de Compromiso (IoC) técnico?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Una firma Hash SHA-256 de un binario troyano o IP maliciosa.", "A"), ("B) El color del gabinete del servidor afectado.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡Exacto! Hashes e IPs maliciosas son IoCs clave para la atribución.")
        else: messagebox.showerror("Incorrecto", "Eso es un dato físico irrelevante.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)