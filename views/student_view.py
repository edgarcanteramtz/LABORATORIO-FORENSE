import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DB = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

try:
  from tools.hash_calculator import generar_hash_archivo
except ImportError:

  import hashlib

  def generar_hash_archivo(ruta, algoritmo="sha256"):
    hasher = (
        hashlib.md5()
        if algoritmo == "md5"
        else (hashlib.sha1() if algoritmo == "sha1" else hashlib.sha256())
    )
    try:
      with open(ruta, "rb") as f:
        while chunk := f.read(4096):
          hasher.update(chunk)
      return hasher.hexdigest()
    except Exception as e:
      return f"Error: {str(e)}"


def obtener_temas_bd():
  """Consulta los temas en la base de datos."""
  conexion = sqlite3.connect(RUTA_DB)
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, unidad, titulo, contenido_teorico FROM temas ORDER BY unidad"
      " ASC"
  )
  temas = cursor.fetchall()
  conexion.close()
  return temas


def obtener_preguntas_unidad(unidad_id):
  """Obtiene las preguntas asociadas a una unidad temática."""
  conexion = sqlite3.connect(RUTA_DB)
  cursor = conexion.cursor()
  cursor.execute(
      "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,"
      " respuesta_correcta FROM preguntas WHERE tema_id = ?",
      (unidad_id,),
  )
  preguntas = cursor.fetchall()
  conexion.close()
  return preguntas


def guardar_calificacion(usuario, tema_id, puntaje):
  """Registra el puntaje obtenido por el alumno en SQLite."""
  conexion = sqlite3.connect(RUTA_DB)
  cursor = conexion.cursor()

  cursor.execute(
      "SELECT id FROM usuarios WHERE nombre_usuario = ?", (usuario,)
  )
  user = cursor.fetchone()
  if user:
    alumno_id = user[0]
    cursor.execute(
        """
            INSERT INTO calificaciones (alumno_id, tema_id, puntaje)
            VALUES (?, ?, ?)
        """,
        (alumno_id, tema_id, puntaje),
    )
    conexion.commit()
  conexion.close()


def abrir_panel_alumno(usuario):
  """Módulo principal del Alumno con 3 pestañas: Teoría, Hashes y Evaluaciones."""
  ventana = tk.Tk()
  ventana.title(f"LAB VISUAL FORENSE - Módulo Alumno ({usuario})")
  ventana.geometry("780x580")

  pestanas = ttk.Notebook(ventana)
  pestanas.pack(fill="both", expand=True, padx=10, pady=10)

  # -------------------------------------------------------------
  # PESTAÑA 1: TEORÍA
  # -------------------------------------------------------------
  tab_teoria = ttk.Frame(pestanas)
  pestanas.add(tab_teoria, text="📚 Temario y Teoría")

  tk.Label(
      tab_teoria,
      text="Unidades del Análisis Forense Informático",
      font=("Arial", 12, "bold"),
  ).pack(pady=10)

  frame_texto = ttk.Frame(tab_teoria)
  frame_texto.pack(fill="both", expand=True, padx=10, pady=5)

  scroll = ttk.Scrollbar(frame_texto)
  scroll.pack(side="right", fill="y")

  area_teoria = tk.Text(
      frame_texto, yscrollcommand=scroll.set, wrap="word", font=("Arial", 10)
  )
  area_teoria.pack(side="left", fill="both", expand=True)
  scroll.config(command=area_teoria.yview)

  temas = obtener_temas_bd()
  if temas:
    for t_id, unidad, titulo, contenido in temas:
      area_teoria.insert(
          "end", f"=== UNIDAD {unidad}: {titulo} ===\n\n", "titulo"
      )
      area_teoria.insert("end", f"{contenido}\n\n")
      area_teoria.insert("end", "-" * 60 + "\n\n")
  area_teoria.config(state="disabled")

  # -------------------------------------------------------------
  # PESTAÑA 2: PRÁCTICA (CALCULADORA DE HASHES)
  # -------------------------------------------------------------
  tab_hashes = ttk.Frame(pestanas)
  pestanas.add(tab_hashes, text="🛠️ Práctica: Hashes")

  tk.Label(
      tab_hashes,
      text="Verificación de Integridad de Evidencias Digitales",
      font=("Arial", 12, "bold"),
  ).pack(pady=10)

  ruta_archivo_var = tk.StringVar()

  def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de evidencia"
    )
    if archivo:
      ruta_archivo_var.set(archivo)

  def calcular():
    ruta = ruta_archivo_var.get()
    if not ruta:
      messagebox.showwarning(
          "Atención", "Por favor selecciona un archivo primero."
      )
      return
    algoritmo = combo_algo.get().lower()
    hash_res = generar_hash_archivo(ruta, algoritmo)
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, hash_res)

  frame_controles = ttk.Frame(tab_hashes)
  frame_controles.pack(pady=10, fill="x", padx=20)

  ttk.Button(
      frame_controles, text="Buscar Archivo...", command=seleccionar_archivo
  ).grid(row=0, column=0, padx=5)
  ttk.Entry(frame_controles, textvariable=ruta_archivo_var, width=50).grid(
      row=0, column=1, padx=5
  )

  ttk.Label(tab_hashes, text="Algoritmo de Hash:").pack(pady=5)
  combo_algo = ttk.Combobox(
      tab_hashes, values=["SHA256", "MD5", "SHA1"], state="readonly"
  )
  combo_algo.set("SHA256")
  combo_algo.pack()

  ttk.Button(tab_hashes, text="Calcular Hash", command=calcular).pack(pady=15)

  ttk.Label(tab_hashes, text="Resultado Hash:").pack()
  entry_resultado = ttk.Entry(tab_hashes, width=70, font=("Consolas", 9))
  entry_resultado.pack(pady=5)

  # -------------------------------------------------------------
  # PESTAÑA 3: CUESTIONARIOS / EVALUACIONES
  # -------------------------------------------------------------
  tab_eval = ttk.Frame(pestanas)
  pestanas.add(tab_eval, text="📝 Cuestionarios")

  tk.Label(
      tab_eval,
      text="Evaluación Teórica del Temario",
      font=("Arial", 12, "bold"),
  ).pack(pady=10)

  frame_quiz = ttk.Frame(tab_eval)
  frame_quiz.pack(fill="both", expand=True, padx=20, pady=10)

  respuestas_usuario = {}
  preguntas_actuales = []
  tema_seleccionado_id = [None]

  def cargar_cuestionario(event):
    """Muestra las preguntas según la unidad elegida en el ComboBox."""
    for widget in frame_quiz.winfo_children():
      widget.destroy()

    idx = combo_unidades.current()
    if idx == -1:
      return

    tema_actual = temas[idx]
    tema_seleccionado_id[0] = tema_actual[0]
    preguntas_actuales.clear()
    preguntas_actuales.extend(obtener_preguntas_unidad(tema_actual[0]))

    if not preguntas_actuales:
      ttk.Label(
          frame_quiz,
          text="No hay preguntas registradas para esta unidad aún.",
      ).pack(pady=20)
      return

    respuestas_usuario.clear()

    for p_idx, p in enumerate(preguntas_actuales):
      p_id, preg, op_a, op_b, op_c, op_d, resp_correcta = p
      ttk.Label(
          frame_quiz,
          text=f"{p_idx + 1}. {preg}",
          font=("Arial", 10, "bold"),
          wraplength=700,
      ).pack(anchor="w", pady=(10, 5))

      var_resp = tk.StringVar(value="")
      respuestas_usuario[p_id] = var_resp

      opciones = [("A) " + op_a, "A"), ("B) " + op_b, "B"), ("C) " + op_c, "C"), ("D) " + op_d, "D")]
      for txt, val in opciones:
        ttk.Radiobutton(
            frame_quiz, text=txt, value=val, variable=var_resp
        ).pack(anchor="w", padx=20)

    ttk.Button(
        frame_quiz, text="Enviar Cuestionario", command=evaluar_respuestas
    ).pack(pady=20)

  def evaluar_respuestas():
    if not preguntas_actuales:
      return

    correctas = 0
    total = len(preguntas_actuales)

    for p in preguntas_actuales:
      p_id = p[0]
      resp_correcta = p[6]
      if respuestas_usuario.get(p_id, tk.StringVar()).get() == resp_correcta:
        correctas += 1

    puntaje_final = int((correctas / total) * 100)
    guardar_calificacion(usuario, tema_seleccionado_id[0], puntaje_final)

    messagebox.showinfo(
        "Resultado",
        f"Evaluación Finalizada.\nAciertos: {correctas}/{total}\nCalificación:"
        f" {puntaje_final}/100\n\n¡Calificación guardada!",
    )

  ttk.Label(tab_eval, text="Selecciona la Unidad a Evaluar:").pack()
  combo_unidades = ttk.Combobox(
      tab_eval,
      values=[f"Unidad {t[1]}: {t[2]}" for t in temas],
      state="readonly",
      width=50,
  )
  combo_unidades.pack(pady=5)
  combo_unidades.bind("<<ComboboxSelected>>", cargar_cuestionario)

  # Botón inferior
  tk.Button(
      ventana,
      text="Cerrar Sesión",
      command=ventana.destroy,
      bg="#f44336",
      fg="white",
  ).pack(pady=5)

  ventana.mainloop()