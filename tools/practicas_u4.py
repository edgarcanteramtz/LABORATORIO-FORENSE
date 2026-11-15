import customtkinter as ctk
from tkinter import messagebox

COLOR_CARD = "#090D18"
COLOR_ENTRY_BG = "#0E1524"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"


def limpiar(c):
    for w in c.winfo_children(): w.destroy()


def cargar_practica_u4_p1(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 4.1: Simulador de Reglas de Firewall (Mitigación DoS)",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Escribe la regla de bloqueo perimetral para una dirección IP atacante.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f, text="Escribe el comando iptables para bloquear la IP 192.168.1.50:", font=("Segoe UI", 12),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=10)
    en_rule = ctk.CTkEntry(f, width=400, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT)
    en_rule.pack(anchor="w", padx=15, pady=5)
    en_rule.insert(0, "iptables -A INPUT -s 192.168.1.50 -j DROP")

    def probar_rule():
        val = en_rule.get()
        if "iptables" in val and "DROP" in val:
            messagebox.showinfo("¡Ataque Contenido!", "Regla aplicada exitosamente en el firewall perimetral.")
        else:
            messagebox.showerror("Error", "La regla debe usar iptables y la acción DROP para bloquear.")

    ctk.CTkButton(f, text="Aplicar Regla de Bloqueo", command=probar_rule, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)


def cargar_practica_u4_p2(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 4.2: Correlación de Bitácoras", font=("Segoe UI", 16, "bold"),
                 text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Selecciona y simula el cruce de logs de autenticación con el servidor web.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)

    f_chk = ctk.CTkFrame(f, fg_color="transparent")
    f_chk.pack(anchor="w", padx=15, pady=15)
    c1 = ctk.BooleanVar()
    c2 = ctk.BooleanVar()
    ctk.CTkCheckBox(f_chk, text="Cargar logs de acceso Apache (/var/log/apache2/access.log)", variable=c1,
                    text_color=COLOR_TEXT_LIGHT).pack(anchor="w", pady=5)
    ctk.CTkCheckBox(f_chk, text="Cargar registros de autenticación SSH (/var/log/auth.log)", variable=c2,
                    text_color=COLOR_TEXT_LIGHT).pack(anchor="w", pady=5)

    def correr_siem():
        if c1.get() and c2.get():
            messagebox.showinfo("Correlación Exitosa",
                                "Se cruzaron 1,420 eventos. Patrón de fuerza bruta identificado.")
        else:
            messagebox.showwarning("Incompleto", "Debes cargar ambas fuentes de bitácoras para hacer la correlación.")

    ctk.CTkButton(f, text="Ejecutar Correlación SIEM", command=correr_siem, fg_color=COLOR_ACCENT,
                  text_color="#05070A").pack(anchor="e", padx=15, pady=15)


def cargar_practica_u4_p3(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 4.3: Generador de Línea de Tiempo",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Simula el ordenamiento cronológico de las marcas temporales del incidente.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)
    ctk.CTkButton(f, text="Generar Línea de Tiempo Unificada (Timeline)",
                  command=lambda: messagebox.showinfo("Timeline",
                                                      "Cronología generada con 15 eventos ordenados en formato UTC."),
                  fg_color=COLOR_ACCENT, text_color="#05070A").pack(anchor="w", padx=15, pady=25)


def cargar_practica_u4_p4(container):
    limpiar(container)
    ctk.CTkLabel(container, text="Práctica Interactiva 4.4: Exportación de Indicadores de Compromiso (IoCs)",
                 font=("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT).pack(pady=5, anchor="w")
    ctk.CTkLabel(container, text="Genera el reporte final de atribución con los hashes y dominios C2 detectados.",
                 font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    f = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f.pack(fill="both", expand=True, padx=5, pady=5)
    ctk.CTkButton(f, text="Exportar IoCs a Formato Pericial (JSON/TXT)", command=lambda: messagebox.showinfo("IoCs",
                                                                                                             "Indicadores de compromiso exportados y listos para tribunales."),
                  fg_color=COLOR_ACCENT, text_color="#05070A").pack(anchor="w", padx=15, pady=25)