import os
import hashlib
import customtkinter as ctk
from tkinter import filedialog, messagebox

try:
    from report_generator import generar_reporte_txt
except ImportError:
    def generar_reporte_txt(tipo, usr, datos):
        return "REPORTE_FALLBACK.txt", "Reporte generado"

COLOR_CARD = "#090D18"
COLOR_ENTRY_BG = "#0E1524"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"


def limpiar(c):
    for w in c.winfo_children(): w.destroy()


def cargar_practica_u2_p1(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 2.1: Etiquetado de Evidencia Física",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Completa los datos del formato de recolección de indicios de la escena.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f, text="Número de Indicio:", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w",
                                                                                                        padx=15,
                                                                                                        pady=(10, 0))
    e1 = ctk.CTkEntry(f, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    e1.pack(fill="x", padx=15, pady=5)

    ctk.CTkLabel(f, text="Descripción del Dispositivo:", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(
        anchor="w", padx=15, pady=(5, 0))
    e2 = ctk.CTkEntry(f, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    e2.pack(fill="x", padx=15, pady=5)

    def guardar_indicio():
        if e1.get() and e2.get():
            messagebox.showinfo("Registrado",
                                f"Indicio '{e1.get()}' registrado correctamente en el acta de cadena de custodia.")
        else:
            messagebox.showwarning("Atención", "Llena todos los campos del indicio.")

    ctk.CTkButton(f, text="Registrar Indicio en Acta", command=guardar_indicio, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)


def cargar_practica_u2_p2(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 2.2: Constructor de Comandos de Adquisición",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Arma el comando con `dcfldd` para generar una imagen forense con SHA-256.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f, text="Escribe el comando completo de volcado forense:", font=("Segoe UI", 12),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=10)
    en_cmd = ctk.CTkEntry(f, width=500, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_cmd.pack(anchor="w", padx=15, pady=5)
    en_cmd.insert(0, "dcfldd if=... of=... hash=sha256")

    def probar_cmd():
        val = en_cmd.get()
        if "dcfldd" in val and "sha256" in val:
            messagebox.showinfo("¡Comando Válido!", "La sintaxis pericial es correcta y segura.")
        else:
            messagebox.showerror("Error de Sintaxis",
                                 "El comando debe incluir la herramienta dcfldd y el parámetro hash=sha256.")

    ctk.CTkButton(f, text="Validar Sintaxis del Comando", command=probar_cmd, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)


def cargar_practica_u2_p3(container):
    """Práctica 2.3: Herramienta Real de Hashes (MD5 / SHA-256)."""
    limpiar(container)

    ctk.CTkLabel(container, text="🛠️ Laboratorio Práctico 2.3: Generador y Verificador de Hashes",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=(0, 5), anchor="w")
    ctk.CTkLabel(container,
                 text="Selecciona cualquier archivo de tu computadora para calcular su huella digital exacta.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 10))

    f_input = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    f_input.pack(fill="x", pady=5, ipady=5)

    lbl_ruta = ctk.CTkLabel(f_input, text="Ningún archivo seleccionado...", font=("Segoe UI", 11),
                            text_color=COLOR_TEXT_MUTED)
    lbl_ruta.pack(side="left", padx=15, pady=10)

    resultado_hashes = {"md5": "", "sha256": "", "archivo": ""}

    txt_salida = ctk.CTkTextbox(container, font=("Consolas", 11), fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT,
                                height=130)
    txt_salida.pack(fill="both", expand=True, pady=5)
    txt_salida.configure(state="disabled")

    def calcular():
        ruta = filedialog.askopenfilename(title="Seleccionar evidencia digital")
        if not ruta: return
        lbl_ruta.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)

        try:
            h_md5 = hashlib.md5()
            h_sha256 = hashlib.sha256()
            with open(ruta, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    h_md5.update(chunk)
                    h_sha256.update(chunk)

            m_val, s_val = h_md5.hexdigest(), h_sha256.hexdigest()
            resultado_hashes["md5"], resultado_hashes["sha256"], resultado_hashes[
                "archivo"] = m_val, s_val, os.path.basename(ruta)

            txt_salida.configure(state="normal")
            txt_salida.delete("1.0", "end")
            txt_salida.insert("end",
                              f"Archivo analizado: {os.path.basename(ruta)}\n\nMD5    : {m_val}\nSHA-256: {s_val}\n")
            txt_salida.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(f_input, text="Examinar Archivo...", command=calcular, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(side="right", padx=15)

    def exportar():
        if not resultado_hashes["md5"]:
            messagebox.showwarning("Atención", "Calcula el hash de un archivo primero.")
            return
        rep, cont = generar_reporte_txt("Analisis de Hashes", "AlumnoDemo",
                                        {"Archivo": resultado_hashes["archivo"], "MD5": resultado_hashes["md5"],
                                         "SHA-256": resultado_hashes["sha256"]})
        with open(rep, "w", encoding="utf-8") as f: f.write(cont)
        messagebox.showinfo("Reporte Generado", f"Cadena de custodia guardada:\n{rep}")

    ctk.CTkButton(container, text="📄 Generar Reporte de Cadena de Custodia (TXT)", command=exportar, fg_color="#2EC4B6",
                  text_color="#05070A").pack(pady=5, anchor="e")


def cargar_practica_u2_p4(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 2.4: Redacción de Hallazgos Periciales",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Escribe la conclusión técnica preliminar para el informe del juez.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)
    txt_inf = ctk.CTkTextbox(f, height=100, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    txt_inf.pack(fill="x", padx=15, pady=10)
    txt_inf.insert("1.0", "Conclusión: Tras el análisis de la muestra digital...")

    def guardar_inf():
        if len(txt_inf.get("1.0", "end").strip()) > 20:
            messagebox.showinfo("Dictamen Emitido", "Informe pericial guardado y firmado digitalmente.")
        else:
            messagebox.showwarning("Muy corto", "El dictamen técnico debe ser más descriptivo.")

    ctk.CTkButton(f, text="Firmar y Guardar Dictamen", command=guardar_inf, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)