import requests
import time

# === CONFIGURACIÓN ===
TOKEN = '7308885337:AAFVZGZnSZq4orsZO4pOvphw-_Taas2RDSw'
CHAT_ID = 'Alertamaipobot'
URL = f'https://api.telegram.org/bot{TOKEN}'
last_update_id = None

# === MÓDULO: SISMOS DE ALTA MAGNITUD ===
def sismos_fuertes():
    url = "https://chilealerta.com/api/query/?user=demo&select=ultimos_sismos_chile&minmagnitude=5"
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            data = response.json()
            eventos = data.get("ultimos_sismos_Chile", [])
            alertas = []
            for sismo in eventos:
                alerta = f"🌍 Sismo {sismo['magnitude']} M cerca de {sismo['reference']} a las {sismo['chilean_time']}"
                alertas.append(alerta)
            return alertas if alertas else ["✅ No hay sismos fuertes recientes."]
    except:
        return ["⚠️ Error al consultar sismos."]
    return ["⚠️ No se pudo obtener datos sísmicos."]

# === MÓDULO: LLUVIAS INTENSAS ===
def lluvia_buin():
    # Simulación de lluvia acumulada (puedes conectar a DGA si tienes API Key)
    try:
        url = "https://api.gael.cloud/general/public/clima"
        response = requests.get(url, timeout=10)
        if response.ok:
            datos = response.json()
            for ciudad in datos:
                if "buin" in ciudad['Estacion'].lower():
                    lluvia = float(ciudad.get('Precipitacion', '0'))
                    if lluvia > 30:
                        return f"🌧️ Alerta: Lluvia intensa en Buin ({lluvia} mm acumulados). Revisa rutas de evacuación."
                    else:
                        return f"✅ Lluvia moderada en Buin ({lluvia} mm). Sin riesgo inmediato."
        return "⚠️ No se pudo obtener datos de lluvia."
    except:
        return "⚠️ Error al consultar lluvia."

# === MÓDULO: RESPUESTA INTELIGENTE ===
def responder(texto):
    texto = texto.lower()
    if "sismo" in texto:
        return "\n".join(sismos_fuertes())
    elif "lluvia" in texto or "agua" in texto:
        return lluvia_buin()
    elif "hola" in texto or "buenas" in texto:
        return "👋 ¡Hola Ricardo! ¿Quieres saber sobre sismos o lluvias en Buin?"
    else:
        return "🤖 Puedo informarte sobre sismos y lluvias intensas en Buin. Escribe 'sismo' o 'lluvia'."

# === MÓDULO: ENVÍO DE MENSAJE ===
def send_message(chat_id, text):
    requests.post(f'{URL}/sendMessage', data={'chat_id': chat_id, 'text': text})

# === MÓDULO: ESCUCHA DE MENSAJES ===
def get_updates():
    global last_update_id
    response = requests.get(f'{URL}/getUpdates?offset={last_update_id}')
    return response.json()

# === LOOP PRINCIPAL ===
def main():
    global last_update_id
    print("🤖 Bot de monitoreo activo...")
    while True:
        updates = get_updates()
        if 'result' in updates:
            for update in updates['result']:
                last_update_id = update['update_id'] + 1
                try:
                    chat_id = update['message']['chat']['id']
                    user_text = update['message']['text']
                    print(f"📨 Mensaje recibido: {user_text}")
                    respuesta = responder(user_text)
                    send_message(chat_id, respuesta)
                except KeyError:
                    continue
        time.sleep(5)

if __name__ == "__main__":
    main()
