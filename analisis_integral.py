# ANÁLISIS DE COMPLEJIDAD Y ERROR DE LAS INTEGRALES

from unidad_5 import *

def graficar(x, y, color, title, xlabel, ylabel):
    for i in range(len(y)): plt.plot(x, y[i], color=color[i])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()


def grafica_barras(x, y, title, xlabel, ylabel):
    ax = plt.figure().add_axes([0,0,1,1])
    plt.title(title)
    ax.bar(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def imprimir(titulo, ns, valores):
    print("------------------------------------------------------")
    print("                       {}                            ".format(titulo))
    print("------------------------------------------------------")
    print(" n\tPunto Medio\tTrapeziode\tSimpson")
    print("------------------------------------------------------")

    N = len(ns)
    for i in range(N):
        e1 = valores[0][i]
        e2 = valores[1][i]
        e3 = valores[2][i]
        print(" {}\t{:.5f}\t{:.5f}\t{:.5f}".format(ns[i], e1, e2, e3))
            
    print("------------------------------------------------------")


def analisis_integral(funcion, a, b):

    MAX, PUNTOS = 10000, 10
    ITER = int(MAX/PUNTOS)
    ns = [i for i in range(ITER, MAX+1, ITER)]
    errores_metodos = [[] for _ in range(3)]
    tiempos_metodos = [[] for _ in range(3)]

    for i in range(PUNTOS):
        analitica, integrales, tiempos, errores = ejemplo_integral(funcion, [(i+1)*ITER], a, b, False)
        errores_metodos[0].append(errores[0])
        errores_metodos[1].append(errores[1])
        errores_metodos[2].append(errores[2])
        tiempos_metodos[0].append(tiempos[0])
        tiempos_metodos[1].append(tiempos[1])
        tiempos_metodos[2].append(tiempos[2])
    
    errores_metodos = [[errores_metodos[i][j][0] for j in range(PUNTOS)] for i in range(3)]
    tiempos_metodos = [[tiempos_metodos[i][j][0] for j in range(PUNTOS)] for i in range(3)]

    imprimir("Errores", ns, errores_metodos)
    graficar(ns, [errores_metodos[0]], ["blue"], "Error (Punto Medio)", "n", "Error")
    graficar(ns, [errores_metodos[1]], ["blue"], "Error (Trapeziode)", "n", "Error")
    graficar(ns, [errores_metodos[2]], ["blue"], "Error (Simpson)", "n", "Error")

    metodos = ['Punto Medio', 'Trapeziode', 'Simpson']
    error = [errores_metodos[i][0] for i in range(3)]
    grafica_barras(metodos, error, "Error con n = "+str(ITER), "Método", "Error")

    imprimir("Tiempos", ns, tiempos_metodos)
    graficar(ns, tiempos_metodos, ["blue", "red", "purple"], "Tiempo", "n", "Tiempo")


print("EJEMPLDO 1")
funcion = 3*sym.cos(x)
ns = [1000, 3000, 5000, 7000]
analisis_integral(funcion, -4.5, 3)

print("EJEMPLDO 2")
funcion = x**2 + 7*x**3 + 2*x + 1
ns = [2000, 4000, 6000, 8000]
analisis_integral(funcion, -10, 20)

print("EJEMPLDO 3")
funcion = 2**(-x+5)
ns = [1000, 2000, 3000, 4000]
analisis_integral(funcion, -18.5, -10)