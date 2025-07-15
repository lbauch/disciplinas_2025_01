import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def exibir(matriz, posAPAy, posAPAx):    
    # plota a matriz com a escala de cores respectiva a cada número
    # azul = 0 = limpo; verde = 1 = parede; amarelo = 2 = sujo
    cmap = mcolors.ListedColormap(['blue', 'green', 'yellow'])
    plt.imshow(matriz, cmap=cmap)

    # plota o ponto vermelho
    plt.plot(posAPAy, posAPAx, marker='o', color='r', ls='')

    plt.show(block=False)

    plt.pause(1)    
    plt.clf()
