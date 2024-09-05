import sqlite3


def conectar_db():
    return sqlite3.connect('../database/sistema_reservas.db')


def insertar_usuario(nombre,email):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO usuarios (nombre, email)
        VALUES (?, ?)
    ''', (nombre, email))

    conn.commit()
    conn.close()

    print(f"Usuario {nombre} agregado correctamente.")


def ver_horarios_disponibles():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM horarios_disponibles')
    horarios = cursor.fetchall()
    conn.close()

    if horarios:
        print("Horarios Disponibles:")
        for horario in horarios:
            print(f"ID: {horario[0]}, Fecha: {horario[1]}, Inicio: {horario[2]}, Fin: {horario[3]}")
    else:
        print("No hay horarios disponibles.")


def hacer_reserva(usuario_id, fecha_reserva, hora_inicio, hora_fin):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM reservas
        WHERE fecha_reserva = ? AND (
            (hora_inicio <= ? AND hora_fin > ?) OR
            (hora_inicio < ? AND hora_fin >= ?)
        )
    ''', (fecha_reserva, hora_inicio, hora_inicio, hora_fin, hora_fin))
    
    conflicto = cursor.fetchone()
    
    if conflicto:
        print("Conflicto de reserva: ya existe una reserva en ese horario.")
    else:
        
        cursor.execute('''
            INSERT INTO reservas (usuario_id, fecha_reserva, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, fecha_reserva, hora_inicio, hora_fin))
        
        conn.commit()
        print("Reserva realizada con éxito.")
    
    conn.close()


def cancelar_reserva(reserva_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si la reserva existe
    cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
    reserva = cursor.fetchone()
    
    if reserva:
        # Eliminar la reserva
        cursor.execute('DELETE FROM reservas WHERE id = ?', (reserva_id,))
        conn.commit()
        print(f"Reserva con ID {reserva_id} cancelada.")
    else:
        print(f"No se encontró ninguna reserva con ID {reserva_id}.")
    
    conn.close()

            


def editar_reserva(reserva_id, nueva_fecha=None, nueva_hora_inicio=None, nueva_hora_fin=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si la reserva existe
    cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
    reserva = cursor.fetchone()
    
    if reserva:
        # Actualizar la reserva solo si se proporcionan los nuevos valores
        nueva_fecha = nueva_fecha if nueva_fecha else reserva[2]
        nueva_hora_inicio = nueva_hora_inicio if nueva_hora_inicio else reserva[3]
        nueva_hora_fin = nueva_hora_fin if nueva_hora_fin else reserva[4]
        
        # Actualizar la reserva
        cursor.execute('''
            UPDATE reservas
            SET fecha_reserva = ?, hora_inicio = ?, hora_fin = ?
            WHERE id = ?
        ''', (nueva_fecha, nueva_hora_inicio, nueva_hora_fin, reserva_id))
        
        conn.commit()
        print(f"Reserva con ID {reserva_id} actualizada.")
    else:
        print(f"No se encontró ninguna reserva con ID {reserva_id}.")
    
    conn.close()
