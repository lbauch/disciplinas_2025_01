import requests
import time
import random
import sys
import socket
import os

COLETOR_URL = "http://coletor:5000/leitura"
SENSOR_ID = socket.gethostname()
TIPO_SENSOR = os.environ.get("TIPO_SENSOR", "temperatura").lower()

def gerar_dado():
    valor = {
        "sensor_id": SENSOR_ID,
        "tipo": TIPO_SENSOR
    }

    if TIPO_SENSOR == "temperatura":
        valor["valor"] = round(random.uniform(20, 40), 2)
    elif TIPO_SENSOR == "umidade":
        valor["valor"] = round(random.uniform(40, 80), 2)
    elif TIPO_SENSOR == "vento":
        valor["valor"] = round(random.uniform(0, 15), 2)
    else:
        valor["valor"] = None

    return valor

while True:
    time.sleep(1)

    if random.random() < 0.1:
        raise Exception("Sensor falhou")
        

    dado = gerar_dado()
    try:
        r = requests.post(COLETOR_URL, json=dado)
    except Exception as e:
        print(f"Erro ao enviar dado: {e}", file=sys.stderr)
