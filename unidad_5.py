# UNIDAD 5: DIFERENCIACIÓN E INTEGRACIÓN

import time
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

x_sym = sym.Symbol("x")
x = sym.Symbol("x")


# Método de Diferencias Finitas Hacia Adelante
def diferencia_hacia_adelante(funcion, h):
    f = sym.lambdify(x_sym, funcion)
    derivada = (f(x+h) - f(x)) / h
    return derivada


# Método de Diferencias Finitas Hacia Atrás
def diferencia_hacia_atras(funcion, h):
    f = sym.lambdify(x_sym, funcion)
    derivada = (f(x) - f(x-h)) / h
    return derivada


# Método de Diferencia Centrada
def diferencia_centrada(funcion, h):
    f = sym.lambdify(x_sym, funcion)
    derivada = (f(x+h) - f(x-h)) / (2*h)
    return derivada


# Segunda derivada
def segunda_derivada(funcion, h):
    f = sym.lambdify(x_sym, funcion)
    derivada = (f(x+h) -2*f(x) + f(x-h)) / (h**2)
    return derivada


# Pintar ejemplo de derivada con cada método
def ejemplo_derivada(funcion, analitica, hs, min_x, min_y, mostrar):
    # FALTA LA SEGUNDA DERIVADA

    x_funcion = np.linspace(min_x, min_y, 1000)
    colores = ["purple", "red", "green", "orange", "gray"]
    metodos = ["Hacia Adelante", "Hacia Atrás", "Centrada"]
    
    f_funcion = sym.lambdify(x, funcion)
    f_analitica = sym.lambdify(x, analitica)

    y_funcion = [f_funcion(i) for i in x_funcion]
    y_analitica = [f_analitica(i) for i in x_funcion]

    for i in range(3):

        if (mostrar):

            # plt.figure(figsize=(10, 5))
            plt.title("Diferencias Finitas " + metodos[i])
            plt.plot(x_funcion, y_funcion, color="black", label="f(x)")
            plt.plot(x_funcion, y_analitica, color="blue", label="f'(x)")

            print("------------------------------------------------------------------------")
            print("                  DIFERENCIAS FINITAS {}                  ".format(metodos[i].upper()))
            print("------------------------------------------------------------------------")
            print("h\tTiempo\t\tError (Prom)\tError (Desv)\tf'(x)")
            print("------------------------------------------------------------------------")

        for j in range(len(hs)):

            if (i == 0):
                inicio = time.time()
                derivada = diferencia_hacia_adelante(funcion, hs[j])
                tiempo = time.time() - inicio

            elif (i == 1):
                inicio = time.time()
                derivada = diferencia_hacia_atras(funcion, hs[j])
                tiempo = time.time() - inicio

            else:
                inicio = time.time()
                derivada = diferencia_centrada(funcion, hs[j])
                tiempo = time.time() - inicio

            f_derivada = sym.lambdify(x, derivada)
            y_derivada = [f_derivada(k) for k in x_funcion]

            errores = [np.abs(y_derivada[k] - y_analitica[k]) for k in range(1000)]
            promedio = np.mean(errores)
            desviacion = np.std(errores)

            if (mostrar):
                print("{}\t{:5f}\t{:.10f}\t{:.10f}\t{}".format(hs[j], tiempo, promedio, desviacion, sym.expand(derivada)))
                plt.plot(x_funcion, y_derivada, color=colores[j], label="h = "+str(hs[j]))

        if (mostrar):

            print("------------------------------------------------------------------------\n")
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()


def main():

    print("DIFERENCIACIÓN")

    print("EJEMPLO 1")
    funcion = x**2
    analitica = 2*x
    hs = [1, 0.1, 0.01]
    ejemplo_derivada(funcion, analitica, hs, -1, 1, True)


main()