"""
Resposta para a pergunta A:

Sim. A solução criada é extensível para uma matriz com tamanho aleatório.
Isso acontece pois todos os seus movimentos são aleatórios, mesmo que priorizando certas posições.
Desta forma, sempre mapeia os movimentos possíveis, dando prioridade aos que não foram vizitados.
Portanto, qualquer matriz onde as paredes estiverem somente na parte externa irá funcionar, mesmo que uma matriz m x n
tenha m e n diferentes.
O aspirador robô pode alcançar todos os locais, porém, pode demorar a percorrer todo o percurso. 
"""

import random
import numpy as np
from exibir import exibir

# Definição dos estados das células da grade
LIMPO = 0  # limpo (azul)
PAREDE = 1  # parede (verde)
SUJO = 2  # sujo (amarelo)

# Configuração da matriz
m = 6
n = m

# Criação da matriz com paredes nas bordas e sujeira aleatória no interior
matriz = np.random.choice([0, 2], size=(m - 2, n - 2))
matriz = np.pad(matriz, pad_width=1, constant_values=1)

# Posição inicial aleatória do agente
posAPAy = random.randint(1, m - 2)
posAPAx = random.randint(1, n - 2)

exibir(matriz, posAPAx, posAPAy)

# Inicialização do estado do agente
posicoes_visitadas = set()
pilha_movimentos = []  # Pilha para armazenar os movimentos e garantir exploração total

def agenteReativoSimples(percepcao):
    """
    Função que define o comportamento do agente reativo simples.
    :param percepcao: Tupla contendo a posição (x, y) e o status (limpo ou sujo).
    :return: Uma das ações possíveis ('acima', 'abaixo', 'esquerda', 'direita', 'aspirar').
    """
    (x, y), status = percepcao
    
    if status == SUJO:
        return 'aspirar'
    
    movimentos_possiveis = obter_movimentos_possiveis(matriz, y, x)
    random.shuffle(movimentos_possiveis)  # Embaralha para evitar loops previsíveis
    
    for movimento in movimentos_possiveis:
        dy, dx = movimento
        nova_posicao = (y + dy, x + dx)
        if nova_posicao not in posicoes_visitadas:
            pilha_movimentos.append((dy, dx))
            return 'acima' if dy == -1 else 'abaixo' if dy == 1 else 'esquerda' if dx == -1 else 'direita'
    
    if pilha_movimentos:  # Se não há novos movimentos, desfaz último passo para buscar outro caminho
        dy, dx = pilha_movimentos.pop()
        return 'acima' if dy == 1 else 'abaixo' if dy == -1 else 'esquerda' if dx == 1 else 'direita'
    
    return None  # Caso extremo em que não há movimentos possíveis

def sensorSujeira(matriz, linha, coluna):
    """Verifica se a posição atual está suja."""
    return matriz[linha][coluna] == SUJO

def aspirar(matriz, linha, coluna):
    """Limpa a posição atual da matriz."""
    matriz[linha][coluna] = LIMPO
    return matriz

def obter_movimentos_possiveis(matriz, linha, coluna):
    """Retorna uma lista de movimentos possíveis (cima, baixo, esquerda, direita) evitando paredes."""
    movimentos = []
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita
    
    for dl, dc in direcoes:
        nova_linha, nova_coluna = linha + dl, coluna + dc
        if 0 <= nova_linha < len(matriz) and 0 <= nova_coluna < len(matriz[0]):
            if matriz[nova_linha][nova_coluna] != PAREDE:
                movimentos.append((dl, dc))
    
    return movimentos

# Loop principal (para percorrer toda a área independentemente da sujeira)
while True:
    # Cria a percepção do ambiente (posição do agente e estado do local)
    percepcao = ((posAPAx, posAPAy), matriz[posAPAy][posAPAx])
    
    # Obtém a ação do agente com base na percepção
    acao = agenteReativoSimples(percepcao)
    
    if acao == 'aspirar':
        matriz = aspirar(matriz, posAPAy, posAPAx)
        print("Posição limpa:", posAPAy, posAPAx)
    
    elif acao == 'acima':
        posAPAy -= 1
    elif acao == 'abaixo':
        posAPAy += 1
    elif acao == 'esquerda':
        posAPAx -= 1
    elif acao == 'direita':
        posAPAx += 1
    else:        
        pilha_movimentos.clear()  # Reinicia a pilha de movimentos para tentar novos caminhos
        posicoes_visitadas.clear()
        continue
    
    posicoes_visitadas.add((posAPAy, posAPAx))
    
    # Exibe o estado atualizado
    exibir(matriz, posAPAx, posAPAy)