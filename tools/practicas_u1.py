import random
import customtkinter as ctk

COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ENTRY_BG = "#0E1524"
COLOR_ACCENT = "#00F0FF"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_SUCCESS = "#2EC4B6"
COLOR_DANGER = "#E63946"


def limpiar(c):
    for w in c.winfo_children(): w.destroy()


# ==========================================
# MODAL DE MENSAJE HUD PERSONALIZADO
# ==========================================
def mostrar_mensaje_hud(parent, titulo, mensaje, tipo="info"):
    dialog = ctk.CTkToplevel(parent)
    dialog.title("")
    dialog.geometry("480x280")
    dialog.configure(fg_color=COLOR_BG_DARK)
    dialog.overrideredirect(True)
    dialog.attributes("-alpha", 0.0)
    dialog.grab_set()

    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 240
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 140
    dialog.geometry(f"+{x}+{y}")

    # Definir color de acento según el tipo de alerta (éxito, error o advertencia)
    borde_color = COLOR_SUCCESS if tipo == "success" else (COLOR_DANGER if tipo == "error" else COLOR_ACCENT)
    titulo_color = COLOR_SUCCESS if tipo == "success" else (COLOR_DANGER if tipo == "error" else COLOR_ACCENT)

    card_modal = ctk.CTkFrame(dialog, fg_color=COLOR_CARD, border_color=borde_color, border_width=1, corner_radius=12)
    card_modal.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(card_modal, text=titulo, font=ctk.CTkFont("Segoe UI", 15, "bold"), text_color=titulo_color).pack(pady=(20, 8))
    
    # Texto descriptivo con ajuste de línea automático y justificación izquierda para legibilidad
    lbl_msg = ctk.CTkLabel(card_modal, text=mensaje, font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_LIGHT, justify="left", wraplength=420)
    lbl_msg.pack(pady=(0, 20), padx=20)

    id_anim_dialog = None
    def animar_aparicion(alpha=0.0):
        nonlocal id_anim_dialog
        if alpha < 1.0:
            alpha += 0.1
            dialog.attributes("-alpha", alpha)
            id_anim_dialog = dialog.after(15, lambda: animar_aparicion(alpha))

    def cerrar():
        if id_anim_dialog:
            try: dialog.after_cancel(id_anim_dialog)
            except: pass
        dialog.destroy()

    btn_ok = ctk.CTkButton(card_modal, text="Aceptar", command=cerrar, width=150, height=38,
                           fg_color=borde_color, hover_color=COLOR_ACCENT_HOVER if tipo == "info" else borde_color, 
                           text_color=COLOR_BG_DARK if tipo != "error" else COLOR_TEXT_LIGHT, 
                           font=ctk.CTkFont("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2")
    btn_ok.pack(pady=(0, 15))

    animar_aparicion()
    parent.wait_window(dialog)


# ==========================================
# PRÁCTICA 1.1: VOLATILIDAD (Con puntaje y feedback detallado)
# ==========================================
def cargar_practica_u1_p1(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🎮 RETO 1.1: Jerarquía de Volatilidad (RFC 3227)", font=("Segoe UI", 15, "bold"),
                 text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Misión: Demuestra tus conocimientos sobre el orden en que debe recolectarse la evidencia según su nivel de evaporación.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f_card,
                 text="¿Cuál de los siguientes elementos es el más volátil y debe recolectarse en primer lugar?",
                 font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=10)

    var_p1 = ctk.StringVar(value="")
    ctk.CTkRadioButton(f_card, text="Memoria Caché y RAM (Se borran al apagar el equipo)", variable=var_p1, value="ram",
                       text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=5)
    ctk.CTkRadioButton(f_card, text="Disco Duro Mecánico (HDD / SSD)", variable=var_p1, value="hdd",
                       text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=5)
    ctk.CTkRadioButton(f_card, text="Unidad de Respaldo en Cinta magnética", variable=var_p1, value="tape",
                       text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=5)

    def evaluar_p1():
        resp = var_p1.get()
        if not resp:
            mostrar_mensaje_hud(container, "⚠️ ATENCIÓN", "Selecciona una opción para continuar.", tipo="warning")
            return

        if resp == "ram":
            puntaje = 100
            msg = f"🏆 ¡PUNTAJE: {puntaje}/100 PUNTOS (RANGO S)!\n\n💡 ¿Por qué es correcta?\nLa memoria RAM y la caché contienen los procesos activos, conexiones de red y llaves de cifrado que desaparecen inmediatamente al cortar la energía. Es el principio número uno de la RFC 3227."
            mostrar_mensaje_hud(container, "✨ ¡Misión Cumplida!", msg, tipo="success")
        else:
            puntaje = 0
            msg = f"❌ ¡PUNTAJE: {puntaje}/100 PUNTOS (MISIÓN FALLIDA)!\n\n💡 ¿Por qué fallaste?\nElegiste un medio de almacenamiento persistente. Los discos y cintas guardan la información aun sin energía, por lo que la RAM siempre debe capturarse antes de apagar el equipo."
            mostrar_mensaje_hud(container, "⚠️ Error Táctico", msg, tipo="error")

    ctk.CTkButton(container, text="🎯 Enviar Respuesta y Evaluar", command=evaluar_p1, font=("Segoe UI", 12, "bold"),
                  fg_color=COLOR_ACCENT, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 1.2: MINI-JUEGO TÁCTICO DE INCIDENTES
# ==========================================
def cargar_practica_u1_p2(container):
    limpiar(container)

    header_frame = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header_frame.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header_frame, text="🚨 MISIÓN SOC: Servidor Crítico Bajo Ataque (Ransomware)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header_frame,
                 text="Contexto: El servidor principal de bases de datos sufre una intrusión activa. Toma 3 decisiones tácticas.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    scroll_decisiones = ctk.CTkScrollableFrame(container, fg_color=COLOR_CARD, corner_radius=8, height=300)
    scroll_decisiones.pack(fill="both", expand=True, padx=5, pady=5)

    # Decisión 1
    ctk.CTkLabel(scroll_decisiones, text="1. ¿Qué acción perimetral realizarás con la red del servidor?",
                 font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=(10, 5))
    var_d1 = ctk.StringVar(value="")
    ctk.CTkRadioButton(scroll_decisiones,
                       text="Desconectar físicamente el cable de red (Ethernet) manteniendo el equipo encendido.",
                       variable=var_d1, value="opt1", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)
    ctk.CTkRadioButton(scroll_decisiones, text="Apagar el servidor de golpe desconectándolo de la corriente eléctrica.",
                       variable=var_d1, value="opt2", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)
    ctk.CTkRadioButton(scroll_decisiones, text="No hacer nada y esperar el respaldo nocturno.", variable=var_d1,
                       value="opt3", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)

    # Decisión 2
    ctk.CTkLabel(scroll_decisiones, text="2. ¿Cómo procederás con la evidencia volátil (Memoria RAM)?",
                 font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=(15, 5))
    var_d2 = ctk.StringVar(value="")
    ctk.CTkRadioButton(scroll_decisiones,
                       text="Realizar un volcado completo de RAM (Memory Dump) antes de apagar el sistema.",
                       variable=var_d2, value="opt1", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)
    ctk.CTkRadioButton(scroll_decisiones, text="Formatear el disco duro de inmediato para erradicar el virus.",
                       variable=var_d2, value="opt2", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)
    ctk.CTkRadioButton(scroll_decisiones, text="Reiniciar el sistema operativo para limpiar la caché.", variable=var_d2,
                       value="opt3", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)

    # Decisión 3
    ctk.CTkLabel(scroll_decisiones, text="3. ¿Cómo documentarás el inicio del protocolo forense?",
                 font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=(15, 5))
    var_d3 = ctk.StringVar(value="")
    ctk.CTkRadioButton(scroll_decisiones,
                       text="Registrar hora, perito a cargo, hashes y abrir Acta de Cadena de Custodia.",
                       variable=var_d3, value="opt1", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)
    ctk.CTkRadioButton(scroll_decisiones, text="Enviar un mensaje rápido por chat interno avisando que todo va bien.",
                       variable=var_d3, value="opt2", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)
    ctk.CTkRadioButton(scroll_decisiones, text="No registrar nada para ahorrar tiempo valioso.", variable=var_d3,
                       value="opt3", text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=30, pady=3)

    def evaluar_mision():
        d1, d2, d3 = var_d1.get(), var_d2.get(), var_d3.get()
        if not d1 or not d2 or not d3:
            mostrar_mensaje_hud(container, "⚠️ Misión Incompleta", "¡Debes tomar una decisión en las 3 categorías!", tipo="warning")
            return

        puntaje, feedback = 0, []

        if d1 == "opt1":
            puntaje += 40
            feedback.append("✅ [Red]: Correcto. Aislar la red detuvo la exfiltración sin apagar la máquina.")
        else:
            feedback.append("❌ [Red]: Incorrecto. Apagar de golpe o no hacer nada destruyó indicios o propagó el ataque.")

        if d2 == "opt1":
            puntaje += 40
            feedback.append("✅ [RAM]: Impecable. Preservaste conexiones activas y rastros en memoria.")
        else:
            feedback.append("❌ [RAM]: Error crítico. Formatear o reiniciar destruyó las pruebas clave.")

        if d3 == "opt1":
            puntaje += 20
            feedback.append("✅ [Custodia]: Perfecto. Garantizaste validez jurídica ante un tribunal.")
        else:
            feedback.append("❌ [Custodia]: Fallo legal. Sin trazabilidad formal, la evidencia no es admisible.")

        if puntaje == 100:
            rango = "🏆 RANGO S+: PERITO FORENSE ELITE"
            tipo_alerta = "success"
        elif puntaje >= 60:
            rango = "🛡️ RANGO A: ANALISTA SOC JUNIOR"
            tipo_alerta = "success"
        else:
            rango = "💀 RANGO C: BRECHA CRÍTICA (CATÁSTROFE)"
            tipo_alerta = "error"

        mostrar_mensaje_hud(container, "📊 Resultados de la Misión SOC", f"{rango}\nPuntaje Final: {puntaje}/100\n\n" + "\n".join(feedback), tipo=tipo_alerta)

    ctk.CTkButton(container, text="🚀 Ejecutar Protocolo Táctico y Evaluar", command=evaluar_mision,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_ACCENT, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 1.3: CAZA DE TESOROS DE METADATOS CLOUD (Botones interactivos)
# ==========================================
def cargar_practica_u1_p3(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🔍 RETO 1.3: Caza de Metadatos Críticos en la Nube", font=("Segoe UI", 15, "bold"),
                 text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Misión: Analiza el siguiente registro de eventos CloudTrail simulado y haz clic en los 3 metadatos más críticos para la investigación.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(f_card, text="Registro CloudTrail Extraído:", font=("Segoe UI", 11, "bold"),
                 text_color=COLOR_TEXT_LIGHT).pack(anchor="w", padx=15, pady=(10, 5))

    # Área interactiva de botones tipo texto
    f_log = ctk.CTkFrame(f_card, fg_color=COLOR_ENTRY_BG, corner_radius=6)
    f_log.pack(fill="x", padx=15, pady=5)

    seleccionados = {"ip": False, "tiempo": False, "usuario": False, "color": False}

    def seleccionar_btn(tipo, btn_widget):
        if not seleccionados[tipo]:
            seleccionados[tipo] = True
            btn_widget.configure(fg_color=COLOR_SUCCESS, text_color="#05070A")
        else:
            seleccionados[tipo] = False
            btn_widget.configure(fg_color=COLOR_CARD, text_color=COLOR_ACCENT)

    # Fila simulando texto con botones interactivos incrustados
    f_btns_row1 = ctk.CTkFrame(f_log, fg_color="transparent")
    f_btns_row1.pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(f_btns_row1, text="• Origen del ataque -> ", text_color=COLOR_TEXT_MUTED).pack(side="left")
    b1 = ctk.CTkButton(f_btns_row1, text="[IP: 203.0.113.45]", fg_color=COLOR_CARD, text_color=COLOR_ACCENT, width=130,
                       command=lambda: seleccionar_btn("ip", b1))
    b1.pack(side="left", padx=5)

    f_btns_row2 = ctk.CTkFrame(f_log, fg_color="transparent")
    f_btns_row2.pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(f_btns_row2, text="• Marca temporal -> ", text_color=COLOR_TEXT_MUTED).pack(side="left")
    b2 = ctk.CTkButton(f_btns_row2, text="[Timestamp: 2026-10-12T04:12Z]", fg_color=COLOR_CARD, text_color=COLOR_ACCENT,
                       width=200, command=lambda: seleccionar_btn("tiempo", b2))
    b2.pack(side="left", padx=5)

    f_btns_row3 = ctk.CTkFrame(f_log, fg_color="transparent")
    f_btns_row3.pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(f_btns_row3, text="• Cuenta afectada -> ", text_color=COLOR_TEXT_MUTED).pack(side="left")
    b3 = ctk.CTkButton(f_btns_row3, text="[IAM: Admin-Root-Service]", fg_color=COLOR_CARD, text_color=COLOR_ACCENT,
                       width=170, command=lambda: seleccionar_btn("usuario", b3))
    b3.pack(side="left", padx=5)

    f_btns_row4 = ctk.CTkFrame(f_log, fg_color="transparent")
    f_btns_row4.pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(f_btns_row4, text="• Dato irrelevante -> ", text_color=COLOR_TEXT_MUTED).pack(side="left")
    b4 = ctk.CTkButton(f_btns_row4, text="[Theme: Dark-Mode-Enabled]", fg_color=COLOR_CARD, text_color=COLOR_ACCENT,
                       width=190, command=lambda: seleccionar_btn("color", b4))
    b4.pack(side="left", padx=5)

    def verificar_metadatos():
        if seleccionados["ip"] and seleccionados["tiempo"] and seleccionados["usuario"] and not seleccionados["color"]:
            mostrar_mensaje_hud(container, "✨ ¡Misión Cumplida!", "🏆 ¡Puntaje: 100/100!\nHas identificado correctamente los metadatos críticos de infraestructura e ignorado los datos basura.", tipo="success")
        else:
            mostrar_mensaje_hud(container, "⚠️ Revisa tus selecciones", "❌ Puntaje incompleto o seleccionaste un dato irrelevante (como el tema de color). Asegúrate de elegir IP, Timestamp y cuenta IAM.", tipo="error")

    ctk.CTkButton(container, text="🕵️ Comprobar Metadatos Seleccionados", command=verificar_metadatos,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_ACCENT, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)


# ==========================================
# PRÁCTICA 1.4: VERIFICACIÓN DE HASH E INTEGRIDAD ALEATORIA
# ==========================================
def cargar_practica_u1_p4(container):
    limpiar(container)

    header = ctk.CTkFrame(container, fg_color=COLOR_ENTRY_BG, corner_radius=8)
    header.pack(fill="x", padx=5, pady=(0, 10))
    ctk.CTkLabel(header, text="🛡️ RETO 1.4: Auditoría de Integridad y Hashes (ISO/IEC 27037)",
                 font=("Segoe UI", 15, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", padx=15, pady=(10, 2))
    ctk.CTkLabel(header,
                 text="Misión: Compara el Hash registrado en la escena contra el Hash actual del archivo analizado para detectar manipulación.",
                 font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

    f_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=8)
    f_card.pack(fill="both", expand=True, padx=5, pady=5)

    estado_hash = {"es_igual": random.choice([True, False])}

    hash_original = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    if estado_hash["es_igual"]:
        hash_actual = hash_original
    else:
        hash_actual = "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"

    ctk.CTkLabel(f_card, text=f"📋 Hash Registrado en Acta (Original):\n{hash_original}", font=("Consolas", 11),
                 text_color=COLOR_ACCENT, justify="left").pack(anchor="w", padx=20, pady=(15, 5))
    ctk.CTkLabel(f_card, text=f"🔍 Hash Calculado Actual (Muestra):\n{hash_actual}", font=("Consolas", 11),
                 text_color=COLOR_TEXT_LIGHT, justify="left").pack(anchor="w", padx=20, pady=(5, 15))

    f_opciones = ctk.CTkFrame(f_card, fg_color="transparent")
    f_opciones.pack(anchor="w", padx=20, pady=10)

    var_integra = ctk.StringVar(value="")
    ctk.CTkRadioButton(f_opciones, text="La evidencia está INTACTA (Los hashes coinciden)", variable=var_integra,
                       value="integra", text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)
    ctk.CTkRadioButton(f_opciones, text="La evidencia fue ALTERADA (Los hashes NO coinciden)", variable=var_integra,
                       value="alterada", text_color=COLOR_TEXT_MUTED).pack(anchor="w", pady=5)

    def comprobar_integridad():
        eleccion = var_integra.get()
        if not eleccion:
            mostrar_mensaje_hud(container, "⚠️ Atención", "Selecciona una conclusión sobre la integridad.", tipo="warning")
            return

        es_correcto_integra = (eleccion == "integra" and estado_hash["es_igual"]) or (
                    eleccion == "alterada" and not estado_hash["es_igual"])

        if es_correcto_integra:
            if estado_hash["es_igual"]:
                mostrar_mensaje_hud(container, "✨ ¡Diagnóstico Correcto!", "🏆 ¡Puntaje: 100/100!\nLos hashes coinciden exactamente. La evidencia mantiene su integridad probatoria y es apta para juicio.", tipo="success")
            else:
                mostrar_mensaje_hud(container, "🚨 ¡Fraude Detectado!", "🏆 ¡Puntaje: 100/100!\n¡Excelente ojo clínico! Los hashes difieren, lo que demuestra que la información ha sido alterada, violando la cadena de custodia.", tipo="success")
        else:
            mostrar_mensaje_hud(container, "❌ Diagnóstico Erróneo", "Error pericial. Compara cuidadosamente los caracteres de ambos hashes para determinar si sufrieron modificaciones.", tipo="error")

    ctk.CTkButton(container, text="⚖️ Validar Diagnóstico de Integridad", command=comprobar_integridad,
                  font=("Segoe UI", 12, "bold"), fg_color=COLOR_ACCENT, text_color="#05070A", height=38).pack(fill="x", padx=5, pady=10)
