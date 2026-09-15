import tkinter as tk

def abrir_panel_docente(usuario):
    """Abre la ventana principal para el Docente."""
    ventana = tk.Tk()
    ventana.title("LAB VISUAL FORENSE - Panel Docente")
    ventana.geometry("600x400")

    tk.Label(ventana, text=f"Bienvenido Profesor: {usuario}", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="Opciones de Docente: Consulta de grupos, alumnos y evaluaciones.").pack(pady=10)

    tk.Button(ventana, text="Cerrar Sesión", command=ventana.destroy, bg="#f44336", fg="white").pack(pady=20)
    ventana.mainloop()