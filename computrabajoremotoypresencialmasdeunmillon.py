import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram import Bot

# Configuración del bot
TOKEN = '8430737352:AAF8ilB8sip0***********'
CHAT_ID = 691216915
bot = Bot(token=TOKEN)

# Función para dividir mensajes largos
def dividir_mensaje(mensaje, limite=4000):
    partes = []
    while len(mensaje) > limite:
        corte = mensaje.rfind("\n", 0, limite)
        if corte == -1:
            corte = limite
        partes.append(mensaje[:corte])
        mensaje = mensaje[corte:]
    partes.append(mensaje)
    return partes

async def enviar_alerta():
    try:
        driver = webdriver.Chrome()
        driver.get("https://cl.computrabajo.com/empleos-en-rmetropolitana-hibrido?sal=14")

        ofertas = []
        job_elements = driver.find_elements(By.CLASS_NAME, "box_offer")
        for job in job_elements:
            texto = job.text.strip()
            if texto:
                ofertas.append(texto)

        driver.quit()

        if ofertas:
            mensaje = "📌 Ofertas encontradas:\n\n" + "\n\n".join(ofertas)
        else:
            mensaje = "⚠️ No se encontraron ofertas visibles."

        # Enviar en partes si el mensaje es muy largo
        for parte in dividir_mensaje(mensaje):
            await bot.send_message(chat_id=CHAT_ID, text=parte)

    except Exception as e:
        print(f"Error: {e}")
        await bot.send_message(chat_id=CHAT_ID, text=f"❌ Error en el bot: {e}")

# Ejecutar directamente
asyncio.run(enviar_alerta())
