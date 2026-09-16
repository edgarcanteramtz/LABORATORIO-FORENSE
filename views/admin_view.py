import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Calculamos la ruta absoluta hacia la base de datos
DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

def obtener_conexion():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect(RUTA_DB)

def abrir_panel_admin(usuario):
    """Ventana principal del Administrador con pestañas para gestión del sistema."""
    ventana = tk.Tk()
    ventana.title(f"LAB VISUAL FORENSE - Panel Administrador ({usuario})")
    ventana.geometry("750x600")

    # Contenedor de pestañas principal
    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------------------------------------------------
    # PESTAÑA 1: GESTIÓN DE USUARIOS (CREAR ALUMNOS Y DOCENTES)
    # -------------------------------------------------------------
    tab_usuarios = ttk.Frame(pestanas)
    pestanas.add(tab_usuarios, text="👤 Registrar Usuarios")

    tk.Label(tab_usuarios, text="Alta de Nuevos Usuarios", font=("Arial", 12, "bold")).pack(pady=10)

    frame_form_user = ttk.Frame(tab_usuarios)
    frame_form_user.pack(pady=10)

    # Campos de entrada para datos del nuevo usuario
    ttk.Label(frame_form_user, text="Nombre Completo:").grid(row=0, column=0, sticky="e", pady=5)
    entry_nombre = ttk.Entry(frame_form_user, width=35)
    entry_nombre.grid(row=0, column=1, pady=5)

    ttk.Label(frame_form_user, text="Nombre de Usuario:").grid(row=1, column=0, sticky="e", pady=5)
    entry_user = ttk.Entry(frame_form_user, width=35)
    entry_user.grid(row=1, column=1, pady=5)

    ttk.Label(frame_form_user, text="Contraseña:").grid(row=2, column=0, sticky="e", pady=5)
    entry_pass = ttk.Entry(frame_form_user, width=35, show="*")
    entry_pass.grid(row=2, column=1, pady=5)

    ttk.Label(frame_form_user, text="Rol del Usuario:").grid(row=3, column=0, sticky="e", pady=5)
    combo_rol = ttk.Combobox(frame_form_user, values=["alumno", "docente", "admin"], state="readonly", width=32)
    combo_rol.set("alumno")
    combo_rol.grid(row=3, column=1, pady=5)

    def guardar_usuario():
        """Inserta un nuevo usuario en la base de datos."""
        nom = entry_nombre.get().strip()
        usr = entry_user.get().strip()
        pwd = entry_pass.get().strip()
        rol = combo_rol.get()

        if not nom or not usr or not pwd:
            messagebox.showwarning("Atención", "Por favor completa todos los campos.")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre_completo, nombre_usuario, password, rol) VALUES (?, ?, ?, ?)",
                (nom, usr, pwd, rol)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", f"Usuario '{usr}' registrado correctamente como {rol}.")
            # Limpiar campos después de guardar
            entry_nombre.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")

    ttk.Button(tab_usuarios, text="Registrar Usuario", command=guardar_usuario).pack(pady=15)

    # -------------------------------------------------------------
    # PESTAÑA 2: GESTIÓN DEL TEMARIO (AGREGAR TEORÍA)
    # -------------------------------------------------------------
    tab_temario = ttk.Frame(pestanas)
    pestanas.add(tab_temario, text="📚 Agregar Temas")

    tk.Label(tab_temario, text="Añadir Unidades / Temas al Temario", font=("Arial", 12, "bold")).pack(pady=10)

    frame_form_tema = ttk.Frame(tab_temario)
    frame_form_tema.pack(pady=5)

    ttk.Label(frame_form_tema, text="Número de Unidad:").grid(row=0, column=0, sticky="e", pady=5)
    entry_unidad = ttk.Entry(frame_form_tema, width=10)
    entry_unidad.grid(row=0, column=1, sticky="w", pady=5)

    ttk.Label(frame_form_tema, text="Título de la Unidad:").grid(row=1, column=0, sticky="e", pady=5)
    entry_titulo_tema = ttk.Entry(frame_form_tema, width=45)
    entry_titulo_tema.grid(row=1, column=1, pady=5)

    ttk.Label(tab_temario, text="Contenido Teórico / Subtemas:").pack(pady=5)
    text_contenido_tema = tk.Text(tab_temario, height=8, width=65, font=("Arial", 9))
    text_contenido_tema.pack()

    def guardar_tema():
        """Guarda un nuevo tema o unidad en la tabla 'temas'."""
        num_u = entry_unidad.get().strip()
        tit = entry_titulo_tema.get().strip()
        cont = text_contenido_tema.get("1.0", tk.END).strip()

        if not num_u.isdigit() or not tit or not cont:
            messagebox.showwarning("Atención", "Ingresa un número válidode unidad, título y contenido.")
            return

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO temas (unidad, titulo, contenido_teorico) VALUES (?, ?, ?)",
            (int(num_u), tit, cont)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Unidad {num_u} agregada correctamente.")
        entry_unidad.delete(0, tk.END)
        entry_titulo_tema.delete(0, tk.END)
        text_contenido_tema.delete("1.0", tk.END)
        actualizar_combo_temas() # Actualizar la lista en la pestaña de preguntas

    ttk.Button(tab_temario, text="Guardar Unidad", command=guardar_tema).pack(pady=10)

    # -------------------------------------------------------------
    # PESTAÑA 3: GESTIÓN DE PREGUNTAS
    # -------------------------------------------------------------
    tab_preguntas = ttk.Frame(pestanas)
    pestanas.add(tab_preguntas, text="📝 Agregar Preguntas")

    tk.Label(tab_preguntas, text="Crear Preguntas de Opción Múltiple", font=("Arial", 12, "bold")).pack(pady=10)

    ttk.Label(tab_preguntas, text="Seleccionar Unidad / Tema:").pack()
    combo_temas_preg = ttk.Combobox(tab_preguntas, state="readonly", width=50)
    combo_temas_preg.pack(pady=5)

    lista_temas_ids = []

    def actualizar_combo_temas():
        """Carga las unidades registradas para asociarle preguntas."""
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, unidad, titulo FROM temas ORDER BY unidad ASC")
        filas = cursor.fetchall()
        conn.close()

        lista_temas_ids.clear()
        opciones = []
        for f_id, u, t in filas:
            lista_temas_ids.append(f_id)
            opciones.append(f"Unidad {u}: {t}")

        combo_temas_preg["values"] = opciones
        if opciones:
            combo_temas_preg.current(0)

    frame_form_preg = ttk.Frame(tab_preguntas)
    frame_form_preg.pack(pady=5)

    ttk.Label(frame_form_preg, text="Pregunta:").grid(row=0, column=0, sticky="e", pady=3)
    entry_preg = ttk.Entry(frame_form_preg, width=50)
    entry_preg.grid(row=0, column=1, pady=3)

    ttk.Label(frame_form_preg, text="Opción A:").grid(row=1, column=0, sticky="e", pady=3)
    entry_op_a = ttk.Entry(frame_form_preg, width=50)
    entry_op_a.grid(row=1, column=1, pady=3)

    ttk.Label(frame_form_preg, text="Opción B:").grid(row=2, column=0, sticky="e", pady=3)
    entry_op_b = ttk.Entry(frame_form_preg, width=50)
    entry_op_b.grid(row=2, column=1, pady=3)

    ttk.Label(frame_form_preg, text="Opción C:").grid(row=3, column=0, sticky="e", pady=3)
    entry_op_c = ttk.Entry(frame_form_preg, width=50)
    entry_op_c.grid(row=3, column=1, pady=3)

    ttk.Label(frame_form_preg, text="Opción D:").grid(row=4, column=0, sticky="e", pady=3)
    entry_op_d = ttk.Entry(frame_form_preg, width=50)
    entry_op_d.grid(row=4, column=1, pady=3)

    ttk.Label(frame_form_preg, text="Respuesta Correcta:").grid(row=5, column=0, sticky="e", pady=3)
    combo_correcta = ttk.Combobox(frame_form_preg, values=["A", "B", "C", "D"], state="readonly", width=10)
    combo_correcta.set("A")
    combo_correcta.grid(row=5, column=1, sticky="w", pady=3)

    def guardar_pregunta():
        """Inserta la pregunta en la base de datos."""
        idx = combo_temas_preg.current()
        if idx == -1 or not lista_temas_ids:
            messagebox.showwarning("Atención", "Selecciona un tema primero.")
            return

        tema_id = lista_temas_ids[idx]
        p = entry_preg.get().strip()
        a = entry_op_a.get().strip()
        b = entry_op_b.get().strip()
        c = entry_op_c.get().strip()
        d = entry_op_d.get().strip()
        rc = combo_correcta.get()

        if not p or not a or not b or not c or not d:
            messagebox.showwarning("Atención", "Completa la pregunta y todas las opciones.")
            return

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (tema_id, p, a, b, c, d, rc)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Pregunta registrada correctamente.")
        entry_preg.delete(0, tk.END)
        entry_op_a.delete(0, tk.END)
        entry_op_b.delete(0, tk.END)
        entry_op_c.delete(0, tk.END)
        entry_op_d.delete(0, tk.END)

    ttk.Button(tab_preguntas, text="Guardar Pregunta", command=guardar_pregunta).pack(pady=10)

    # Inicializar menú desplegable de temas
    actualizar_combo_temas()

    # Botón inferior
    tk.Button(ventana, text="Cerrar Sesión", command=ventana.destroy, bg="#f44336", fg="white").pack(pady=5)

    ventana.mainloop()