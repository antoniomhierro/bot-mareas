import requests
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo  # Python ≥3.9; si usas <3.9 instala backports.zoneinfo
from pathlib import Path
from config import STORMGLASS_API_KEY

# === CONFIGURACIÓN ===
LAT, LNG = 28.4636, -16.2518  # Santa Cruz de Tenerife
ZONA_HORARIA_LOCAL = ZoneInfo("Atlantic/Canary")

# Directorio base (el mismo donde está el script)
BASE_DIR = Path(__file__).parent
RUTA_FICHERO = BASE_DIR / "mareaDeHoy.txt"

def obtener_mareas():
    hoy = datetime.now(timezone.utc).date()
    manana = hoy + timedelta(days=1)

    start = hoy.isoformat()
    end = manana.isoformat()

    url = (
        f'https://api.stormglass.io/v2/tide/extremes/point'
        f'?lat={LAT}&lng={LNG}&start={start}&end={end}'
    )
    headers = {'Authorization': STORMGLASS_API_KEY}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    datos = response.json()
    eventos = datos.get('data', [])

    mensaje = f"Mareas para hoy ({hoy}):\n"
    for evento in eventos:
        fecha_evento = evento['time'][:10]
        if fecha_evento != hoy.isoformat():
            continue

        tipo = evento['type'].capitalize()
        # parsear la hora UTC y convertir a local canaria
        hora_utc = datetime.fromisoformat(evento['time'].replace('Z', '+00:00'))
        hora_local = hora_utc.astimezone(ZONA_HORARIA_LOCAL)
        hora_str = hora_local.strftime('%H:%M')

        altura = round(evento['height'], 2)
        mensaje += f"- {tipo} a las {hora_str} hora canaria ({altura} m)\n"

    if mensaje.strip().endswith(':'):
        mensaje += "No hay datos de mareas disponibles para hoy.\n"

    return mensaje

def guardar_en_archivo(texto):
    # Asegurarse de que la carpeta existe (aunque aquí es la del script)
    RUTA_FICHERO.parent.mkdir(parents=True, exist_ok=True)
    # Abrir en modo 'w' creará el fichero si no existe
    with open(RUTA_FICHERO, 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f"✅ Datos guardados en: {RUTA_FICHERO}")

if __name__ == '__main__':
    try:
        texto = obtener_mareas()
        guardar_en_archivo(texto)
    except Exception as e:
        print("❌ Error:", e)
