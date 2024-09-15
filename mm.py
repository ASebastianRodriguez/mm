import pandas as pd
from datetime import datetime
from plyer import notification
from telegram import Bot
import asyncio
import configparser

# Leer el archivo de configuración
config = configparser.ConfigParser(comment_prefixes=('#', '//'))
config.read('token.ini')

# Obtener el token y el chat ID del archivo de configuración
TOKEN = config['DEFAULT']['TOKEN']
CHAT_ID = config['DEFAULT']['CHAT_ID']

# Mensaje que quieres enviar
async def send_message():
    # Crear una instancia del bot
    bot = Bot(token=TOKEN)
    # Enviar el mensaje (usamos await porque es una función asíncrona)
    await bot.send_message(chat_id=CHAT_ID, text=mensaje)
    #print("Mensaje enviado a Telegram con éxito.")

# Cargar el cronograma desde el archivo Excel
file_path = "cronograma_medicamentos.xlsx"

# Obtener la fecha actual
today = datetime.today().date()
#print(f"Fecha actual: {today}")

# MEDICAMENTOS A NO TOMAR
# Recorrer el cronograma para verificar alarmas
# Especificar el nombre de la hoja de cálculo y pestaña
sheet_name = 'notomar'
df = pd.read_excel(file_path, sheet_name=sheet_name)
for index, row in df.iterrows():
    medicamento = row['Medicamento']
    #print(f"Verificando {medicamento}...")
    fecha_inicio = row['Fecha de inicio']
    #print(f"Fecha de inicio 1: {fecha_inicio}")
    fecha_inicio = fecha_inicio.date()
    #print(f"Fecha de inicio 2: {fecha_inicio}")
    fecha_fin = row['Fecha de fin']
    #print(f"Fecha de fin 1: {fecha_fin}")
    fecha_fin = fecha_fin.date()
    #print(f"Fecha de fin 2: {fecha_fin}")

    # Verificar si la fecha actual coincide con la fecha de inicio
    if today == fecha_inicio:
        notification.notify(
            title=f"Inicio de suspensión: {medicamento}",
            message=f"Hoy comienza la suspensión de {medicamento}.",
            timeout=10
        )
        mensaje = f"Hoy comienza la suspensión de {medicamento}."
        asyncio.run(send_message())

    # Verificar si la fecha está entre la fecha de inicio y la fecha de finalización
    if fecha_inicio < today < fecha_fin:
        notification.notify(
            title=f"Suspensión en curso: {medicamento}",
            message=f"Hoy no debes tomar {medicamento}.",
            timeout=10
        )
        mensaje = f"Hoy no debes tomar {medicamento}."
        asyncio.run(send_message())

    # Verificar si la fecha actual coincide con la fecha de finalización
    if today == fecha_fin:
        notification.notify(
            title=f"Fin de suspensión: {medicamento}",
            message=f"Hoy finaliza la suspensión de {medicamento}.",
            timeout=10
        )
        mensaje = f"Hoy finaliza la suspensión de {medicamento}."
        asyncio.run(send_message())

#print("Verificación NO TOMAR completada.")

# MEDICAMENTOS A
# Recorrer el cronograma para verificar alarmas
# Especificar el nombre de la hoja de cálculo y pestaña
sheet_name = 'tomar'
df = pd.read_excel(file_path, sheet_name=sheet_name)
for index, row in df.iterrows():
    medicamento = row['Medicamento']
    #print(f"Verificando {medicamento}...")
    fecha_toma = row['Fecha de toma']
    #print(f"Fecha de toma 1: {fecha_inicio}")
    fecha_toma = fecha_toma.date()
    #print(f"Fecha de toma 2: {fecha_inicio}")

    # Verificar si la fecha actual coincide con la fecha de inicio
    if today == fecha_toma:
        notification.notify(
            title=f"Hoy te toca tomar: {medicamento}",
            message=f"Hoy te toca tomar {medicamento}.",
            timeout=10
        )
        mensaje = f"Hoy te toca tomar {medicamento}."
        asyncio.run(send_message())

#print("Verificación TOMAR completada.")
