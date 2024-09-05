from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect('../database/sistema_reservas.db')

# Ruta principal para mostrar los horarios disponibles
@app.route('/')
def index():
    conn = conectar_db()
    cursor = conn.cursor()

    # Obtener los horarios disponibles
    cursor.execute('SELECT * FROM horarios_disponibles')
    horarios = cursor.fetchall()
    conn.close()

    # Renderizar la página con los horarios
    return render_template('index.html', horarios=horarios)

# Ruta para manejar el registro de usuarios
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO usuarios (nombre, email)
        VALUES (?, ?)
    ''', (nombre, email))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Ruta para manejar la reserva de un horario
@app.route('/reservar', methods=['POST'])
def reservar():
    horario_id = request.form['horario_id']
    usuario_id = request.form['usuario_id']  # Obtener el ID del usuario desde el formulario
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Obtener el horario seleccionado
    cursor.execute('SELECT * FROM horarios_disponibles WHERE id = ?', (horario_id,))
    horario = cursor.fetchone()
    
    if horario:
        # Verificar conflictos antes de realizar la reserva
        cursor.execute('''
            SELECT * FROM reservas
            WHERE fecha_reserva = ? AND (
                (hora_inicio <= ? AND hora_fin > ?) OR
                (hora_inicio < ? AND hora_fin >= ?)
            )
        ''', (horario[1], horario[2], horario[2], horario[3], horario[3]))
        
        conflicto = cursor.fetchone()
        
        if conflicto:
            conn.close()
            return "Conflicto de reserva: ya existe una reserva en ese horario."
        
        # Realizar la reserva
        cursor.execute('''
            INSERT INTO reservas (usuario_id, fecha_reserva, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, horario[1], horario[2], horario[3]))
        
        conn.commit()
        conn.close()
        return "Reserva realizada con éxito"
    else:
        conn.close()
        return "Error: horario no disponible"

# Ruta para cancelar una reserva
@app.route('/cancelar_reserva/<int:reserva_id>')
def cancelar_reserva(reserva_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
    reserva = cursor.fetchone()
    
    if reserva:
        cursor.execute('DELETE FROM reservas WHERE id = ?', (reserva_id,))
        conn.commit()
        mensaje = f"Reserva con ID {reserva_id} cancelada."
    else:
        mensaje = f"No se encontró ninguna reserva con ID {reserva_id}."
    
    conn.close()
    return mensaje

# Ruta para editar una reserva
@app.route('/editar_reserva/<int:reserva_id>', methods=['POST'])
def editar_reserva(reserva_id):
    nueva_fecha = request.form.get('nueva_fecha')
    nueva_hora_inicio = request.form.get('nueva_hora_inicio')
    nueva_hora_fin = request.form.get('nueva_hora_fin')
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM reservas WHERE id = ?', (reserva_id,))
    reserva = cursor.fetchone()
    
    if reserva:
        nueva_fecha = nueva_fecha if nueva_fecha else reserva[2]
        nueva_hora_inicio = nueva_hora_inicio if nueva_hora_inicio else reserva[3]
        nueva_hora_fin = nueva_hora_fin if nueva_hora_fin else reserva[4]
        
        cursor.execute('''
            UPDATE reservas
            SET fecha_reserva = ?, hora_inicio = ?, hora_fin = ?
            WHERE id = ?
        ''', (nueva_fecha, nueva_hora_inicio, nueva_hora_fin, reserva_id))
        
        conn.commit()
        mensaje = f"Reserva con ID {reserva_id} actualizada."
    else:
        mensaje = f"No se encontró ninguna reserva con ID {reserva_id}."
    
    conn.close()
    return mensaje

if __name__ == '__main__':
    app.run(debug=True)
