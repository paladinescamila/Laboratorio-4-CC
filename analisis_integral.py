# ANÁLISIS DE COMPLEJIDAD Y ERROR DE LAS INTEGRALES

from unidad_5 import *

def analisis_integral(funcion, a, b):

    print("f(x) = {}".format(funcion))

    metodos = ['Punto Medio', 'Trapezoide', 'Simpson']
    colores = ["blue", "red", "purple"]

    ns = [(i+1)*1000 for i in range(10)]
    error = [[] for _ in range(3)]
    tiempo = [[] for _ in range(3)]

    for i in range(10):
        _, _, t, e = ejemplo_integral(funcion, (i+1)*1000, a, b, False)
        for j in range(3):
            error[j].append(e[j])
            tiempo[j].append(t[j])

    imprimir("Errores", ns, error, ["n"] + metodos)
    graficar(ns, error, colores, "Error", "n", "Error", metodos)
    for i in range(3):
        graficar(ns, [error[i]], [colores[i]], "Error ("+metodos[i]+")", "n", "Error", [metodos[i]])

    imprimir("Tiempos", ns, tiempo, ["n"] + metodos)
    graficar(ns, tiempo, colores, "Tiempo", "n", "Tiempo", metodos)


# Análisis de los ejemplos planteados
def main_integral():

    print("EJEMPLO 1")
    funcion = 3*x*sym.cos(x)
    analisis_integral(funcion, -4.5, 3)

    print("EJEMPLO 2")
    funcion = x**2 + 7*x**3 + 2*x + 1
    analisis_integral(funcion, -10, 20)

    print("EJEMPLO 3")
    funcion = 2**(-x + 5)
    analisis_integral(funcion, -18.5, -10)


# main_integral()