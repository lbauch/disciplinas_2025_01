"""
Resposta para a pergunta B:

Sim. Com este código foi possível fazer a limpeza de uma forma eficiente, considerando 
a limpeza somente em locais que estão sujos, tomando o mínimo de passos possíveis.
"""

import random
import time
from collections import deque

import numpy as np
from exibir import exibir

# Linhas da matriz
m = 6
# Colunas da matriz
n = m

# Definir posição inicial fixa (1,1)
posAPAy, posAPAx = 1, 1

# matriz interna sem borda
matriz = np.random.choice([0, 2], size=(m-2, n-2))
# bordas
matriz = np.pad(matriz, pad_width=1, constant_values=1)

# Manter registro de células visitadas e limpas
celulas_visitadas = set()
# Manter um caminho para seguir (resultado da busca)
caminho_atual = []

# Função para verificar se há sujeira na sala
def checkObj(sala):
    for i in range(1, 5):
        for j in range(1, 5):
            if sala[i, j] == 2:  # Se encontrar alguma sujeira
                return 1
    return 0

# Função para encontrar células sujas usando BFS (Breadth-First Search)
def encontrar_celula_suja(matriz, pos_x, pos_y):
    # Se a célula atual estiver suja, retornar a posição atual
    if matriz[pos_x, pos_y] == 2:
        return [(pos_x, pos_y)]
    
    # Inicializar a fila para BFS
    fila = deque([(pos_x, pos_y, [])])  # (x, y, caminho)
    visitados = set([(pos_x, pos_y)])
    
    # Direções possíveis: cima, direita, baixo, esquerda
    direcoes = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while fila:
        x, y, caminho = fila.popleft()
        
        # Verificar todas as direções
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            
            # Verificar se a nova posição está dentro dos limites e não é parede
            if (1 <= nx <= 4 and 1 <= ny <= 4 and 
                matriz[nx, ny] != 1 and 
                (nx, ny) not in visitados):
                
                novo_caminho = caminho + [(nx, ny)]
                
                # Se encontrou uma célula suja, retornar o caminho até ela
                if matriz[nx, ny] == 2:
                    return novo_caminho
                
                # Adicionar à fila e marcar como visitado
                fila.append((nx, ny, novo_caminho))
                visitados.add((nx, ny))
    
    # Se não encontrou células sujas, procurar células não visitadas
    fila = deque([(pos_x, pos_y, [])])  # Reiniciar a busca
    visitados = set([(pos_x, pos_y)])
    
    while fila:
        x, y, caminho = fila.popleft()
        
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            
            if (1 <= nx <= 4 and 1 <= ny <= 4 and 
                matriz[nx, ny] != 1 and 
                (nx, ny) not in visitados):
                
                novo_caminho = caminho + [(nx, ny)]
                
                # Se encontrou uma célula não visitada, retornar o caminho
                if (nx, ny) not in celulas_visitadas:
                    return novo_caminho
                
                fila.append((nx, ny, novo_caminho))
                visitados.add((nx, ny))
    
    # Se todas as células foram visitadas, retornar um caminho vazio
    return []

# Função para converter posição para ação
def posicao_para_acao(pos_atual, prox_pos):
    x_atual, y_atual = pos_atual
    x_prox, y_prox = prox_pos
    
    if x_prox < x_atual:
        return 'acima'
    elif x_prox > x_atual:
        return 'abaixo'
    elif y_prox < y_atual:
        return 'esquerda'
    elif y_prox > y_atual:
        return 'direita'
    
    # Não deve chegar aqui
    return 'aspirar'

# Função do agente baseado em objetivo
def agenteObjetivo(percepcao, objObtido):
    global caminho_atual, celulas_visitadas
    
    # Se o objetivo foi atingido (sala limpa), não fazer nada
    if objObtido == 0:
        return 'NoOp'
    
    posicao_x, posicao_y, status = percepcao
    celulas_visitadas.add((posicao_x, posicao_y))
    
    # Se a posição atual estiver suja, aspirar
    if status == 2:  # 2 representa sujeira
        return 'aspirar'
    
    # Se não tiver um caminho a seguir ou o caminho estiver vazio, calcular novo caminho
    if not caminho_atual:
        caminho_atual = encontrar_celula_suja(matriz, posicao_x, posicao_y)
    
    # Se ainda não tiver caminho, todas as células foram visitadas
    # Neste caso, podemos implementar um padrão de varredura simples
    if not caminho_atual:
        # Padrão de zigue-zague como fallback
        if posicao_x == 1:
            if posicao_y < 4:
                return 'direita'
            else:
                return 'abaixo'
        elif posicao_x == 2:
            if posicao_y > 1:
                return 'esquerda'
            else:
                return 'abaixo'
        elif posicao_x == 3:
            if posicao_y < 4:
                return 'direita'
            else:
                return 'abaixo'
        elif posicao_x == 4:
            if posicao_y > 1:
                return 'esquerda'
            else:
                return 'acima'
        return 'direita'
    
    # Pegar o próximo passo do caminho
    prox_pos = caminho_atual.pop(0)
    
    # Converter a próxima posição em uma ação
    return posicao_para_acao((posicao_x, posicao_y), prox_pos)

# Função para executar a ação do agente
def executarAcao(acao, posicao_x, posicao_y, matriz):
    nova_posicao_x, nova_posicao_y = posicao_x, posicao_y
    
    if acao == 'acima':
        nova_posicao_x = max(1, posicao_x - 1)
    elif acao == 'abaixo':
        nova_posicao_x = min(4, posicao_x + 1)
    elif acao == 'esquerda':
        nova_posicao_y = max(1, posicao_y - 1)
    elif acao == 'direita':
        nova_posicao_y = min(4, posicao_y + 1)
    elif acao == 'aspirar':
        # Aspirar a sujeira na posição atual
        matriz[posicao_x, posicao_y] = 0
    elif acao == 'NoOp':
        # Não fazer nada
        pass
    
    # Verificar se a nova posição é uma parede (valor 1)
    if matriz[nova_posicao_x, nova_posicao_y] == 1:
        # Se for parede, não muda a posição
        return posicao_x, posicao_y, matriz
    
    return nova_posicao_x, nova_posicao_y, matriz

# Simulação do ambiente
def simular(passos=100):
    global matriz, posAPAx, posAPAy
    pontos = 0
    
    for passo in range(passos):
        # Obter percepção atual
        status = matriz[posAPAx, posAPAy]
        percepcao = (posAPAx, posAPAy, status)
        
        # Verificar objetivo
        objObtido = checkObj(matriz)
        
        # Decidir ação com base na percepção e objetivo
        acao = agenteObjetivo(percepcao, objObtido)
        
        # Exibir estado da percepção e ação escolhida
        print(f"Estado da percepcao: {1 if status == 2 else 0} Acao escolhida: {acao}")
        
        # Se a ação for NoOp e o objetivo foi atingido, encerrar
        if acao == 'NoOp' and objObtido == 0:
            print(f"Ponto: -> {pontos}")
            print("Aspirador concluiu a limpeza com sucesso!")
            break
        
        # Executar ação
        posAPAx, posAPAy, matriz = executarAcao(acao, posAPAx, posAPAy, matriz)
        
        # Incrementar pontos
        pontos += 1
        
        # Exibir estado atual
        exibir(matriz, posAPAy, posAPAx)
        
        # Pequena pausa para visualização
        time.sleep(0.1)
    
    # Se saiu do loop sem atingir o objetivo
    if not objObtido == 0:
        print(f"Ponto: -> {pontos}")
        print("Aspirador não conseguiu limpar toda a sala no número de passos definido.")

# Exibir estado inicial
exibir(matriz, posAPAy, posAPAx)
time.sleep(0.1)

# Iniciar simulação
simular(100)