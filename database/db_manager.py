import sqlite3
import os

# Definimos el nombre del archivo de nuestra base de datos.
# Al ejecutarse, creará este archivo automáticamente en la misma carpeta.
DB_PATH = "lab_forense.db"


def conectar():
    """
    Establece la conexión con la base de datos SQLite.
    Si el archivo 'lab_forense.db' no existe, lo crea automáticamente.
    """
    conexion = sqlite3.connect(DB_PATH)
    return conexion


def inicializar_base_datos():
    """
    Crea todas las tablas (estructuras de filas y columnas) necesarias
    para que el laboratorio funcione, solo si estas aún no existen.
    """
    conexion = conectar()
    cursor = conexion.cursor()  # El cursor es nuestra "herramienta" para ejecutar comandos SQL

    # 1. Tabla de Usuarios (Alumnos, Docentes, Administradores)
    # Guarda las credenciales y el rol de cada persona.
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuarios
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nombre_completo
                       TEXT
                       NOT
                       NULL,
                       nombre_usuario
                       TEXT
                       UNIQUE
                       NOT
                       NULL, -- El nombre de usuario no se puede repetir
                       password
                       TEXT
                       NOT
                       NULL, -- Contraseña del usuario
                       rol
                       TEXT
                       CHECK (
                       rol
                       IN
                   (
                       'alumno',
                       'docente',
                       'admin'
                   )) NOT NULL,
                       grupo_id INTEGER NULL -- Puede estar vacío si es un docente o admin
                       )
                   ''')

    # 2. Tabla de Grupos
    # Sirve para que el docente (o admin) organice a los alumnos.
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS grupos
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nombre_grupo
                       TEXT
                       NOT
                       NULL,
                       docente_id
                       INTEGER,
                       FOREIGN
                       KEY
                   (
                       docente_id
                   ) REFERENCES usuarios
                   (
                       id
                   ) -- Vincula el grupo con un docente
                       )
                   ''')

    # 3. Tabla del Temario (Unidades 1 a 4 según tu captura de pantalla)
    # Almacena el número de unidad, título y el texto de la teoría para los alumnos.
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS temas
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       unidad
                       INTEGER
                       NOT
                       NULL,
                       titulo
                       TEXT
                       NOT
                       NULL,
                       contenido_teorico
                       TEXT
                   )
                   ''')

    # 4. Tabla de Preguntas (Para los cuestionarios de opción múltiple)
    # Cada pregunta pertenece a un 'tema_id' específico y tiene 4 opciones.
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS preguntas
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       tema_id
                       INTEGER,
                       pregunta
                       TEXT
                       NOT
                       NULL,
                       opcion_a
                       TEXT
                       NOT
                       NULL,
                       opcion_b
                       TEXT
                       NOT
                       NULL,
                       opcion_c
                       TEXT
                       NOT
                       NULL,
                       opcion_d
                       TEXT
                       NOT
                       NULL,
                       respuesta_correcta
                       TEXT
                       CHECK (
                       respuesta_correcta
                       IN
                   (
                       'A',
                       'B',
                       'C',
                       'D'
                   )) NOT NULL,
                       FOREIGN KEY
                   (
                       tema_id
                   ) REFERENCES temas
                   (
                       id
                   )
                       )
                   ''')

    # 5. Tabla de Calificaciones (Evaluaciones)
    # Registra qué alumno resolvió qué cuestionario y qué puntaje obtuvo.
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS calificaciones
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       alumno_id
                       INTEGER,
                       tema_id
                       INTEGER,
                       puntaje
                       INTEGER
                       NOT
                       NULL,
                       fecha
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP, -- Se llena sola con la fecha actual
                       FOREIGN
                       KEY
                   (
                       alumno_id
                   ) REFERENCES usuarios
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       tema_id
                   ) REFERENCES temas
                   (
                       id
                   )
                       )
                   ''')

    # Guardamos los cambios y cerramos la conexión para no consumir memoria
    conexion.commit()
    conexion.close()
    print("✅ Base de datos y tablas inicializadas correctamente.")


def crear_admin_por_defecto():
    """
    Crea un usuario administrador por defecto para que podamos iniciar sesión
    la primera vez que abramos el programa.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    # Buscamos si ya existe un admin en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE rol = 'admin'")
    admin_existe = cursor.fetchone()

    if not admin_existe:
        # Si no existe, lo insertamos
        cursor.execute('''
                       INSERT INTO usuarios (nombre_completo, nombre_usuario, password, rol)
                       VALUES ('Administrador del Sistema', 'admin', 'admin123', 'admin')
                       ''')
        conexion.commit()
        print("👤 Usuario administrador creado (Usuario: admin / Contraseña: admin123)")

    conexion.close()


# Este bloque hace que, si ejecutamos ESTE archivo directamente en PyCharm,
# se ejecuten las funciones de arriba.
if __name__ == "__main__":
    inicializar_base_datos()
    crear_admin_por_defecto()

    import sqlite3
    import os

    DB_PATH = os.path.join(os.path.dirname(__file__), "lab_forense.db")


    def conectar():
        """Establece conexión con la base de datos SQLite."""
        return sqlite3.connect(DB_PATH)


    def inicializar_base_datos():
        """Crea la estructura de tablas si no existen."""
        conexion = conectar()
        cursor = conexion.cursor()

        # Tabla de Usuarios
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS usuarios
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nombre_completo
                           TEXT
                           NOT
                           NULL,
                           nombre_usuario
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           password
                           TEXT
                           NOT
                           NULL,
                           rol
                           TEXT
                           CHECK (
                           rol
                           IN
                       (
                           'alumno',
                           'docente',
                           'admin'
                       )) NOT NULL,
                           grupo_id INTEGER NULL
                           )
                       ''')

        # Tabla de Grupos
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS grupos
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nombre_grupo
                           TEXT
                           NOT
                           NULL,
                           docente_id
                           INTEGER,
                           FOREIGN
                           KEY
                       (
                           docente_id
                       ) REFERENCES usuarios
                       (
                           id
                       )
                           )
                       ''')

        # Tabla de Temas
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS temas
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           unidad
                           INTEGER
                           NOT
                           NULL,
                           titulo
                           TEXT
                           NOT
                           NULL,
                           contenido_teorico
                           TEXT
                           NOT
                           NULL
                       )
                       ''')

        # Tabla de Preguntas
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS preguntas
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           tema_id
                           INTEGER,
                           pregunta
                           TEXT
                           NOT
                           NULL,
                           opcion_a
                           TEXT
                           NOT
                           NULL,
                           opcion_b
                           TEXT
                           NOT
                           NULL,
                           opcion_c
                           TEXT
                           NOT
                           NULL,
                           opcion_d
                           TEXT
                           NOT
                           NULL,
                           respuesta_correcta
                           TEXT
                           CHECK (
                           respuesta_correcta
                           IN
                       (
                           'A',
                           'B',
                           'C',
                           'D'
                       )) NOT NULL,
                           FOREIGN KEY
                       (
                           tema_id
                       ) REFERENCES temas
                       (
                           id
                       )
                           )
                       ''')

        # Tabla de Calificaciones
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS calificaciones
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           alumno_id
                           INTEGER,
                           tema_id
                           INTEGER,
                           puntaje
                           INTEGER
                           NOT
                           NULL,
                           fecha
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           FOREIGN
                           KEY
                       (
                           alumno_id
                       ) REFERENCES usuarios
                       (
                           id
                       ),
                           FOREIGN KEY
                       (
                           tema_id
                       ) REFERENCES temas
                       (
                           id
                       )
                           )
                       ''')

        conexion.commit()
        conexion.close()


    def cargar_datos_iniciales():
        import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "lab_forense.db")


def conectar():
  """Establece conexión con la base de datos SQLite."""
  return sqlite3.connect(DB_PATH)


def inicializar_base_datos():
  """Crea la estructura de tablas si no existen."""
  conexion = conectar()
  cursor = conexion.cursor()

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

  cursor.execute("""
                 CREATE TABLE IF NOT EXISTS grupos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_grupo TEXT NOT NULL,
            docente_id INTEGER,
            FOREIGN KEY(docente_id) REFERENCES usuarios(id)
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS temas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidad INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            contenido_teorico TEXT NOT NULL
        )
    """)

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
  """Inserta usuarios, temario y banco de preguntas de opción múltiple."""
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
        """
            INSERT OR IGNORE INTO usuarios (nombre_completo, nombre_usuario, password, rol)
            VALUES (?, ?, ?, ?)
        """,
        (nombre, user, password, rol),
    )

  # 2. Temario Oficial
  temario_oficial = [
      (
          1,
          "Generalidades del Análisis Forense Informático",
          "1.1 Conceptos generales\n"
          "1.2 Importancia\n"
          "1.3 Situación actual\n"
          "1.4 Principios\n"
          "1.5 Estándares\n"
          "   1.5.1 Nivel nacional\n"
          "   1.5.2 Nivel internacional",
      ),
      (
          2,
          "Metodología del Análisis Forense Informático",
          "2.1 Identificación de la evidencia\n"
          "2.2 Adquisición de la evidencia\n"
          "2.3 Preservación de la evidencia\n"
          "2.4 Análisis de la evidencia\n"
          "2.5 Presentación del informe",
      ),
      (
          3,
          "Herramientas de Análisis Forense",
          "3.1 Software Libre de herramientas (Autopsy, Wireshark, CAINE,"
          " ExifTool)\n"
          "3.2 Revisión de Herramientas de recuperación de datos\n"
          "3.3 Programas de Recuperación de Datos Forenses",
      ),
      (
          4,
          "Evidencia y Atribución del Ataque Digital",
          "4.1 Informática forense digital\n"
          "   4.1.1 Análisis y respuesta a incidentes\n"
          "4.2 Evidencias analizadas",
      ),
  ]

  for unidad, titulo, contenido in temario_oficial:
    cursor.execute("SELECT id FROM temas WHERE unidad = ?", (unidad,))
    if not cursor.fetchone():
      cursor.execute(
          """
                INSERT INTO temas (unidad, titulo, contenido_teorico)
                VALUES (?, ?, ?)
            """,
          (unidad, titulo, contenido),
      )

  # 3. Preguntas de opción múltiple para evaluación de la Unidad 1
  cursor.execute("SELECT id FROM temas WHERE unidad = 1")
  tema_1 = cursor.fetchone()

  if tema_1:
    tema_1_id = tema_1[0]
    preguntas_u1 = [
        (
            tema_1_id,
            "¿Cuál es el objetivo principal del análisis forense digital?",
            "Instalar antivirus en el sistema",
            "Identificar, preservar y analizar evidencia digital sin alterarla",
            "Eliminar registros de auditoría",
            "Formatear discos duros",
            "B",
        ),
        (
            tema_1_id,
            "¿Qué principio garantiza que la evidencia mantenga su integridad"
            " desde el hallazgo hasta el juicio?",
            "Cadena de Custodia",
            "Cifrado de disco",
            "Formateo rápido",
            "Ingeniería inversa",
            "A",
        ),
    ]

    for t_id, preg, op_a, op_b, op_c, op_d, resp in preguntas_u1:
      cursor.execute("SELECT id FROM preguntas WHERE pregunta = ?", (preg,))
      if not cursor.fetchone():
        cursor.execute(
            """
                    INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
            (t_id, preg, op_a, op_b, op_c, op_d, resp),
        )

  conexion.commit()
  conexion.close()
  print("✅ Base de datos actualizada con preguntas de evaluación.")


if __name__ == "__main__":
  inicializar_base_datos()
  cargar_datos_iniciales()