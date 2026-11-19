import os
import sqlite3
import customtkinter as ctk
from PIL import Image

from database.db_manager import inicializar_base_datos, cargar_datos_iniciales, DB_PATH

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_ACCENT_HOVER = "#00C4D4"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BORDER = "#1E293B"
COLOR_SUCCESS = "#2EC4B6"
COLOR_DANGER = "#E63946"
COLOR_DANGER_HOVER = "#D62828"


def crear_barra_titulo(ventana, bg_color, on_close=None):
    barra_titulo = ctk.CTkFrame(ventana, height=35, fg_color=bg_color, corner_radius=0)
    barra_titulo.pack(side="top", fill="x")
    barra_titulo.pack_propagate(False)

    comando_cerrar = on_close if on_close else ventana.destroy

    btn_cerrar = ctk.CTkButton(
        barra_titulo, text="✕", font=("Segoe UI", 14), width=45, height=35,
        fg_color="transparent", hover_color="#E81123", text_color="white",
        corner_radius=0, command=comando_cerrar
    )
    btn_cerrar.pack(side="right")

    def toggle_maximizar():
        es_fullscreen = ventana.attributes("-fullscreen")
        ventana.attributes("-fullscreen", not es_fullscreen)

    btn_max = ctk.CTkButton(
        barra_titulo, text="🗗", font=("Segoe UI", 15), width=45, height=35,
        fg_color="transparent", hover_color=COLOR_BORDER, text_color="white",
        corner_radius=0, command=toggle_maximizar
    )
    btn_max.pack(side="right")

    btn_min = ctk.CTkButton(
        barra_titulo, text="—", font=("Segoe UI", 15, "bold"), width=45, height=35,
        fg_color="transparent", hover_color=COLOR_BORDER, text_color="white",
        corner_radius=0, command=ventana.iconify
    )
    btn_min.pack(side="right")


def mostrar_alerta_hud(parent, titulo, mensaje, tipo="error"):
    borde = COLOR_DANGER if tipo == "error" else (COLOR_SUCCESS if tipo == "success" else COLOR_ACCENT)
    color_tit = COLOR_DANGER if tipo == "error" else (COLOR_SUCCESS if tipo == "success" else COLOR_ACCENT)

    modal = ctk.CTkToplevel(parent)
    modal.title("")
    modal.geometry("440x225")
    modal.configure(fg_color=COLOR_BG_DARK)
    modal.overrideredirect(True)
    modal.attributes("-alpha", 0.0)
    modal.grab_set()

    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 220
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 112
    modal.geometry(f"+{x}+{y}")

    card_m = ctk.CTkFrame(
        modal, fg_color=COLOR_CARD, border_color=borde, border_width=1, corner_radius=12
    )
    card_m.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(
        card_m, text=titulo, font=ctk.CTkFont("Segoe UI", 15, "bold"), text_color=color_tit
    ).pack(pady=(22, 8))

    ctk.CTkLabel(
        card_m, text=mensaje, font=ctk.CTkFont("Segoe UI", 12),
        text_color=COLOR_TEXT_LIGHT, justify="center", wraplength=380
    ).pack(pady=(0, 20), padx=16)

    anim_id = None

    def fade_in(a=0.0):
        nonlocal anim_id
        if a < 1.0 and modal.winfo_exists():
            a = min(1.0, a + 0.12)
            modal.attributes("-alpha", a)
            anim_id = modal.after(15, lambda: fade_in(a))

    def cerrar():
        if anim_id:
            try:
                modal.after_cancel(anim_id)
            except Exception:
                pass
        if modal.winfo_exists():
            modal.destroy()

    ctk.CTkButton(
        card_m, text="ACEPTAR", command=cerrar, width=140, height=36,
        fg_color=borde, hover_color=COLOR_DANGER_HOVER if tipo == "error" else COLOR_ACCENT_HOVER,
        text_color=COLOR_TEXT_LIGHT if tipo == "error" else COLOR_BG_DARK,
        font=ctk.CTkFont("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2"
    ).pack(pady=(0, 14))

    modal.bind("<Return>", lambda e: cerrar())
    modal.bind("<Escape>", lambda e: cerrar())
    fade_in()
    parent.wait_window(modal)


inicializar_base_datos()
cargar_datos_iniciales()


def main():
    app = ctk.CTk()
    app.title("LAB VISUAL FORENSE")
    app.configure(fg_color=COLOR_BG_DARK)
    app.attributes("-fullscreen", True)

    dir_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(dir_actual, "assets", "fondo_forense.png")
    fondo_ctk = None

    try:
        if os.path.exists(ruta_imagen):
            img_pil = Image.open(ruta_imagen)
            ancho_p = app.winfo_screenwidth()
            alto_p = app.winfo_screenheight()
            fondo_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(ancho_p, alto_p))
    except Exception:
        fondo_ctk = None

    autenticando = {"activo": False}

    def limpiar_vista_actual():
        for w in list(app.winfo_children()):
            w.destroy()

    def mostrar_login():
        autenticando["activo"] = False
        limpiar_vista_actual()

        crear_barra_titulo(app, COLOR_CARD, on_close=app.destroy)

        area_login = ctk.CTkFrame(app, fg_color=COLOR_BG_DARK, corner_radius=0)
        area_login.pack(fill="both", expand=True)

        if fondo_ctk is not None:
            lbl_fondo = ctk.CTkLabel(area_login, image=fondo_ctk, text="")
            lbl_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        card = ctk.CTkFrame(
            area_login, width=400, height=500, fg_color=COLOR_CARD,
            border_color=COLOR_BORDER, border_width=1, corner_radius=15
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="LAB VISUAL FORENSE",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=COLOR_ACCENT
        ).grid(row=0, column=0, pady=(35, 5))

        ctk.CTkLabel(
            card, text="Acceso al sistema",
            font=ctk.CTkFont(family="Segoe UI", size=13), text_color=COLOR_TEXT_MUTED
        ).grid(row=1, column=0, pady=(0, 25))

        entry_usuario = ctk.CTkEntry(
            card, placeholder_text="Usuario", font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER,
            height=45, corner_radius=8
        )
        entry_usuario.grid(row=2, column=0, sticky="ew", padx=40, pady=(0, 15))

        entry_clave = ctk.CTkEntry(
            card, placeholder_text="Contraseña", show="*", font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXT_LIGHT, border_color=COLOR_BORDER,
            height=45, corner_radius=8
        )
        entry_clave.grid(row=3, column=0, sticky="ew", padx=40, pady=(0, 20))

        def iniciar_sesion(event=None):
            if autenticando["activo"]:
                return
            usuario = entry_usuario.get().strip()
            clave = entry_clave.get().strip()

            if not usuario or not clave:
                mostrar_alerta_hud(
                    app, "⚠️ CAMPOS INCOMPLETOS",
                    "Por favor, ingresa tu usuario y contraseña para continuar.", tipo="warning"
                )
                return

            autenticando["activo"] = True
            try:
                conexion = sqlite3.connect(DB_PATH)
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT rol FROM usuarios WHERE nombre_usuario = ? AND password = ?",
                    (usuario, clave)
                )
                resultado = cursor.fetchone()
                conexion.close()
            except Exception as e:
                autenticando["activo"] = False
                mostrar_alerta_hud(
                    app, "❌ ERROR DE BASE DE DATOS",
                    f"No fue posible validar las credenciales:\n{e}", tipo="error"
                )
                return

            if not resultado:
                autenticando["activo"] = False
                mostrar_alerta_hud(
                    app, "🔒 CONTRASEÑA O USUARIO INCORRECTO",
                    "El usuario o la contraseña ingresados son incorrectos.\nVerifica tus datos e inténtalo de nuevo.",
                    tipo="error"
                )
                return

            rol = resultado[0]
            app.withdraw()
            app.update_idletasks()

            try:
                if rol == "admin":
                    from views.admin_view import abrir_panel_admin
                    regresar = abrir_panel_admin(usuario)
                elif rol == "docente":
                    from views.teacher_view import abrir_panel_docente
                    regresar = abrir_panel_docente(usuario)
                elif rol == "alumno":
                    from views.student_view import abrir_panel_alumno
                    regresar = abrir_panel_alumno(usuario)
                else:
                    regresar = True
            except Exception as exc:
                autenticando["activo"] = False
                app.deiconify()
                app.attributes("-fullscreen", True)
                app.update_idletasks()
                app.update()
                mostrar_login()
                mostrar_alerta_hud(
                    app, "❌ ERROR AL ABRIR PORTAL",
                    f"Ocurrió un problema al cargar la vista:\n{exc}", tipo="error"
                )
                return

            if regresar and app.winfo_exists():
                app.deiconify()
                app.attributes("-fullscreen", True)
                app.lift()
                app.focus_force()
                app.update_idletasks()
                app.update()
                mostrar_login()
            elif app.winfo_exists():
                app.destroy()

        btn_ingresar = ctk.CTkButton(
            card, text="INICIAR SESIÓN", command=iniciar_sesion,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=COLOR_ACCENT, text_color=COLOR_BG_DARK, hover_color=COLOR_ACCENT_HOVER,
            height=42, corner_radius=8, cursor="hand2"
        )
        btn_ingresar.grid(row=4, column=0, sticky="ew", padx=40, pady=(0, 10))

        btn_salir_sistema = ctk.CTkButton(
            card, text="SALIR DEL PROGRAMA", command=app.destroy,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=COLOR_DANGER, text_color=COLOR_TEXT_LIGHT, hover_color=COLOR_DANGER_HOVER,
            height=38, corner_radius=8, cursor="hand2"
        )
        btn_salir_sistema.grid(row=5, column=0, sticky="ew", padx=40)

        app.bind("<Return>", iniciar_sesion)

    mostrar_login()
    app.mainloop()


if __name__ == "__main__":
    main()
