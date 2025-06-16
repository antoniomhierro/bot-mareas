import time
import requests
import os
from config import BOT_TOKEN

URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
ARCHIVO_MAREA = 'mareaDeHoy.txt'

def obtener_offset():
    try:
        response = requests.get(f'{URL}/getUpdates')
        response.raise_for_status()
        datos = response.json()
        if datos['result']:
            return datos['result'][-1]['update_id'] + 1
    except Exception as e:
        print(f"⚠️ Error obteniendo offset: {e}")
    return None

def leer_mareas():
    if not os.path.exists(ARCHIVO_MAREA):
        return "⚠️ No se ha generado aún el archivo con las mareas de hoy."
    try:
        with open(ARCHIVO_MAREA, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error leyendo archivo de mareas: {e}"

def enviar_mensaje(chat_id, texto):
    data = {
        'chat_id': chat_id,
        'text': texto,
        'parse_mode': 'HTML'
    }
    try:
        resp = requests.post(f'{URL}/sendMessage', data=data)
        resp.raise_for_status()
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a {chat_id}: {e}")

def escuchar():
    print("🤖 Bot de mareas iniciado...")
    offset = obtener_offset()
    while True:
        try:
            params = {'offset': offset, 'timeout': 30}
            response = requests.get(f'{URL}/getUpdates', params=params, timeout=35)
            response.raise_for_status()
            datos = response.json()

            for update in datos.get('result', []):
                offset = update['update_id'] + 1
                mensaje = update.get('message', {})
                texto = mensaje.get('text', '').lower()
                chat_id = mensaje.get('chat', {}).get('id')

                if texto == '/marea' and chat_id:
                    print("📩 Solicitud de marea recibida.")
                    contenido = leer_mareas()
                    enviar_mensaje(chat_id, contenido)
        except requests.exceptions.ReadTimeout:
            # Timeout esperado para long polling, no es error
            continue
        except Exception as e:
            print("⚠️ Error en el loop principal:", e)
            time.sleep(5)

if __name__ == '__main__':
    escuchar()