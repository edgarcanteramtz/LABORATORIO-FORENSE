import tkinter as tk

def abrir_panel_admin(usuario):
    """Abre la ventana principal para el Administrador del sistema."""
    ventana = tk.Tk()
    ventana.title("LAB VISUAL FORENSE - Panel Administrador")
    ventana.geometry("600x400")

    tk.Label(ventana, text=f"Bienvenido Administrador: {usuario}", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(ventana, text="Opciones de Admin: Gestión de usuarios, asignación de grupos y temarios.").pack(pady=10)

    # Botón para cerrar sesión
    tk.Button(ventana, text="Cerrar Sesión", command=ventana.destroy, bg="#f44336", fg="white").pack(pady=20)
    ventana.mainloop()