import socket
import threading
import random
from datetime import datetime, timedelta

FORMATO = 'utf-8'

hora_cliente = None
desvio = random.uniform(-120, 120)

socket_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cli.connect(("192.168.0.4", 80))
print('[CLIENTE] Conexão estabelecida')

def calcular_diferenca(hora_servidor_msg):
  global hora_cliente
  hora_servidor = datetime.strptime(hora_servidor_msg, "%Y-%m-%d %H:%M:%S")
  hora_cliente = datetime.now() + timedelta(minutes=desvio)
  print(f"[CLIENTE] Tempo local (com desvio de {desvio:.2f}min): {hora_cliente.time()}")
  return (hora_cliente - hora_servidor).total_seconds()

def ajustar():
  global hora_cliente
  global desvio
  hora_servidor_msg = socket_cli.recv(1024).decode(FORMATO)
  print('[RECEBENDO] Hora do servidor :', hora_servidor_msg)
  diferenca_tempo = calcular_diferenca(hora_servidor_msg)
  print('[ENVIANDO] Diferença de tempo em segundos para servidor:', diferenca_tempo)
  socket_cli.send(str(diferenca_tempo).encode(FORMATO))   
  ajuste_seg_msg = socket_cli.recv(1024).decode()  
  ajuste_segundos = float(ajuste_seg_msg)
  print('[RECEBENDO] Ajuste em segundos obtido pelo servidor :', ajuste_seg_msg)
  hora_cliente = datetime.now() + timedelta(minutes=desvio, seconds=ajuste_segundos)
  print(f'[Cliente] Hora ajustada em: {ajuste_segundos} segundos')
  print(f'[Cliente] Hora atualizada: {hora_cliente}')
  socket_cli.close()

def iniciar():
  thread1 = threading.Thread(target=ajustar)
  thread1.start()

iniciar()