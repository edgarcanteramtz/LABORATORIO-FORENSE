import os
import sqlite3

# Rutas robustas para asegurar que la DB siempre se guarde en la carpeta 'database'
DIR_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DIR_PRINCIPAL, "database", "lab_forense.db")

def conectar():
    """Establece conexión con la base de datos SQLite y asegura que la carpeta exista."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def inicializar_base_datos():
    """Crea la estructura de tablas si no existen."""
    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla Usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            nombre_usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('alumno','docente','admin')) NOT NULL,
            grupo_id INTEGER NULL
        )
    """)

    # Tabla Grupos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grupos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_grupo TEXT NOT NULL,
            docente_id INTEGER,
            FOREIGN KEY(docente_id) REFERENCES usuarios(id)
        )
    """)

    # Tabla Temas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidad INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            contenido_teorico TEXT NOT NULL
        )
    """)

    # Tabla Preguntas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tema_id INTEGER,
            pregunta TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            respuesta_correcta TEXT CHECK(respuesta_correcta IN ('A', 'B', 'C', 'D')) NOT NULL,
            FOREIGN KEY (tema_id) REFERENCES temas(id)
        )
    """)

    # Tabla Calificaciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER,
            tema_id INTEGER,
            puntaje INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alumno_id) REFERENCES usuarios(id),
            FOREIGN KEY (tema_id) REFERENCES temas(id)
        )
    """)

    conexion.commit()
    conexion.close()

def cargar_datos_iniciales():
    """Inserta usuarios demo, temario y banco de preguntas si la base de datos está vacía."""
    conexion = conectar()
    cursor = conexion.cursor()

    # 1. Usuarios demo
    usuarios_demo = [
        ("Administrador Sistema", "admin", "admin123", "admin"),
        ("Profesor Forense", "docente1", "docente123", "docente"),
        ("Alumno Prueba", "alumno1", "alumno123", "alumno"),
    ]
    for nombre, user, password, rol in usuarios_demo:
        cursor.execute(
            "INSERT OR IGNORE INTO usuarios (nombre_completo, nombre_usuario, password, rol) VALUES (?, ?, ?, ?)",
            (nombre, user, password, rol),
        )

    # 2. Temario Oficial
    temario_oficial = [
        (1, "Generalidades del Análisis Forense Informático", "1.1 Conceptos generales\n1.2 Importancia\n1.3 Situación actual\n1.4 Principios\n1.5 Estándares\n   1.5.1 Nivel nacional\n   1.5.2 Nivel internacional"),
        (2, "Metodología del Análisis Forense Informático", "2.1 Identificación de la evidencia\n2.2 Adquisición de la evidencia\n2.3 Preservación de la evidencia\n2.4 Análisis de la evidencia\n2.5 Presentación del informe"),
        (3, "Herramientas de Análisis Forense", "3.1 Software Libre de herramientas (Autopsy, Wireshark, CAINE, ExifTool)\n3.2 Revisión de Herramientas de recuperación de datos\n3.3 Programas de Recuperación de Datos Forenses"),
        (4, "Evidencia y Atribución del Ataque Digital", "4.1 Informática forense digital\n   4.1.1 Análisis y respuesta a incidentes\n4.2 Evidencias analizadas"),
    ]

    for unidad, titulo, contenido in temario_oficial:
        cursor.execute("SELECT id FROM temas WHERE unidad = ?", (unidad,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO temas (unidad, titulo, contenido_teorico) VALUES (?, ?, ?)",
                (unidad, titulo, contenido),
            )

    # 3. Preguntas Unidad 1
    cursor.execute("SELECT id FROM temas WHERE unidad = 1")
    tema_1 = cursor.fetchone()

    if tema_1:
        tema_1_id = tema_1[0]
        preguntas_u1 = [
            (tema_1_id, "¿Cuál es el objetivo principal del análisis forense digital?", "Instalar antivirus en el sistema", "Identificar, preservar y analizar evidencia digital sin alterarla", "Eliminar registros de auditoría", "Formatear discos duros", "B"),
            (tema_1_id, "¿Qué principio garantiza que la evidencia mantenga su integridad desde el hallazgo hasta el juicio?", "Cadena de Custodia", "Cifrado de disco", "Formateo rápido", "Ingeniería inversa", "A"),
        ]

        for t_id, preg, op_a, op_b, op_c, op_d, resp in preguntas_u1:
            cursor.execute("SELECT id FROM preguntas WHERE pregunta = ?", (preg,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (t_id, preg, op_a, op_b, op_c, op_d, resp),
                )

    conexion.commit()
    conexion.close()
    print("✅ Base de datos inicializada y cargada con datos de prueba.")

if __name__ == "__main__":
    inicializar_base_datos()
    cargar_datos_iniciales()


    import sqlite3

class DBManager:
    def __init__(self, db_path="database/lab_forense.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.crear_tabla_practicas()
        self.poblar_practicas()

    def crear_tabla_practicas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS practicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unidad INTEGER,
                numero_practica INTEGER,
                titulo TEXT,
                descripcion TEXT
            )
        ''')
        self.conn.commit()

    def poblar_practicas(self):
        # Verifica si la tabla ya tiene datos para no duplicarlos
        self.cursor.execute('SELECT COUNT(*) FROM practicas')
        if self.cursor.fetchone()[0] == 0:
            lista_practicas = [
                # Unidad 1
                (1, 1, 'Reto de Trivia "Principios Forenses"', 'Clasifica decisiones basadas en principios forenses.'),
                (1, 2, 'Simulador de Cumplimiento (ISO/IEC 27037)', 'Selecciona directrices para el manejo de dispositivos.'),
                (1, 3, 'Crucigrama de Terminología', 'Resuelve conceptos de evidencia digital y volatilidad.'),
                (1, 4, 'Análisis de Caso Real', 'Identifica violaciones en la recolección de evidencia.'),
                # Unidad 2
                (2, 1, 'Laboratorio de Identificación', 'Etiqueta evidencia crítica en una red comprometida.'),
                (2, 2, 'Generador y Verificador de Hashes', 'Calcula huellas digitales (MD5/SHA-256) de evidencias.'),
                (2, 3, 'Llenado de Cadena de Custodia', 'Rellena el formato legal de recolección.'),
                (2, 4, 'Constructor de Informes', 'Ordena las secciones de un informe pericial.'),
                # Unidad 3
                (3, 1, 'Cazador de Metadatos (ExifTool)', 'Extrae metadatos y GPS de una imagen.'),
                (3, 2, 'Mini-Reto de Tráfico (Wireshark)', 'Filtra un archivo .pcap para buscar contraseñas.'),
                (3, 3, 'File Carving (Recuperación)', 'Recupera fragmentos de archivos eliminados.'),
                (3, 4, 'Análisis de BD SQLite', 'Ejecuta consultas para extraer chats eliminados.'),
                # Unidad 4
                (4, 1, 'Simulador de Triage', 'Toma decisiones críticas ante un incidente en curso.'),
                (4, 2, 'Análisis de Eventos Windows', 'Busca códigos de evento para armar una cronología.'),
                (4, 3, 'Línea de Tiempo (Timeline)', 'Ordena logs desordenados de un ataque.'),
                (4, 4, 'Atribución (IoC)', 'Empareja indicadores de compromiso con tácticas de ataque.')
            ]
            self.cursor.executemany('''
                INSERT INTO practicas (unidad, numero_practica, titulo, descripcion) 
                VALUES (?, ?, ?, ?)
            ''', lista_practicas)
            self.conn.commit()

    def obtener_practicas_por_unidad(self, unidad):
        self.cursor.execute('SELECT id, numero_practica, titulo, descripcion FROM practicas WHERE unidad = ?', (unidad,))
        return self.cursor.fetchall()