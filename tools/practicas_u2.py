import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BG_DARK = "#05070A"

def cargar_practica_u2_p1(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    
    ctk.CTkLabel(card, text="PRÁCTICA 2.1: IDENTIFICACIÓN DE EQUIPOS EN VIVO", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Qué tipo de soporte requiere adquisición de memoria RAM en vivo antes del apagado?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Un servidor encendido ejecutando transacciones activas.", "A"), ("B) Un disco duro guardado en una bolsa antiestática.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡Exacto! Los servidores encendidos retienen procesos en RAM.")
        else: messagebox.showerror("Incorrecto", "Ese equipo no tiene energía.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u2_p2(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 2.2: BLOQUEO DE ESCRITURA", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Para qué sirve un bloqueador de escritura físico o por software?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Para impedir cualquier alteración o modificación al medio original durante la lectura.", "A"), ("B) Para acelerar la velocidad de internet.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "Garantiza la integridad jurídica de la prueba.")
        else: messagebox.showerror("Incorrecto", "No tiene relación con internet.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u2_p3(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 2.3: CREACIÓN DE IMAGEN FORENSE", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="¿Cuál es el formato estándar comúnmente utilizado para almacenar imágenes forenses bit a bit?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) Formato .RAW / .DD o .E01 (Expert Witness Format)", "A"), ("B) Formato .docx o .xlsx", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "¡Exacto! .RAW y .E01 son los formatos estándar en peritaje.")
        else: messagebox.showerror("Incorrecto", "Esos son documentos de ofimática.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)

def cargar_practica_u2_p4(parent):
    for w in parent.winfo_children(): w.destroy()
    card = ctk.CTkFrame(parent, fg_color=COLOR_ENTRY_BG, corner_radius=10)
    card.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(card, text="PRÁCTICA 2.4: VERIFICACIÓN DE HASH", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 15))
    ctk.CTkLabel(card, text="Si el Hash SHA-256 de la evidencia original difiere del hash de la copia forense, ¿qué significa?", font=ctk.CTkFont("Segoe UI", 11), text_color=COLOR_TEXT_LIGHT).pack(pady=10)
    
    var_resp = tk.StringVar()
    opciones = [("A) La copia está corrompida o fue alterada; no es íntegra.", "A"), ("B) La copia fue exitosa y perfecta.", "B")]
    for t, v in opciones: ctk.CTkRadioButton(card, text=t, variable=var_resp, value=v, fg_color=COLOR_ACCENT, text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=80, pady=5)
    
    def verificar():
        if var_resp.get() == "A": messagebox.showinfo("Correcto", "El cambio de hash invalida la prueba por pérdida de integridad.")
        else: messagebox.showerror("Incorrecto", "Los hashes deben ser idénticos.")
    ctk.CTkButton(card, text="VALIDAR", command=verificar, fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK).pack(pady=20)