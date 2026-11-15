import tkinter as tk
from tkinter import messagebox

class WindowsLogsSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Práctica 4.2 - Análisis de Registros de Eventos de Windows")
        self.root.geometry("700x550")
        self.crear_ui()

    def crear_ui(self):
        lbl_titulo = tk.Label(self.root, text="Investigación Forense: Visor de Eventos (Security.evtx)", font=("Helvetica", 12, "bold"))
        lbl_titulo.pack(pady=10)

        instruccion = (
            "Analiza el fragmento de registros de eventos extraídos de la máquina comprometida.\n"
            "Tu objetivo es identificar el Event ID clave que revela la alteración de la seguridad o persistencia del atacante."
        )
        lbl_instrucciones = tk.Label(self.root, text=instruccion, justify="left", wraplength=650)
        lbl_instrucciones.pack(pady=5)

        # Área de texto simulando logs forenses
        self.txt_logs = tk.Text(self.root, height=10, width=80)
        self.txt_logs.pack(pady=10)
        
        logs_simulados = (
            "[10:12:04] Event ID: 4624 - An account was successfully logged on. User: SYSTEM\n"
            "[10:15:22] Event ID: 4625 - An account failed to log on. User: Administrator (Password incorrect)\n"
            "[10:15:28] Event ID: 4625 - An account failed to log on. User: Administrator (Password incorrect)\n"
            "[10:20:01] Event ID: 4720 - A user account was created. TargetAccount: 'backdoor_admin'\n"
            "[10:25:40] Event ID: 4672 - Special privileges assigned to new logon. User: backdoor_admin\n"
        )
        self.txt_logs.insert(tk.END, logs_simulados)
        self.txt_logs.config(state="disabled") # Bloqueado para simular solo lectura pericial

        # Opciones de respuesta múltiple para el diagnóstico
        lbl_pregunta = tk.Label(self.root, text="¿Cuál es el Event ID crítico que evidencia la creación de una cuenta no autorizada?", font=("Helvetica", 10, "bold"))
        lbl_pregunta.pack(pady=5)

        self.var_respuesta = tk.StringVar(value="")
        
        opciones = [
            ("4624 - Inicio de sesión exitoso", "4624"),
            ("4625 - Fallo de inicio de sesión masivo", "4625"),
            ("4720 - Creación de una cuenta de usuario", "4720"),
            ("4672 - Asignación de privilegios especiales", "4672")
        ]

        for texto, val in opciones:
            rb = tk.Radiobutton(self.root, text=texto, variable=self.var_respuesta, value=val)
            rb.pack(anchor="w", padx=60)

        btn_verificar = tk.Button(self.root, text="Verificar Hallazgo", bg="darkblue", fg="white", command=self.verificar)
        btn_verificar.pack(pady=15)

    def verificar(self):
        seleccion = self.var_respuesta.get()
        if seleccion == "4720":
            messagebox.showinfo("¡Correcto!", "¡Excelente análisis forense! El Event ID 4720 confirma que se creó la cuenta 'backdoor_admin', evidenciando el mecanismo de persistencia del atacante.")
            self.root.destroy()
        elif seleccion == "":
            messagebox.showwarning("Atención", "Por favor selecciona una opción de la lista.")
        else:
            messagebox.showerror("Incorrecto", "Ese evento muestra actividad del sistema o fuerza bruta, pero no es el indicador principal de la creación de la cuenta maliciosa.")