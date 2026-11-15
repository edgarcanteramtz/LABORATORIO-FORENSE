import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

try:
    from exif_extractor import extraer_metadatos_imagen
except ImportError:
    def extraer_metadatos_imagen(ruta):
        return {"Error": "Módulo exif_extractor no disponible"}

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


def cargar_practica_u3_p1(container):
    """Práctica 3.1: Extractor Real de Metadatos EXIF (Ya reparado)."""
    limpiar(container)

    ctk.CTkLabel(container, text="🛠️ Laboratorio Práctico 3.1: Cazador de Metadatos (ExifTool / Pillow)",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=(0, 5), anchor="w")
    ctk.CTkLabel(container,
                 text="Selecciona cualquier imagen (.jpg, .png) para extraer sus metadatos internos y geolocalización.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=(0, 10))

    f_input = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    f_input.pack(fill="x", pady=5, ipady=5)

    lbl_ruta = ctk.CTkLabel(f_input, text="Selecciona una imagen...", font=("Segoe UI", 11),
                            text_color=COLOR_TEXT_MUTED)
    lbl_ruta.pack(side="left", padx=15, pady=10)

    datos_ultimos = {"metadatos": {}, "ruta": ""}

    txt_salida = ctk.CTkTextbox(container, font=("Consolas", 11), fg_color=COLOR_CARD, text_color=COLOR_TEXT_LIGHT,
                                height=140)
    txt_salida.pack(fill="both", expand=True, pady=5)
    txt_salida.configure(state="disabled")

    def examinar():
        ruta = filedialog.askopenfilename(title="Seleccionar imagen",
                                          filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.tiff *.bmp *.webp")])
        if not ruta: return
        lbl_ruta.configure(text=ruta, text_color=COLOR_TEXT_LIGHT)
        datos_ultimos["ruta"] = ruta

        meta = extraer_metadatos_imagen(ruta)
        datos_ultimos["metadatos"] = meta

        txt_salida.configure(state="normal")
        txt_salida.delete("1.0", "end")
        if isinstance(meta, dict):
            for k, v in meta.items():
                if isinstance(v, dict):
                    txt_salida.insert("end", f"\n[{k}]\n")
                    for sk, sv in v.items(): txt_salida.insert("end", f"  * {sk:<24}: {sv}\n")
                else:
                    txt_salida.insert("end", f"{k:<22}: {v}\n")
        else:
            txt_salida.insert("end", str(meta))
        txt_salida.configure(state="disabled")

    ctk.CTkButton(f_input, text="Examinar Imagen...", command=examinar, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(side="right", padx=15)

    def exportar():
        if not datos_ultimos["metadatos"]:
            messagebox.showwarning("Atención", "Analiza una imagen primero.")
            return
        rep, cont = generar_reporte_txt("Analisis EXIF", "AlumnoDemo", datos_ultimos["metadatos"])
        with open(rep, "w", encoding="utf-8") as f: f.write(cont)
        messagebox.showinfo("Reporte Generado", f"Reporte técnico guardado:\n{rep}")

    ctk.CTkButton(container, text="📄 Generar Reporte Forense (TXT)", command=exportar, fg_color="#2EC4B6",
                  text_color="#05070A").pack(pady=5, anchor="e")


def cargar_practica_u3_p2(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 3.2: Simulador de Filtros en Wireshark",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Escribe el filtro de red adecuado para aislar sesiones HTTP con credenciales.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f, text="Introduce el filtro de captura Wireshark:", font=("Segoe UI", 12),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=10)
    en_filtro = ctk.CTkEntry(f, width=400, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_filtro.pack(anchor="w", padx=15, pady=5)
    en_filtro.insert(0, "http.request.method == \"POST\"")

    def probar_filtro():
        if "http" in en_filtro.get().lower():
            messagebox.showinfo("¡Filtro Exitoso!", "Se han aislado 14 paquetes HTTP con credenciales.")
        else:
            messagebox.showerror("Error", "Filtro no válido para aislar tráfico web de autenticación.")

    ctk.CTkButton(f, text="Aplicar Filtro en Captura", command=probar_filtro, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)


def cargar_practica_u3_p3(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 3.3: Analizador de Cabeceras (File Carving)",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Identifica y escribe la firma hexadecimal para recuperar un archivo PNG borrado.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f, text="Escribe los bytes mágicos (Magic Number) en Hex:", font=("Segoe UI", 12),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=10)
    en_hex = ctk.CTkEntry(f, width=300, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_hex.pack(anchor="w", padx=15, pady=5)
    en_hex.insert(0, "89 50 4E 47")

    def probar_hex():
        if "89 50" in en_hex.get().upper():
            messagebox.showinfo("¡Carving Exitoso!",
                                "¡Cabecera correcta! Archivo PNG reconstruido desde bloques huérfanos.")
        else:
            messagebox.showerror("Error", "Firma hexadecimal incorrecta para un archivo PNG.")

    ctk.CTkButton(f, text="Ejecutar Carving de Bloques", command=probar_hex, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)


def cargar_practica_u3_p4(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 3.4: Consultas Forenses SQLite", font=("Segoe UI", 16, "bold"),
                 text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Escribe la consulta SQL para extraer registros de una base de datos de mensajería.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f, text="Sentencia SQL de búsqueda:", font=("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT).pack(
        anchor="w", padx=15, pady=10)
    en_sql = ctk.CTkEntry(f, width=450, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_sql.pack(anchor="w", padx=15, pady=5)
    en_sql.insert(0, "SELECT * FROM mensajes;")

    def probar_sql():
        if "select" in en_sql.get().lower():
            messagebox.showinfo("¡Consulta Ejecutada!", "Se extrajeron 24 registros de la base de datos SQLite.")
        else:
            messagebox.showerror("Error SQL", "La sentencia debe ser una consulta SELECT válida.")

    ctk.CTkButton(f, text="Ejecutar Consulta en DB", command=probar_sql, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)