# ANÁLISIS DE COMPLEJIDAD Y ERRROR DE LAS DERIVADAS

from unidad_5 import *

def analisis_derivada(funcion, a, b):

    print("f(x) = {}".format(funcion))

    metodos = ['Adelante', 'Atrás', 'Centrada']
    colores = ["blue", "red", "green"]

    hs = [round(0.1*(i+1), 1) for i in range(10)]
    promedio = [[] for _ in range(3)]
    desviacion = [[] for _ in range(3)]
    tiempo = [[] for _ in range(3)]

    for i in hs:
        _, _, t, p, d = ejemplo_derivada(funcion, [i], a, b, False)
        for j in range(3):
            promedio[j].append(p[j][0])
            desviacion[j].append(d[j][0])
            tiempo[j].append(t[j][0])

    imprimir("Error (Promedio)", hs, promedio, ["h"] + metodos)
    imprimir("Error (Desviación)", hs, desviacion, ["h"] + metodos)
    graficar(hs, promedio, colores, "Error", "h", "Error", metodos)

    imprimir("Tiempo", hs, tiempo, ["h"] + metodos)
    graficar(hs, tiempo, colores, "Tiempo", "n", "Tiempo", metodos)


# Análisis de los ejemplos planteados
def main_derivada():

    print("EJEMPLO 1")
    funcion = 2*x**4 + 3*x**2 + x
    analisis_derivada(funcion, 0, 3)

    print("EJEMPLO 2")
    funcion = 3**(x + 2) + x
    analisis_derivada(funcion, 7, 10)

    print("EJEMPLO 3")
    funcion = sym.sin(2*x**3)
    analisis_derivada(funcion, 1, 2)


main_derivada()