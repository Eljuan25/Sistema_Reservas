import sqlite3


conn = sqlite3.connect('sistema_reservas.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    fecha_reserva  TEXT NOT NULL,
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL,
    FOREIGN KEY (usuario_id)  REFERENCES usuarios (id)                                 
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS horarios_disponibles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL           
)
''')

conn.commit()
conn.close()



print("Base de datos creada exitosamente.")