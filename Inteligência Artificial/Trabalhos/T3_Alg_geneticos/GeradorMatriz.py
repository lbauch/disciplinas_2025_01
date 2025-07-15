import random
import numpy as np

class GeradorMatriz():

  def __init__(self, linhas, colunas):
    self.linhas = linhas
    self.colunas = colunas
    self.matriz = []
    self.matriz_distancias = []
    self.roleta = self._gerar_roleta()

  def _gerar_roleta(self):
    roleta = []
    for i in range(1, 11):
      for _ in range(i):
        roleta.append(11 - i)
    self.roleta = roleta

  def _gerar_linha(self):
    """
    Gera cada linha da matriz, com números aleatórios entre 1 e o número máximo de colunas da matriz.
    """
    # Cria uma lista com números de 1 até o máximo de colunas e embaralha estes números.
    numeros_disponiveis = list(range(1, self.colunas + 1))
    random.shuffle(numeros_disponiveis)  # embaralha os números
    # 
    linha = []
    for _ in range(self.colunas):
      numero = numeros_disponiveis.pop()
      linha.append(numero)
    return linha

  @staticmethod
  def _calcular_distancias_linha(x1, y1, x2, y2):
    """
    Calcula a distância euclidiana entre 2 pontos.

    Args:
      x1 (float): valor de x do primeiro ponto.
      y1 (float): valor de y do primeiro ponto.
      x2 (float): valor de x do segundo ponto.
      y2 (float): valor de y do segundo ponto.
    """
    return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** (1/2)

  def gerar_matriz(self):
    """
    Gera a matriz com o nr de linhas e colunas, gerando uma linha de cada vez
    preenchendo-a com valores aleatórios entre 1 e o nr de colunas, para cada linha.
    """
    for _ in range(self.linhas):
      self.matriz.append(self._gerar_linha())

  def calcular_distancias(self, valores_x, valores_y):
    """
    Calcula as distâncias euclidianas entre pontos consecutivos em cada linha da matriz e
    adiciona essas distâncias a uma nova matriz de distâncias.

    Para cada linha em `self.matriz`, a função itera sobre os pontos (índices) definidos na linha.
    Usando os `valores_x` e `valores_y` fornecidos, ela recupera as coordenadas (x, y) de cada ponto.
    A distância entre um ponto e o próximo é calculada. Além disso, a distância entre
    o último ponto da linha e o primeiro ponto da mesma linha também é calculada para fechar o "caminho".

    As distâncias calculadas para cada linha são armazenadas como uma lista em `self.matriz_distancias`.

    Args:
      valores_x (list): Uma lista contendo as coordenadas x dos pontos.
                          O índice do ponto na linha da matriz corresponde ao índice
                          nesta lista (ajustado por -1, pois os índices da matriz
                          iniciam em 1).
      valores_y (list): Uma lista contendo as coordenadas y dos pontos.
                          O índice do ponto na linha da matriz corresponde ao índice
                          nesta lista (ajustado por -1, pois os índices da matriz
                            iniciam em 1).
    """
    for linha in self.matriz:
      distancias_linha = []
      for i in range(len(linha) - 1):
        x1 = valores_x[linha[i] - 1]
        y1 = valores_y[linha[i] - 1]
        x2 = valores_x[linha[i + 1] - 1]
        y2 = valores_y[linha[i + 1] - 1]
        distancias_linha.append(
          float(self._calcular_distancias_linha(x1, y1, x2, y2))
        )
      distancias_linha.append(
        float(
          self._calcular_distancias_linha(
            valores_x[linha[self.colunas - 1] - 1], valores_y[linha[self.colunas - 1] - 1], valores_x[linha[0] - 1], valores_y[linha[0] - 1]
          )
        )
      )
      self.matriz_distancias.append(distancias_linha)

  def ordenar_matriz(self):
    """
    Ordena a matriz por linha, considerando a soma das distâncias de cada linha.
    """
    distancias_aptidao = np.sum(self.matriz_distancias, axis=1)
    indices = np.argsort(distancias_aptidao)[::-1]
    matriz_np = np.array(self.matriz_distancias)
    self.matriz_distancias = matriz_np[indices][:self.linhas // 2].tolist()

  def selecionar_pais(self):
    """
    Seleciona os índices que serão utilizados como pais (geradores).

    Returns:
      tuple[int, int]: Uma tupla contendo os índices do pai1 e pai2
      que serão utilizados para gerar os filhos
    """
    indice_pai1 = random.choice(self.roleta) - 1
    indice_pai2 = random.choice(self.roleta) - 1
    while indice_pai1 == indice_pai2:
      indice_pai2 = random.choice(self.roleta) - 1
    return indice_pai1, indice_pai2