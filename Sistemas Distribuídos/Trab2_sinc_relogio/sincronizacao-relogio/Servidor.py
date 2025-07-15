import socket
import threading
import numpy as np
from datetime import datetime, timedelta

NUM_CLIENTES = 2
FORMATO = 'utf-8'

conexoes = []
diferencas = []
hora_agora = None

def handle_clientes(conn, addr):
  print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}")
  global conexoes
  conexoes.append((conn, addr))

def verificar_diferencas_horarios():
  global conexoes
  global hora_agora
  for conexao in conexoes:
    print(f"[ENVIANDO] Enviando t servidor para {conexao[1]}")
    hora_agora = datetime.now()
    hora_str = hora_agora.strftime('%Y-%m-%d %H:%M:%S')
    conexao[0].send(hora_str.encode(FORMATO))
    print(f"[RECEBENDO] Recebendo diferença de tempo em segudos de {conexao[1]}")
    dif_tempo_str = conexao[0].recv(1024).decode(FORMATO)
    diferencas.append(float(dif_tempo_str))

def enviar_media_dif(media):
  global conexoes
  print(f'[SERVIDOR] Média das diferenças (em segundos): {media}')
  for i in range(len(conexoes)):
    total_diferenca = media - diferencas[i]
    print(f'[ENVIANDO] conexão: {conexoes[i][1]} : Ajuste: {diferencas[i]}')
    conexoes[i][0].send(str(total_diferenca).encode(FORMATO))

def start():
  global hora_agora
  socket_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket_serv.bind(("192.168.0.4", 80))
  socket_serv.listen(NUM_CLIENTES)
  print('[SERVIDOR] Aguardando conexões...')
  while True:
    conn, addr = socket_serv.accept()
    thread = threading.Thread(target=handle_clientes, args=(conn, addr))
    thread.start()
    if len(conexoes) == NUM_CLIENTES - 1:
      break
  verificar_diferencas_horarios()  
  media = np.mean(diferencas)
  enviar_media_dif(media)
  hora_agora = datetime.now() + timedelta(seconds=media)
  print(f'[SERVIDOR] Hora atualizada: {hora_agora}')
  return()

start()