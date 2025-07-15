def eh_valido(pos, matriz):
  """
  Verifica se a posição está dentro da matriz e não é uma parede
  """
  x, y = pos
  return 0 <= x < len(matriz) and 0 <= y < len(matriz[0]) and matriz[x][y] != '#'

def mover(pos, direcao):
  """
  Retorna nova posição após aplicar movimento
  """
  return (pos[0] + direcao[0], pos[1] + direcao[1])

def distancia_manhattan(a, b):
  """
  Calcula a distância Manhattan entre dois pontos
  """
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def obter_comidas(matriz):
  """
  Retorna lista de posições com comida
  """
  return [(i, j) for i in range(len(matriz)) for j in range(len(matriz[0])) if matriz[i][j] == '.']
