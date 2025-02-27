import cv2
import mysql.connector
import json
from pyzbar.pyzbar import decode
from datetime import datetime
import time
from flask import Flask, Response, render_template, jsonify
from flask_cors import CORS  # Importamos CORS
import numpy as np  # Aquí se importa numpy

# Configuración del servidor Flask
app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas de la aplicación

# Conexión a la base de datos
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Seguridad2025",
            database="gestion_urbanizacion"
        )
    except mysql.connector.Error as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return None

# Función para registrar al visitante
def registrar_visitante(id_usuario, codigo_familia):
    try:
        conn = connect_db()
        if conn is None:
            return False, "❌ Error de conexión a la BD"
        
        cursor = conn.cursor()

        cursor.execute("""
            SELECT hora_entrada FROM visitantes WHERE id_usuario = %s ORDER BY hora_entrada DESC LIMIT 1
        """, (id_usuario,))
        result = cursor.fetchone()

        if result:
            ultima_entrada = result[0]
            hora_actual = datetime.now()

            if (hora_actual - ultima_entrada).total_seconds() < 10:
                return False, "❌ QR repetido, espera 10s"

        hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO visitantes (id_usuario, codigo_familia, hora_entrada)
            VALUES (%s, %s, %s)
        """, (id_usuario, codigo_familia, hora_entrada))
        conn.commit()

        return True, "✅ Código Aceptado"

    except mysql.connector.Error:
        return False, "❌ Error al registrar en la BD"

# Procesar QR
def procesar_qr(data):
    try:
        qr_data = json.loads(data)
        return qr_data['id_usuario'], qr_data['codigo_familia']
    except Exception:
        return None, None

# Captura de video y streaming
cap = cv2.VideoCapture(0)

message = ""  
message_color = (0, 255, 0)  
message_timer = 0  
qr_status = "waiting"  # Variable global para el estado

def generate_frames():
    global message, message_color, message_timer, qr_status  # Usamos la variable global

    last_scanned_time = None  
    qr_detected_last = False  

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        decoded_objects = decode(frame)
        qr_detected = False

        for obj in decoded_objects:
            data = obj.data.decode('utf-8')

            id_usuario, codigo_familia = procesar_qr(data)
            
            if id_usuario and codigo_familia and not qr_detected_last:
                current_time = time.time()
                if last_scanned_time is None or current_time - last_scanned_time >= 1:
                    valid, msg = registrar_visitante(id_usuario, codigo_familia)
                    message = msg  
                    message_color = (0, 255, 0) if valid else (0, 0, 255)  
                    message_timer = time.time()  
                    last_scanned_time = current_time  
                    qr_detected_last = True
                    qr_status = "accepted" if valid else "rejected"  # Cambiamos el estado al aceptado o rechazado
                else:
                    message = "❌ Espera 1s antes de escanear de nuevo"
                    message_color = (0, 0, 255)  

                qr_detected = True

            points = obj.polygon
            if len(points) == 4:
                points = [(int(point[0]), int(point[1])) for point in points]
                cv2.polylines(frame, [np.array(points)], True, (0, 0, 255), 2)

        # Mostrar mensaje en pantalla
        if message and (time.time() - message_timer < 2):
            cv2.putText(frame, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, message_color, 2)
        else:
            message = ""

        if not qr_detected and qr_detected_last:
            qr_detected_last = False  

        # Mostrar el frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Endpoint para el estado de los códigos QR
@app.route('/status')
def status():
    global qr_status
    qr_status = "waiting"  # Restablecemos el estado a "waiting" cuando se consulta
    return jsonify({'status': qr_status, 'message': message})


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
