import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Importamos las vistas desde la carpeta views
from views.admin_view import abrir_panel_admin
from views.teacher_view import abrir_panel_docente
from views.student_view import abrir_panel_alumno

# Ruta absoluta a la base de datos dentro de la carpeta database
DIR_PRINCIPAL = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

# ==========================================
# PALETA DE COLORES "HUD FORENSIC / HIGH-TECH"
# (Ligeramente oscurecida para mayor elegancia y contraste)
# ==========================================
COLOR_BG_DARK = "#05070A"      # Negro abisal
COLOR_CARD = "#090D18"         # Gris naval ultra oscuro
COLOR_ACCENT = "#00F0FF"       # Cian neón principal
COLOR_ACCENT_HOVER = "#00C4D4" # Cian de respuesta hover
COLOR_TEXT_LIGHT = "#FFFFFF"   # Blanco puro (mejor legibilidad)
COLOR_TEXT_MUTED = "#64748B"   # Gris técnico sutil
COLOR_ENTRY_BG = "#0E1524"     # Fondo de entradas más oscuro que la tarjeta
COLOR_BORDER = "#1E293B"       # Borde base de componentes
COLOR_BORDER_FOCUS = "#00F0FF" # Borde activo al enfocar

def verificar_credenciales(usuario, password):
    """Consulta las credenciales en la base de datos de manera segura."""
    if not os.path.exists(RUTA_DB):
        return None
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ? AND password = ?", (usuario, password))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado
    except Exception:
        return None

def intentar_login(event=None):
    """Valida el acceso con animación de salida y abre el panel correspondiente."""
    usuario_ingresado = entry_usuario.get().strip()
    password_ingresada = entry_password.get().strip()

    if not usuario_ingresado or not password_ingresada:
        messagebox.showwarning("Campos vacíos", "Por favor, introduce tu usuario y contraseña de acceso.")
        return

    resultado = verificar_credenciales(usuario_ingresado, password_ingresada)

    if resultado:
        rol = resultado[0]
        # Efecto visual de cierre antes de destruir la ventana
        animar_salida(rol, usuario_ingresado)
    else:
        messagebox.showerror("Acceso Denegado", "Credenciales incorrectas o usuario no registrado en el sistema.")

def animar_salida(rol, usuario):
    """Efecto de desvanecimiento suave antes de cambiar de ventana."""
    alpha = ventana_login.attributes("-alpha")
    if alpha > 0.1:
        alpha -= 0.15
        ventana_login.attributes("-alpha", alpha)
        ventana_login.after(25, lambda: animar_salida(rol, usuario))
    else:
        ventana_login.destroy()
        if rol == 'admin':
            abrir_panel_admin(usuario)
        elif rol == 'docente':
            abrir_panel_docente(usuario)
        elif rol == 'alumno':
            abrir_panel_alumno(usuario)

# ==========================================
# INTERFAZ GRÁFICA DE LOGIN - FULLSCREEN HUD
# ==========================================
ventana_login = tk.Tk()
ventana_login.title("Lab Visual Forense — Secure Access Terminal")
ventana_login.attributes('-fullscreen', True)  # Pantalla completa real
ventana_login.configure(bg=COLOR_BG_DARK)

# Iniciar completamente transparente para aplicar efecto Fade-In fluido
ventana_login.attributes("-alpha", 0.0)

def animar_entrada(alpha=0.0):
    """Efecto de aparición gradual tipo HUD militar/tecnológico."""
    if alpha < 1.0:
        alpha += 0.05
        ventana_login.attributes("-alpha", alpha)
        ventana_login.after(20, lambda: animar_entrada(alpha))

# Contenedor principal flotante (Ajuste de proporciones para verse más estilizado)
card_frame = tk.Frame(
    ventana_login, 
    bg=COLOR_CARD, 
    bd=0, 
    highlightthickness=1, 
    highlightbackground=COLOR_BORDER
)
card_frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=540)

# Encabezado con tipografía técnica (Fuente más grande y llamativa)
lbl_titulo = tk.Label(
    card_frame, 
    text="LAB VISUAL FORENSE", 
    font=("Segoe UI", 22, "bold"), 
    bg=COLOR_CARD, 
    fg=COLOR_TEXT_LIGHT,
    letter=2 if hasattr(tk.Label, 'letter') else None
)
lbl_titulo.pack(pady=(50, 5))

# Subtítulo con efecto de carga progresiva
lbl_sub = tk.Label(
    card_frame, 
    text="", 
    font=("Segoe UI", 9, "bold"), 
    bg=COLOR_CARD, 
    fg=COLOR_ACCENT
)
lbl_sub.pack(pady=(0, 40))

texto_slogan = "SISTEMA INTEGRAL DE INVESTIGACIÓN"
def escribir_slogan(i=0):
    if i <= len(texto_slogan):
        lbl_sub.config(text=texto_slogan[:i])
        ventana_login.after(25, lambda: escribir_slogan(i + 1))

# Función para estilizar inputs con enfoque dinámico y PADDING INTERNO
def crear_input_hud(parent, label_text, is_password=False):
    # Etiqueta del input
    lbl = tk.Label(
        parent, 
        text=label_text, 
        font=("Segoe UI", 8, "bold"), 
        bg=COLOR_CARD, 
        fg=COLOR_TEXT_MUTED, 
        anchor="w"
    )
    lbl.pack(fill="x", padx=45, pady=(10, 5))

    # Marco envolvente para simular borde iluminado al enfocar
    frame_entry = tk.Frame(parent, bg=COLOR_BORDER, bd=0)
    frame_entry.pack(fill="x", padx=45, pady=(0, 10))

    # Marco interno para generar margen (padding) real dentro del input
    inner_frame = tk.Frame(frame_entry, bg=COLOR_ENTRY_BG, bd=0)
    inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

    entry = tk.Entry(
        inner_frame, 
        font=("Segoe UI", 12), 
        bg=COLOR_ENTRY_BG, 
        fg=COLOR_TEXT_LIGHT, 
        insertbackground=COLOR_ACCENT, # Color del cursor parpadeante
        relief="flat", 
        bd=0
    )
    if is_password:
        entry.config(show="●")
    
    # El ipady y pady aquí evitan que el texto se vea pegado a los bordes
    entry.pack(fill="x", padx=12, pady=10)

    # Animación de enfoque (cambio de color de borde Y de texto del label)
    def on_focus_in(e):
        frame_entry.config(bg=COLOR_BORDER_FOCUS)
        lbl.config(fg=COLOR_ACCENT)
    def on_focus_out(e):
        frame_entry.config(bg=COLOR_BORDER)
        lbl.config(fg=COLOR_TEXT_MUTED)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry

entry_usuario = crear_input_hud(card_frame, "IDENTIFICADOR DE USUARIO")
entry_password = crear_input_hud(card_frame, "CLAVE DE ACCESO", is_password=True)

# Botón de Ingreso Principal (Más grueso y con fuente más clara)
btn_entrar = tk.Button(
    card_frame, 
    text="INICIALIZAR SESIÓN", 
    command=intentar_login, 
    font=("Segoe UI", 11, "bold"), 
    bg=COLOR_ACCENT, 
    fg=COLOR_BG_DARK, 
    activebackground=COLOR_ACCENT_HOVER,
    activeforeground=COLOR_BG_DARK,
    relief="flat", 
    cursor="hand2",
    bd=0
)
btn_entrar.pack(fill="x", padx=45, pady=(35, 20), ipady=12)

# Efectos visuales de Hover interactivo
def on_enter(e):
    btn_entrar.config(bg=COLOR_ACCENT_HOVER)
def on_leave(e):
    btn_entrar.config(bg=COLOR_ACCENT)

btn_entrar.bind("<Enter>", on_enter)
btn_entrar.bind("<Leave>", on_leave)

# Atajos de teclado profesionales
ventana_login.bind("<Return>", intentar_login)
ventana_login.bind("<Escape>", lambda e: ventana_login.destroy())  # Salir de pantalla completa con ESC

# Ejecutar animaciones iniciales al cargar la ventana
ventana_login.after(100, animar_entrada)
ventana_login.after(400, escribir_slogan)

ventana_login.mainloop()