import logging
import qrcode
import mysql.connector
import json
from io import BytesIO
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# 🔹 Configuración de logs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

# 🔹 Token del bot de Telegram
TOKEN = "7336361417:AAGF10BBLqAyIzqUqYAoVIsI1NuT76HPx6U"

# 🔹 Conexión a MySQL
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Seguridad2025",
            database="gestion_urbanizacion"
        )
    except mysql.connector.Error as e:
        logger.error(f"❌ Error de conexión a la base de datos: {e}")
        return None

# 🔹 Guardar usuario en la BD (solo se ejecutará una vez)
def guardar_usuario(user_id, id_persona, codigof):
    try:
        conn = connect_db()
        if conn is None:
            logger.error("❌ Error: No se pudo conectar a la base de datos.")
            return False
        
        cursor = conn.cursor()

        # Verificar si el usuario ya está registrado
        cursor.execute("SELECT idtel, codigo_familia FROM personas WHERE id = %s", (id_persona,))
        existing_user = cursor.fetchone()

        if not existing_user:
            logger.error(f"❌ Error: El ID de persona {id_persona} no existe en la base de datos.")
            cursor.close()
            conn.close()
            return False  # El ID de persona no existe en la base de datos.

        # Verificar si el código de familia coincide
        if existing_user[1] != codigof:
            logger.error(f"❌ Error: El código de familia {codigof} no coincide con el registrado en la base de datos.")
            cursor.close()
            conn.close()
            return False  # El código de familia no coincide.

        # Solo asignamos el ID de Telegram si no se ha asignado previamente
        if existing_user[0] is None:
            cursor.execute(
                "UPDATE personas SET idtel = %s WHERE id = %s AND codigo_familia = %s",
                (user_id, id_persona, codigof)
            )
            conn.commit()
            logger.info(f"✅ Usuario con ID {id_persona} y código de familia {codigof} validado correctamente.")
            cursor.close()
            conn.close()
            return True
        else:
            logger.info(f"✅ El usuario con ID {id_persona} ya tiene asignado un ID de Telegram.")
            cursor.close()
            conn.close()
            return False  # El usuario ya tiene un ID de Telegram asignado.

    except mysql.connector.Error as e:
        logger.error(f"❌ Error al validar usuario en la base de datos: {e}")
        return False

# 🔹 Guardar QR en la base de datos de forma automática y generar JSON
def guardar_qr(user_id, codigo_familia):
    try:
        conn = connect_db()
        if conn is None:
            logger.error("❌ Error de conexión a la base de datos.")
            return False
        
        cursor = conn.cursor()

        # Obtener el ID de la persona con ese ID de Telegram y el código de familia
        cursor.execute("SELECT id, codigo_familia FROM personas WHERE idtel = %s", (user_id,))
        result = cursor.fetchone()

        if not result:
            logger.error("❌ El usuario no está validado.")
            cursor.close()
            conn.close()
            return False  # El usuario no está validado

        id_persona, codigo_familia = result  # Extraemos el ID y el código de familia

        # Obtener la hora actual para la generación del QR
        hora_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Definir una hora de vencimiento (por ejemplo, 1 día después de la generación)
        hora_vencimiento = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

        # Insertar el QR en la tabla qrs_generados
        cursor.execute("""
            INSERT INTO qrs_generados (id_usuario, codigo_familia, hora_generacion, hora_vencimiento)
            VALUES (%s, %s, %s, %s)
        """, (id_persona, codigo_familia, hora_generacion, hora_vencimiento))
        conn.commit()

        # Crear el JSON con los datos necesarios para el QR
        qr_data = {
            "id_usuario": id_persona,
            "codigo_familia": codigo_familia,
            "hora_generacion": hora_generacion,
            "hora_vencimiento": hora_vencimiento
        }

        # Generar el código QR con el JSON
        qr_json = json.dumps(qr_data)
        bio = generar_qr(qr_json)  # Usamos la función generada previamente para generar el QR

        logger.info(f"✅ QR generado para el usuario {id_persona} con código de familia {codigo_familia}")
        
        cursor.close()
        conn.close()
        
        return bio  # Devolvemos la imagen del QR generada para enviarla al usuario

    except mysql.connector.Error as e:
        logger.error(f"❌ Error al guardar QR en la base de datos: {e}")
        return False

# 🔹 Generar QR
def generar_qr(codigo: str) -> BytesIO:
    qr = qrcode.make(codigo)
    bio = BytesIO()
    qr.save(bio, format="PNG")
    bio.seek(0)
    return bio

# 🔹 Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_text(f"👋 ¡Hola {user.first_name}! Usa /menu para comenzar.")

# 🔹 Comando /menu para elegir qué hacer
async def menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("✅ Validar Usuario", callback_data="validar")],
        [InlineKeyboardButton("📲 Generar QR", callback_data="generar_qr")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📌 ¿Qué quieres hacer?", reply_markup=reply_markup)

# 🔹 Comando /validar para registrar el usuario
async def validar(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.effective_user.id
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usa el formato: /validar <ID_PERSONA> <CODIGO_FAMILIA>")
            return
        
        id_persona = context.args[0]
        codigof = context.args[1]
        
        if guardar_usuario(user_id, id_persona, codigof):
            await update.message.reply_text("✅ ¡Usuario validado correctamente!")
        else:
            await update.message.reply_text("❌ No se pudo validar al usuario.")
    except Exception as e:
        logger.error(f"❌ Error al validar usuario: {e}")
        await update.message.reply_text("❌ Ocurrió un error al validar el usuario.")

# 🔹 Manejo del menú
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "validar":
        await query.message.reply_text("📌 Usa el comando: `/validar <ID> <CODIGO_FAMILIA>` para registrarte.")
    elif query.data == "generar_qr":
        user_id = update.effective_user.id

        # Obtener el código de familia del usuario
        conn = connect_db()
        if conn is None:
            await query.message.reply_text("❌ No se pudo conectar a la base de datos.")
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT codigo_familia FROM personas WHERE idtel = %s", (user_id,))
        result = cursor.fetchone()

        if not result:
            await query.message.reply_text("⚠️ El usuario no está validado. Usa el comando /validar para validar tu cuenta.")
            return

        codigo_familia = result[0]

        # Guardar el QR en la base de datos y generar el QR con los datos JSON
        bio = guardar_qr(user_id, codigo_familia)
        if bio:
            await query.message.reply_photo(photo=bio, caption=f"✅ QR generado para el código de familia: {codigo_familia}")
        else:
            await query.message.reply_text("⚠️ No se pudo generar el QR. Inténtalo de nuevo más tarde.")

# 🔹 Configurar el bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("validar", validar))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("✅ Bot de Telegram en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
