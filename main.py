import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Importar las funciones de tu archivo db_manager
from database.db_manager import inicializar_base_datos, cargar_datos_iniciales, DB_PATH

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


def aplicar_hover(boton, color_normal, color_hover):
    boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
    boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))


# ==========================================
# LÓGICA DE AUTENTICACIÓN
# ==========================================
def iniciar_sesion():
    usuario = entry_usuario.get().strip()
    clave = entry_clave.get().strip()

    if not usuario or not clave:
        messagebox.showwarning("Acceso Denegado", "Por favor, ingresa tu usuario y contraseña.")
        return

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    # Verifica credenciales usando la columna "password"
    cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ? AND password = ?", (usuario, clave))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        rol = resultado[0]
        ventana_login.destroy()  # Cierra la ventana de login

        # Enrutamiento según el rol
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
        messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")


# ==========================================
# PREPARAR BASE DE DATOS Y ARRANCAR APP
# ==========================================
# 1. Asegurar que las tablas existan
inicializar_base_datos()
# 2. Cargar los usuarios (admin, docente1, alumno1) y el temario
cargar_datos_iniciales()

# Crear ventana principal
ventana_login = tk.Tk()
ventana_login.title("LAB VISUAL FORENSE - Iniciar Sesión")
ventana_login.geometry("500x600")
ventana_login.configure(bg=COLOR_BG_DARK)
ventana_login.resizable(False, False)

# Centrar la ventana
ventana_login.update_idletasks()
x = (ventana_login.winfo_screenwidth() // 2) - (500 // 2)
y = (ventana_login.winfo_screenheight() // 2) - (600 // 2)
ventana_login.geometry(f"500x600+{x}+{y}")

# Contenedor central
card = tk.Frame(ventana_login, bg=COLOR_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1)
card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)

# Textos
tk.Label(card, text="LAB VISUAL FORENSE", font=("Segoe UI", 18, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT).pack(
    pady=(40, 10))
tk.Label(card, text="Acceso al sistema", font=("Segoe UI", 11), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(pady=(0, 30))

# Entrada Usuario
tk.Label(card, text="USUARIO", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(anchor="w",
                                                                                                      padx=40,
                                                                                                      pady=(0, 5))
entry_usuario = tk.Entry(card, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT,
                         insertbackground=COLOR_ACCENT, bd=0, relief="flat")
entry_usuario.pack(fill="x", padx=40, pady=(0, 20), ipady=8)

# Entrada Contraseña
tk.Label(card, text="CONTRASEÑA", font=("Segoe UI", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT).pack(anchor="w",
                                                                                                         padx=40,
                                                                                                         pady=(0, 5))
entry_clave = tk.Entry(card, font=("Segoe UI", 11), bg=COLOR_ENTRY_BG, fg=COLOR_TEXT_LIGHT,
                       insertbackground=COLOR_ACCENT, bd=0, relief="flat", show="*")
entry_clave.pack(fill="x", padx=40, pady=(0, 30), ipady=8)

# Botón Ingresar
btn_ingresar = tk.Button(card, text="INICIAR SESIÓN", command=iniciar_sesion, font=("Segoe UI", 11, "bold"),
                         bg=COLOR_ACCENT, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER,
                         activeforeground=COLOR_BG_DARK, relief="flat", cursor="hand2", bd=0)
btn_ingresar.pack(fill="x", padx=40, ipady=10)
aplicar_hover(btn_ingresar, COLOR_ACCENT, COLOR_ACCENT_HOVER)

ventana_login.bind('<Return>', lambda event: iniciar_sesion())
ventana_login.mainloop()