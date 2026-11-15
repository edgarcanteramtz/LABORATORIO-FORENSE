import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

class HashSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Práctica 2.2 - Simulador de Hashing Forense")
        self.root.geometry("600x400")
        
        self.texto_evidencia = "Archivo de evidencia digital: disco_clonado.img\nTamaño: 1024 MB\nContenido: Binario del disco"
        self.hash_original = self.calcular_hash(self.texto_evidencia)
        
        self.crear_ui()

    def calcular_hash(self, texto):
        return hashlib.sha256(texto.encode()).hexdigest()

    def crear_ui(self):
        lbl_instruccion = tk.Label(self.root, text="Analiza la evidencia y verifica su integridad (SHA-256)", font=("Helvetica", 12, "bold"))
        lbl_instruccion.pack(pady=10)

        # Área de evidencia (Simulación de un editor hexadecimal/visor)
        self.txt_evidencia = tk.Text(self.root, height=5, width=60)
        self.txt_evidencia.pack(pady=10)
        self.txt_evidencia.insert(tk.END, self.texto_evidencia)

        # Botón para calcular Hash
        btn_calcular = tk.Button(self.root, text="Calcular Hash SHA-256", command=self.verificar_integridad, bg="darkgreen", fg="white")
        btn_calcular.pack(pady=10)

        # Panel de resultados
        self.lbl_resultado = tk.Label(self.root, text=f"Hash Original (Registrado en Cadena de Custodia):\n{self.hash_original}", fg="blue")
        self.lbl_resultado.pack(pady=10)
        
        self.lbl_hash_actual = tk.Label(self.root, text="", font=("Helvetica", 10, "bold"))
        self.lbl_hash_actual.pack(pady=5)

    def verificar_integridad(self):
        contenido_actual = self.txt_evidencia.get("1.0", tk.END).strip()
        hash_actual = self.calcular_hash(contenido_actual)
        
        self.lbl_hash_actual.config(text=f"Hash Calculado: {hash_actual}")
        
        if hash_actual == self.hash_original:
            messagebox.showinfo("Integridad Verificada", "¡Excelente! Los hashes coinciden. La evidencia no ha sido alterada.")
            self.lbl_hash_actual.config(fg="green")
        else:
            messagebox.showerror("Alerta de Integridad", "PELIGRO: Los hashes no coinciden. La evidencia ha sido alterada y no será admisible en un tribunal.")
            self.lbl_hash_actual.config(fg="red")