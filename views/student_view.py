import tkinter as tk

def abrir_panel_alumno(usuario):
    """Abre la ventana principal para el Alumno."""
    ventana = tk.Tk()
    ventana.title("LAB VISUAL FORENSE - Panel Alumno")
    ventana.geometry("600x400")

    tk.Label(ventana, text=f"Bienvenido Alumno: {usuario}", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="Opciones de Alumno: Teoría, Cuestionarios, Prácticas y Calculadora de Hashes.").pack(pady=10)

    tk.Button(ventana, text="Cerrar Sesión", command=ventana.destroy, bg="#f44336", fg="white").pack(pady=20)
    ventana.mainloop()