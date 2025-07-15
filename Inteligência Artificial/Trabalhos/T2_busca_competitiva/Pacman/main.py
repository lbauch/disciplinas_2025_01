from pacman import Pacman
from fantasma import Fantasma
import time

def imprimir_matriz(matriz, pos_pacman, pos_fantasma):
  # Exibe na tela o estado atual do tabuleiro
  for i in range(len(matriz)):
    linha = ""
    for j in range(len(matriz[0])):
      if (i, j) == pos_pacman:
        linha += 'P'
      elif (i, j) == pos_fantasma:
        linha += 'F'
      else:
        linha += matriz[i][j]
    print(linha)
  print("\n" + "-" * 20 + "\n")

# Mapa do jogo (pode ser alterado para qualquer tamanho, formato e posições alteradas)
grade = [
  ['#', '#', '#', '#', '#', '#', '#'],
  ['#', '.', '.', '.', '.', '.', '#'],
  ['#', '.', '#', '.', '.', '.', '#'],
  ['#', '.', '#', '#', '#', '.', '#'],
  ['#', '.', '.', '.', '.', '.', '#'],
  ['#', '#', '#', '#', '#', '#', '#']
]

# Inicialização dos jogadores
pacman = Pacman((2, 1))
fantasma = Fantasma((1, 4))

turno = 0
# Executa o jogo até todas as comidas serem comidas ou Pacman ser pego
while pacman.posicao != fantasma.posicao and any('.' in linha for linha in grade):
  print(f"Turno {turno}")
  imprimir_matriz(grade, pacman.posicao, fantasma.posicao)

  # Movimento do Pacman
  pacman.melhor_movimento(grade, fantasma.posicao)
  if grade[pacman.posicao[0]][pacman.posicao[1]] == '.':
    grade[pacman.posicao[0]][pacman.posicao[1]] = ' '

  # Verifica se Pacman foi capturado
  if pacman.posicao == fantasma.posicao:
    print("O Pacman foi pego!")
    break

  # Fantasma se move na direção do Pacman
  fantasma.melhor_movimento(pacman.posicao, grade)

  # Verifica novamente se Pacman foi capturado
  if pacman.posicao == fantasma.posicao:
    imprimir_matriz(grade, pacman.posicao, fantasma.posicao)
    print("O Pacman foi pego!")
    break

  turno += 1
  time.sleep(0.5)

if pacman.posicao != fantasma.posicao and not any('.' in linha for linha in grade):
  print("O Pacman venceu! Comeu todas as comidas!")
