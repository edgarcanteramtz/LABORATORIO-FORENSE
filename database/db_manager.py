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