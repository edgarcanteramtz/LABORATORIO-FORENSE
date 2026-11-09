import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BG_DARK = "#05070A"

def cargar_practica_u3_p1(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 3.1: ANÁLISIS DE METADATOS EXIF", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Qué tipo de información sensible suele encontrarse en los metadatos EXIF de una fotografía digital?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Coordenadas GPS, fecha, hora y modelo de cámara.", "A"), ("B) Las capas de diseño originales de Photoshop.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡Exacto! El EXIF guarda datos geográficos y técnicos del dispositivo.")
        else: messagebox.showerror("Incorrecto", "Incorrecto.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u3_p2(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 3.2: USO DE AUTOPSY Y VOLATILITY", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Para qué se utiliza principalmente el framework Volatility en informática forense?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Análisis forense de volcado de memoria RAM (Live Memory Forensics).", "A"), ("B) Recuperación de particiones formateadas en FAT32.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "Volatility extrae procesos, conexiones y claves desde la RAM.")
        else: messagebox.showerror("Incorrecto", "Para eso se usan herramientas de particionado.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u3_p3(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 3.3: TÉCNICA DE FILE CARVING", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿En qué consiste el 'File Carving' cuando se examina un disco duro?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Recuperar archivos buscando cabeceras y pies (Magic Numbers) sin depender del sistema de archivos.", "A"), ("B) Tallar piezas de hardware con láser.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "Reconoce firmas hexadecimales para rescatar archivos borrados.")
        else: messagebox.showerror("Incorrecto", "Nada que ver con hardware físico.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u3_p4(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 3.4: CONSULTAS SQLITE FORENSE", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Por qué es útil el análisis de bases de datos SQLite en peritajes de smartphones?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Porque aplicaciones como WhatsApp, chats y registros de llamadas almacenan su historial ahí.", "A"), ("B) Porque acelera el procesador del teléfono.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "Las apps móviles usan SQLite masivamente para bases de datos locales.")
        else: messagebox.showerror("Incorrecto", "No afecta la velocidad del procesador.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)