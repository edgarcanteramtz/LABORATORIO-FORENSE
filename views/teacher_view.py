import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Ruta absoluta hacia la base de datos
DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

def obtener_conexion():
    return sqlite3.connect(RUTA_DB)

def abrir_panel_docente(usuario):
    """Ventana principal para el rol de Docente."""
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel Docente ({usuario})")
    ventana.geometry("750x500")

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------------------------------------------------
    # PESTAÑA 1: REPORTE DE CALIFICACIONES DE ALUMNOS
    # -------------------------------------------------------------
    tab_notas = ttk.Frame(pestanas)
    pestanas.add(tab_notas, text="📊 Calificaciones de Alumnos")

    tk.Label(tab_notas, text="Historial de Evaluaciones", font=("Arial", 12, "bold")).pack(pady=10)

    # Tabla de datos (Treeview)
    columnas = ("alumno", "unidad", "puntaje", "fecha")
    tabla_notas = ttk.Treeview(tab_notas, columns=columnas, show="headings", height=12)

    tabla_notas.heading("alumno", text="Alumno")
    tabla_notas.heading("unidad", text="Unidad / Tema")
    tabla_notas.heading("puntaje", text="Calificación")
    tabla_notas.heading("fecha", text="Fecha de Realización")

    tabla_notas.column("alumno", width=200)
    tabla_notas.column("unidad", width=250)
    tabla_notas.column("puntaje", width=100, anchor="center")
    tabla_notas.column("fecha", width=150, anchor="center")

    tabla_notas.pack(fill="both", expand=True, padx=10, pady=5)

    def cargar_calificaciones():
        """Obtiene las notas registradas uniendo la tabla de calificaciones, usuarios y temas."""
        for item in tabla_notas.get_children():
            tabla_notas.delete(item)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nombre_completo, t.titulo, c.puntaje, c.fecha
            FROM calificaciones c
            JOIN usuarios u ON c.alumno_id = u.id
            JOIN temas t ON c.tema_id = t.id
            ORDER BY c.fecha DESC
        ''')
        filas = cursor.fetchall()
        conn.close()

        for fila in filas:
            tabla_notas.insert("", "end", values=fila)

    ttk.Button(tab_notas, text="🔄 Actualizar Tabla", command=cargar_calificaciones).pack(pady=10)

    # -------------------------------------------------------------
    # PESTAÑA 2: LISTA DE ALUMNOS REGISTRADOS
    # -------------------------------------------------------------
    tab_alumnos = ttk.Frame(pestanas)
    pestanas.add(tab_alumnos, text="👥 Lista de Alumnos")

    tk.Label(tab_alumnos, text="Alumnos Registrados en el Sistema", font=("Arial", 12, "bold")).pack(pady=10)

    tabla_alumnos = ttk.Treeview(tab_alumnos, columns=("id", "nombre", "usuario"), show="headings", height=12)
    tabla_alumnos.heading("id", text="ID")
    tabla_alumnos.heading("nombre", text="Nombre Completo")
    tabla_alumnos.heading("usuario", text="Nombre de Usuario")

    tabla_alumnos.column("id", width=50, anchor="center")
    tabla_alumnos.column("nombre", width=350)
    tabla_alumnos.column("usuario", width=200)

    tabla_alumnos.pack(fill="both", expand=True, padx=10, pady=5)

    def cargar_alumnos():
        for item in tabla_alumnos.get_children():
            tabla_alumnos.delete(item)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_completo, nombre_usuario FROM usuarios WHERE rol = 'alumno'")
        filas = cursor.fetchall()
        conn.close()

        for fila in filas:
            tabla_alumnos.insert("", "end", values=fila)

    ttk.Button(tab_alumnos, text="🔄 Actualizar Lista", command=cargar_alumnos).pack(pady=10)

    # Cargar datos al abrir
    cargar_calificaciones()
    cargar_alumnos()

    # Botón inferior para cerrar sesión
    tk.Button(ventana, text="Cerrar Sesión", command=ventana.destroy, bg="#f44336", fg="white").pack(pady=5)

    ventana.mainloop()