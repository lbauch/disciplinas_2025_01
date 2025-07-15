import copy
from utilitarios import eh_valido, mover, obter_comidas, distancia_manhattan

class Pacman:
  def __init__(self, posicao):
    """
    Inicializa o Pacman com sua posição inicial
    """
    self.posicao = posicao

  def heuristica(self, grade, posicao_fantasma):
    """
    Avalia a qualidade do estado atual
    """
    if self.posicao == posicao_fantasma:
      return -10000  # Pacman morreu

    # Distância total até todas as comidas restantes
    comidas = obter_comidas(grade)
    dist_total = sum(distancia_manhattan(self.posicao, c) for c in comidas) if comidas else 0
    # Distância até o fantasma (quanto mais longe, melhor)
    dist_fantasma = distancia_manhattan(self.posicao, posicao_fantasma)

    # Fatores a serem analisados, com pesos diferentes, para balancear os objetivos do pacman
    return -2 * dist_total + 5 * dist_fantasma - 10 * len(comidas)

  def minimax(self, grade, posicao_fantasma, profundidade, turno_pacman, alfa, beta):
    """
    Algoritmo Minimax com poda alfa-beta
    """
    if profundidade == 0 or self.posicao == posicao_fantasma or not obter_comidas(grade):
      return self.heuristica(grade, posicao_fantasma)

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if turno_pacman:
      # Jogada do Pacman (maximizador)
      melhor_valor = float('-inf')
      for d in direcoes:
        nova_pos = mover(self.posicao, d)
        if eh_valido(nova_pos, grade):
          nova_grade = copy.deepcopy(grade)
          if nova_grade[nova_pos[0]][nova_pos[1]] == '.':
            nova_grade[nova_pos[0]][nova_pos[1]] = ' '
          valor = Pacman(nova_pos).minimax(nova_grade, posicao_fantasma, profundidade-1, False, alfa, beta)
          melhor_valor = max(melhor_valor, valor)
          alfa = max(alfa, valor)
          if beta <= alfa:
            break
      return melhor_valor
    else:
      # Jogada do Fantasma (minimizador)
      pior_valor = float('inf')
      for d in direcoes:
        nova_pos_fantasma = mover(posicao_fantasma, d)
        if eh_valido(nova_pos_fantasma, grade):
          valor = self.minimax(grade, nova_pos_fantasma, profundidade-1, True, alfa, beta)
          pior_valor = min(pior_valor, valor)
          beta = min(beta, valor)
          if beta <= alfa:
            break
      return pior_valor

  def melhor_movimento(self, grade, posicao_fantasma, profundidade=4):
    # Escolhe o melhor movimento usando Minimax com profundidade limitada
    melhor_pontuacao = float('-inf')
    melhor_direcao = self.posicao
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for d in direcoes:
      nova_pos = mover(self.posicao, d)
      if eh_valido(nova_pos, grade):
        nova_grade = copy.deepcopy(grade)
        if nova_grade[nova_pos[0]][nova_pos[1]] == '.':
          nova_grade[nova_pos[0]][nova_pos[1]] = ' '
        pontuacao = Pacman(nova_pos).minimax(nova_grade, posicao_fantasma, profundidade-1, False, float('-inf'), float('inf'))
        if pontuacao > melhor_pontuacao:
          melhor_pontuacao = pontuacao
          melhor_direcao = nova_pos

    # Atualiza posição do Pacman
    self.posicao = melhor_direcao
    return melhor_direcao
