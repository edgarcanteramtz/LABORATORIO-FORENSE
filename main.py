import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Importamos las funciones de las vistas que creamos en la carpeta views
from views.admin_view import abrir_panel_admin
from views.teacher_view import abrir_panel_docente
from views.student_view import abrir_panel_alumno

# Ruta absoluta a la base de datos
DIR_PRINCIPAL = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

def verificar_credenciales(usuario, password):
    """Consulta las credenciales en SQLite."""
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario = ? AND password = ?", (usuario, password))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def intentar_login():
    """Valida el acceso y redirige según el rol."""
    usuario_ingresado = entry_usuario.get()
    password_ingresada = entry_password.get()

    resultado = verificar_credenciales(usuario_ingresado, password_ingresada)

    if resultado:
        rol = resultado[0]
        ventana_login.destroy() # Oculta/Destruye la ventana de Login

        # Redirección según el rol
        if rol == 'admin':
            abrir_panel_admin(usuario_ingresado)
        elif rol == 'docente':
            abrir_panel_docente(usuario_ingresado)
        elif rol == 'alumno':
            abrir_panel_alumno(usuario_ingresado)
    else:
        messagebox.showerror("Error de Acceso", "Usuario o contraseña incorrectos.")

# ==========================================
# INTERFAZ GRÁFICA DE LOGIN
# ==========================================
ventana_login = tk.Tk()
ventana_login.title("Lab Visual Forense - Login")
ventana_login.geometry("300x300")
ventana_login.resizable(False, False)

tk.Label(ventana_login, text="Inicio de Sesión", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(ventana_login, text="Nombre de Usuario:").pack()
entry_usuario = tk.Entry(ventana_login, width=25)
entry_usuario.pack(pady=5)

tk.Label(ventana_login, text="Contraseña:").pack()
entry_password = tk.Entry(ventana_login, width=25, show="*")
entry_password.pack(pady=5)

tk.Button(ventana_login, text="Entrar", command=intentar_login, width=15, bg="#4CAF50", fg="white").pack(pady=25)

ventana_login.mainloop()