import math
import random
import numpy as np
import matplotlib.pyplot as plt

# função para carregar o arquivo cidades.mat
def carregar_cidades(arquivo):
    return np.loadtxt(arquivo)

# função para gerar a matriz 20x20, com cada linha indo de 1 a 20 de forma aleatória
def gerar_matriz_caminhos(tamanho):
  matriz = []
  for _ in range(tamanho):
    linha = list(range(1, 21))
    random.shuffle(linha)
    matriz.append(linha)
  return matriz

# função para copiar a matriz_caminhos e adicionar uma coluna no final que é a cópia da primeira coluna
def gerar_matriz_caminhos_com_puxadinho(matriz_caminhos):
  matriz = []
  for linha in matriz_caminhos:
    nova_linha = linha + [linha[0]]
    matriz.append(nova_linha)
  return matriz

#função que gera uma matriz do calculo de distância baseado no arquivo cidades.mat
def gerar_matriz_distancias(matriz_caminhos, dados):
  matriz = []
  for caminho in matriz_caminhos:
      nova_linha = []
      for i in range(len(caminho) - 1):
          pos1 = caminho[i] - 1
          pos2 = caminho[i + 1] - 1
          x1, y1 = dados[0][pos1], dados[1][pos1]
          x2, y2 = dados[0][pos2], dados[1][pos2]
          dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
          nova_linha.append(dist)
      matriz.append(nova_linha)
  return matriz

# função que gera uma matriz com uma coluna, onde cada linha é a soma total da matriz_distâncias
def gerar_matriz_custos(matriz_distancias):
  matriz = []
  for linha in matriz_distancias:
    soma_linha = sum(linha)
    matriz.append([soma_linha])
  return matriz

# função que ordena as matrizes levando em consideração a matriz custos
def ordenar_por_custo(matriz_distancias, matriz_custos, matriz_caminhos):
    n = len(matriz_custos)
    for i in range(n):
        for j in range(0, n - i - 1):
            if matriz_custos[j] > matriz_custos[j + 1]:
                matriz_custos[j], matriz_custos[j + 1] = matriz_custos[j + 1], matriz_custos[j]
                matriz_distancias[j], matriz_distancias[j + 1] = matriz_distancias[j + 1], matriz_distancias[j]
                matriz_caminhos[j], matriz_caminhos[j + 1] = matriz_caminhos[j + 1], matriz_caminhos[j]
    return matriz_distancias, matriz_custos, matriz_caminhos

# função para selecionar os pais através da roleta
def selecionar_pais_roleta(roletas):
    pai1 = random.choice(roletas) - 1
    pai2 = random.choice(roletas) - 1
    while pai1 == pai2:
        pai2 = random.choice(roletas) - 1
    return pai1, pai2

# função  que faz a recombinação, e retorna os dois filhos gerados através dos pais
def recombinacao(pai1, pai2):
    filho1 = pai1.copy()
    filho2 = pai2.copy()
    pos = random.randint(0, 19)
    filho1[pos], filho2[pos] = filho2[pos], filho1[pos]

    def corrigir_duplicados(filho1, filho2, pos):
        valor_inserido = filho1[pos]

        while filho1.count(valor_inserido) > 1:
            for i in range(len(filho1)):
                if i != pos and filho1[i] == valor_inserido:
                    novo_valor = filho2[i]
                    filho1[i] = novo_valor
                    filho2[i] = valor_inserido
                    valor_inserido = novo_valor
                    pos = i
                    break

    corrigir_duplicados(filho1, filho2, pos)

    return filho1, filho2

# função que faz a mutação, onde escolhe duas posições aleatórias do cromossomo, e inverte os valores
def mutacao(cromossomo):
    filho = cromossomo.copy()
    i, j = random.sample(range(len(filho)), 2)
    filho[i], filho[j] = filho[j], filho[i]
    return filho

# função para imprimir uma matriz no console
def imprimir_matriz(titulo, matriz):
    print(f"--------------- {titulo}")
    for linha in matriz:
        print(linha)

def funcao_principal(matriz_caminhos):
    cidades = carregar_cidades('cidades.mat')
    #imprimir_matriz("cidades", cidades)

    #imprimir_matriz("matriz_caminhos", matriz_caminhos)

    matriz_caminhos_com_puxadinho = gerar_matriz_caminhos_com_puxadinho(matriz_caminhos)
    #imprimir_matriz("matriz_caminhos_com_puxadinho", matriz_caminhos_com_puxadinho)

    matriz_distancias = gerar_matriz_distancias(matriz_caminhos_com_puxadinho, cidades)
    #imprimir_matriz("matriz_distancias", matriz_distancias)

    matriz_custos = gerar_matriz_custos(matriz_distancias)
    #imprimir_matriz("matriz_custos", matriz_custos)

    matriz_distancias, matriz_custos, matriz_caminhos = ordenar_por_custo(matriz_distancias, matriz_custos, matriz_caminhos)
    #imprimir_matriz("matriz_distancias Ordenadas", matriz_distancias)
    #imprimir_matriz("matriz_custos Ordenados", matriz_custos)
    #imprimir_matriz("matriz_caminhos Ordenados", matriz_caminhos)

    matriz_distancias = matriz_distancias[:10]
    matriz_caminhos = matriz_caminhos[:10]
    #imprimir_matriz("matriz_distancias Top 10", matriz_distancias)
    #imprimir_matriz("matriz_caminhos Top 10", matriz_caminhos)

    #print("--------------- Roleta")
    roletas = [10,9,9,8,8,8,7,7,7,7,6,6,6,6,6,5,5,5,5,5,5,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1]

    for i in range(5):
        pai1, pai2 = selecionar_pais_roleta(roletas)
        #print("Pai 1:", pai1)
        #print("Pai 2:", pai2)

        filho1, filho2 = recombinacao(matriz_caminhos[pai1], matriz_caminhos[pai2])
        #print("Filho 1 recombinacao:", filho1)
        #print("Filho 2 recombinacao:", filho2)

        filho1 = mutacao(filho1)
        filho2 = mutacao(filho2)
        #print("Filho 1 mutacao:", filho1)
        #print("Filho 2 mutacao:", filho2)

        matriz_caminhos.append(filho1)
        matriz_caminhos.append(filho2)

    #imprimir_matriz("matriz_caminhos com filhos", matriz_caminhos)

    return matriz_caminhos

# inicio do processo
numero_cidades = 20
populacao_inicial = gerar_matriz_caminhos(numero_cidades)
matriz = populacao_inicial.copy()

# loop que roda o algoritmo as 10 mil vezes
for i in range(10000):
    matriz = funcao_principal(matriz)

populacao_final = matriz.copy()

imprimir_matriz("Populacao inicial: ", populacao_inicial)
print()
imprimir_matriz("Populacao final: ", populacao_final)
print()
print("Número de cidades: ", numero_cidades)



cidades = carregar_cidades('cidades.mat')

# cria listas com coordenadas do melhor caminho
x_coords = []
for cidade in populacao_final[0]:
    x = cidades[0][cidade - 1]
    x_coords.append(x)
y_coords = []
for cidade in populacao_final[0]:
    y = cidades[1][cidade - 1]
    y_coords.append(y)

# adiciona a cidade inicial no final para fechar o ciclo
x_coords.append(x_coords[0])
y_coords.append(y_coords[0])

# plot
plt.figure(figsize=(10, 6))
plt.scatter(cidades[0], cidades[1], color='blue', label='Cidades')
plt.plot(x_coords, y_coords, color='red', linestyle='-', linewidth=2, label='Melhor Caminho')

# marcar as cidades com número
for i, (x, y) in enumerate(zip(cidades[0], cidades[1]), 1):
    plt.text(x, y, str(i), fontsize=9, ha='right', va='bottom')

plt.title("Melhor Caminho Encontrado pelo Algoritmo Genético")
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.legend()
plt.grid(True)
plt.show()