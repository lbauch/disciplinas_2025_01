import numpy as np

from GeradorMatriz import GeradorMatriz

x, y = np.loadtxt('cidades.mat')

gerador = GeradorMatriz(20, 20)
gerador.gerar_matriz()
gerador.calcular_distancias(x, y)
gerador.ordenar_matriz()
indice_pai1, indice_pai2 = gerador.selecionar_pais()



