import requests
import urllib3
import os
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def buscar_mencoes_dia(marca, dias_atras=0):
    data_ini = datetime.now() - timedelta(days=dias_atras)
    data_inicio = data_ini.strftime("%Y-%m-%d") + "T00:00:00"
    data_final = data_ini.strftime("%Y-%m-%d") + "T23:59:59"

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={marca}"
        f"&from={data_inicio}"
        f"&to={data_final}"
        f"&sortBy=publishedAt"
        f"&language=pt"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, verify=False, timeout=10)
        data = response.json()

        if data.get("status") != "ok":
            return 0

        return data.get("totalResults", 0)

    except:
        return 0


def enviar_alerta(marca, mencoes_1, data_1, mencoes_2, data_2, variacao):
    mensagem = (
        f"🚨 ALERTA DE PICO 🚨\n\n"
        f"Marca: {marca}\n"
        f"{data_1}: {mencoes_1}\n"
        f"{data_2}: {mencoes_2}\n"
        f"Variação: {variacao:+.1f}%\n"
        f"Hora: {datetime.now().strftime('%H:%M:%S')}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    try:
        requests.post(url, json=payload, timeout=5)
        return True
    except:
        return False


def verificar_crise(marca, limite, d1=1, d2=2):
    data_1 = datetime.now() - timedelta(days=d1)
    data_2 = datetime.now() - timedelta(days=d2)

    label_1 = data_1.strftime("%d/%m/%Y")
    label_2 = data_2.strftime("%d/%m/%Y")

    m1 = buscar_mencoes_dia(marca, d1)
    m2 = buscar_mencoes_dia(marca, d2)

    if m2 == 0:
        variacao = 100 if m1 > 0 else 0
    else:
        variacao = ((m1 - m2) / m2) * 100

    if variacao >= limite:
        enviar_alerta(marca, m1, label_1, m2, label_2, variacao)

    return variacao
