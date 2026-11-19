import json
from pathlib import Path
import customtkinter as ctk


PREFS_FILE = Path(__file__).resolve().parent.parent / "tutorial_prefs.json"

COLOR_BG_DARK = "#05070A"
COLOR_CARD = "#090D18"
COLOR_ACCENT = "#00F0FF"
COLOR_ACCENT_HOVER = "#00C4D4"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ENTRY_BG = "#0E1524"
COLOR_BORDER = "#1E293B"
COLOR_SUCCESS = "#2EC4B6"

TUTORIAL_CONTENT = {
    "alumno": {
        "titulo": "🎓 TUTORIAL — APARTADO ALUMNO",
        "subtitulo": "Cómo navegar el temario, responder cuestionarios, usar prácticas y ver calificaciones",
        "pasos": [
            "1. Selecciona un tema del temario: Haz clic en cualquier unidad del menú lateral izquierdo para cargar su explicación, cuestionario y prácticas.",
            "2. Explora las 4 pestañas del módulo: Lee la teoría en '1. Explicación', contesta el examen en '2. Cuestionario' o entra a '3. Práctica Aplicada'.",
            "3. Ejecuta las prácticas de la unidad: Usa los botones Práctica 1 a 4 para abrir las herramientas forenses y consulta tus puntajes en '4. Mis Calificaciones'.",
            "4. Guía y cierre de sesión: Presiona '❓ AYUDA / TUTORIAL' arriba de 'CERRAR SESIÓN' cuando necesites repasar estos pasos."
        ],
    },
    "docente": {
        "titulo": "👨‍🏫 TUTORIAL — APARTADO DOCENTE",
        "subtitulo": "Seguimiento del grupo, revisión de actividades y control académico",
        "pasos": [
            "1. Consulta el avance de tus alumnos: Revisa el progreso, entregas y calificaciones registradas por unidad y tema.",
            "2. Verifica evidencias y prácticas: Comprueba que las actividades y reportes generados cumplan con los criterios de la unidad.",
            "3. Registra retroalimentación: Agrega observaciones claras para orientar a los estudiantes en su análisis forense.",
            "4. Guía y cierre de sesión: Pulsa '❓ AYUDA / TUTORIAL' arriba de 'CERRAR SESIÓN' para volver a ver este apartado."
        ],
    },
    "admin": {
        "titulo": "🛡️ TUTORIAL — APARTADO ADMIN",
        "subtitulo": "Administración de usuarios, catálogo del laboratorio y mantenimiento",
        "pasos": [
            "1. Gestiona usuarios y roles: Crea, edita o desactiva cuentas asignando el rol correspondiente (alumno, docente o admin).",
            "2. Revisa temas, preguntas y prácticas: Verifica que el temario, reactivos y módulos de práctica estén disponibles en el sistema.",
            "3. Resguarda la base de datos: Realiza respaldos antes de cambios estructurales o limpiezas para evitar pérdida de información.",
            "4. Guía y cierre de sesión: Usa '❓ AYUDA / TUTORIAL' arriba de 'CERRAR SESIÓN' cuando quieras revisar este apartado."
        ],
    },
}


def _load_prefs() -> dict:
    if PREFS_FILE.exists():
        try:
            data = json.loads(PREFS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {"dismissed_roles": []}


def _save_prefs(prefs: dict) -> None:
    try:
        PREFS_FILE.write_text(json.dumps(prefs, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def should_show_tutorial_on_entry(role: str) -> bool:
    role_key = role.lower().strip()
    prefs = _load_prefs()
    dismissed = set(prefs.get("dismissed_roles", []))
    return role_key not in dismissed


def open_tutorial(parent, role: str = "alumno", auto: bool = False):
    role_clean = role.lower().strip() if role else "alumno"
    role_key = role_clean if role_clean in TUTORIAL_CONTENT else "alumno"

    if auto and not should_show_tutorial_on_entry(role_key):
        return None

    data = TUTORIAL_CONTENT[role_key]

    modal = ctk.CTkToplevel(parent)
    modal.title("")
    modal.geometry("580x445")
    modal.configure(fg_color=COLOR_BG_DARK)
    modal.overrideredirect(True)
    modal.attributes("-alpha", 0.0)
    modal.grab_set()

    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - 290
    y = parent.winfo_y() + (parent.winfo_height() // 2) - 222
    modal.geometry(f"+{max(x, 20)}+{max(y, 20)}")

    card = ctk.CTkFrame(
        modal, fg_color=COLOR_CARD, border_color=COLOR_ACCENT, border_width=1, corner_radius=14
    )
    card.pack(fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(
        card, text=data["titulo"],
        font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=COLOR_ACCENT
    ).pack(pady=(20, 4), padx=20, anchor="w")

    ctk.CTkLabel(
        card, text=data["subtitulo"],
        font=ctk.CTkFont("Segoe UI", 12), text_color=COLOR_TEXT_MUTED
    ).pack(pady=(0, 12), padx=20, anchor="w")

    scroll = ctk.CTkScrollableFrame(card, fg_color=COLOR_ENTRY_BG, corner_radius=10, height=205)
    scroll.pack(fill="both", expand=True, padx=20, pady=(0, 12))

    for p in data["pasos"]:
        item = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=8)
        item.pack(fill="x", padx=6, pady=5)
        ctk.CTkLabel(
            item, text=p, font=ctk.CTkFont("Segoe UI", 12),
            text_color=COLOR_TEXT_LIGHT, justify="left", wraplength=480
        ).pack(padx=12, pady=9, anchor="w")

    prefs = _load_prefs()
    dismissed = set(prefs.get("dismissed_roles", []))
    var_dont_show = ctk.BooleanVar(value=role_key in dismissed)

    def guardar_preferencia():
        p_actual = _load_prefs()
        descartados = set(p_actual.get("dismissed_roles", []))
        if var_dont_show.get():
            descartados.add(role_key)
        else:
            descartados.discard(role_key)
        p_actual["dismissed_roles"] = sorted(descartados)
        _save_prefs(p_actual)

    ctk.CTkCheckBox(
        card,
        text="No volver a mostrar automáticamente en este apartado",
        variable=var_dont_show,
        command=guardar_preferencia,
        font=ctk.CTkFont("Segoe UI", 12),
        text_color=COLOR_TEXT_MUTED,
        fg_color=COLOR_ACCENT,
        hover_color=COLOR_ACCENT_HOVER,
        border_color=COLOR_ACCENT,
        checkmark_color=COLOR_BG_DARK,
    ).pack(padx=22, pady=(0, 12), anchor="w")

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
        guardar_preferencia()
        if modal.winfo_exists():
            try:
                modal.grab_release()
            except Exception:
                pass
            modal.destroy()

    ctk.CTkButton(
        card, text="ENTENDIDO", command=cerrar, width=160, height=36,
        fg_color=COLOR_SUCCESS, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG_DARK,
        font=ctk.CTkFont("Segoe UI", 12, "bold"), corner_radius=8, cursor="hand2"
    ).pack(pady=(0, 16))

    modal.bind("<Return>", lambda e: cerrar())
    modal.bind("<Escape>", lambda e: cerrar())
    fade_in()
    parent.wait_window(modal)
