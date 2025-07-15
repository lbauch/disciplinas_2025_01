from utilitarios import eh_valido, mover, distancia_manhattan

class Fantasma:
  def __init__(self, posicao):
    # Inicializa o fantasma com a posição inicial
    self.posicao = posicao

  def melhor_movimento(self, pos_pacman, grade):
    # Movimento simples: anda na direção mais próxima do Pacman
    menor_dist = float('inf')
    melhor_direcao = self.posicao
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for d in direcoes:
      nova_pos = mover(self.posicao, d)
      if eh_valido(nova_pos, grade):
        dist = distancia_manhattan(nova_pos, pos_pacman)
        if dist < menor_dist:
          menor_dist = dist
          melhor_direcao = nova_pos

    # Atualiza posição do fantasma
    self.posicao = melhor_direcao
    return melhor_direcao
