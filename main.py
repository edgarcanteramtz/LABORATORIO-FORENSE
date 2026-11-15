import os
import time
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Importar las funciones de tu archivo db_manager
from database.db_manager import inicializar_base_datos, cargar_datos_iniciales, DB_PATH

# ==========================================
# CONFIGURACIÓN DE CUSTOMTKINTER
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# PALETA DE COLORES
# ==========================================
COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_ACCENT_HOVER = "#00C4D4"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#64748B"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BORDER = "#1E293B"

# ==========================================
# BARRA DE TÍTULO PERSONALIZADA
# ==========================================
def crear_barra_titulo(ventana, bg_color):
    barra_titulo = ctk.CTkFrame(ventana, height=35, fg_color=bg_color, corner_radius=0)
    barra_titulo.pack(side="top", fill="x")
    barra_titulo.pack_propagate(False)

    # Botón Cerrar (✕)
    btn_cerrar = ctk.CTkButton(barra_titulo, text="✕", font=("Segoe UI", 14), width=45, height=35, 
                               fg_color="transparent", hover_color="#E81123", text_color="white", 
                               corner_radius=0, command=ventana.quit)
    btn_cerrar.pack(side="right")

    # Botón Maximizar/Restaurar (🗗)
    def toggle_maximizar():
        es_fullscreen = ventana.attributes('-fullscreen')
        ventana.attributes('-fullscreen', not es_fullscreen)
        
    btn_max = ctk.CTkButton(barra_titulo, text="🗗", font=("Segoe UI", 15), width=45, height=35, 
                            fg_color="transparent", hover_color=COLOR_BORDER, text_color="white", 
                            corner_radius=0, command=toggle_maximizar)
    btn_max.pack(side="right")

    # Botón Minimizar (—)
    btn_min = ctk.CTkButton(barra_titulo, text="—", font=("Segoe UI", 15, "bold"), width=45, height=35, 
                            fg_color="transparent", hover_color=COLOR_BORDER, text_color="white", 
                            corner_radius=0, command=ventana.iconify)
    btn_min.pack(side="right")

# ==========================================
# LÓGICA DE AUTENTICACIÓN
# ==========================================
def iniciar_sesion(event=None):
    usuario = entry_usuario.get().strip()
    clave = entry_clave.get().strip()

    if not usuario or not clave:
        messagebox.showwarning("Acceso Denegado", "Por favor, ingresa tu usuario y contraseña.")
        return

    progress_bar.set(0)
    progress_bar.grid(row=5, column=0, pady=(15, 0), sticky="ew", padx=40)
    ventana_login.update_idletasks()
    
    for i in range(1, 11):
        progress_bar.set(i / 10)
        ventana_login.update_idletasks()
        time.sleep(0.03)

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ? AND password = ?", (usuario, clave))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        rol = resultado[0]
        ventana_login.withdraw() 

        if rol == "admin":
            from views.admin_view import abrir_panel_admin
            abrir_panel_admin(usuario)
        elif rol == "docente":
            from views.teacher_view import abrir_panel_docente
            abrir_panel_docente(usuario)
        elif rol == "alumno":
            from views.student_view import abrir_panel_alumno
            abrir_panel_alumno(usuario)
    else:
        progress_bar.grid_remove()
        messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")


# ==========================================
# PREPARAR BASE DE DATOS Y ARRANCAR APP
# ==========================================
inicializar_base_datos()
cargar_datos_iniciales()

ventana_login = ctk.CTk()
ventana_login.title("LAB VISUAL FORENSE - Iniciar Sesión")
ventana_login.configure(fg_color=COLOR_BG_DARK)
ventana_login.attributes('-fullscreen', True)

# --- INSTANCIAR LA BARRA DE TÍTULO ---
crear_barra_titulo(ventana_login, COLOR_CARD)

# ==========================================
# INTERFAZ GRÁFICA (LOGIN)
# ==========================================
card = ctk.CTkFrame(ventana_login, width=400, height=450, fg_color=COLOR_CARD, border_color=COLOR_BORDER, border_width=1, corner_radius=15)
card.place(relx=0.5, rely=0.5, anchor="center")
card.grid_propagate(False)
card.grid_columnconfigure(0, weight=1)

titulo = ctk.CTkLabel(card, text="LAB VISUAL FORENSE", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=COLOR_ACCENT)
titulo.grid(row=0, column=0, pady=(40, 5))

subtitulo = ctk.CTkLabel(card, text="Acceso al sistema", font=ctk.CTkFont(family="Segoe UI", size=13), text_color=COLOR_TEXT_MUTED)
subtitulo.grid(row=1, column=0, pady=(0, 30))

entry_usuario = ctk.CTkEntry(card, placeholder_text="Usuario", font=ctk.CTkFont(family="Segoe UI", size=13), 
                             fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER, height=45, corner_radius=8)
entry_usuario.grid(row=2, column=0, sticky="ew", padx=40, pady=(0, 20))

entry_clave = ctk.CTkEntry(card, placeholder_text="Contraseña", show="*", font=ctk.CTkFont(family="Segoe UI", size=13), 
                           fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER, height=45, corner_radius=8)
entry_clave.grid(row=3, column=0, sticky="ew", padx=40, pady=(0, 30))

btn_ingresar = ctk.CTkButton(card, text="INICIAR SESIÓN", command=iniciar_sesion, font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                             fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK, hover_color=COLOR_ACCENT_HOVER, height=45, corner_radius=8, cursor="hand2")
btn_ingresar.grid(row=4, column=0, sticky="ew", padx=40)

progress_bar = ctk.CTkProgressBar(card, orientation="horizontal", progress_color=COLOR_ACCENT, fg_color=COLOR_ENTRY_BG, height=8)
progress_bar.set(0)

ventana_login.bind('<Return>', iniciar_sesion)
ventana_login.mainloop()
