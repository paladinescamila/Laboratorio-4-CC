# UNIDAD 5: DIFERENCIACIÓN E INTEGRACIÓN

import time
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

x_sym = sym.Symbol("x")
x = sym.Symbol("x")


# Método de Diferencias Finitas Hacia Adelante
def diferencia_hacia_adelante(f, h):
    """
    Entrada: una función f(x) y un entero h.
    Salida: primera derivada f'(x).
    """

    derivada = (f.subs(x,x+h) - f) / h
    return derivada


# Método de Diferencias Finitas Hacia Atrás
def diferencia_hacia_atras(f, h):
    """
    Entrada: una función f(x) y un entero h.
    Salida: primera derivada f'(x).
    """

    derivada = (f - f.subs(x,x-h)) / h
    return derivada


# Método de Diferencia Centrada
def diferencia_centrada(f, h):
    """
    Entrada: una función f(x) y un entero h.
    Salida: primera derivada f'(x).
    """

    derivada = (f.subs(x,x+h) - f.subs(x,x-h)) / (2*h)
    return derivada


# Segunda derivada
def segunda_derivada(f, h):
    """
    Entrada: una función f(x) y un entero h.
    Salida: segunda derivada f''(x).
    """

    derivada = (f.subs(x,x+h) -2*f + f.subs(x,x-h)) / (h**2)
    return derivada


# Pintar ejemplo de derivada con cada método
def ejemplo_derivada(funcion, hs, min_x, min_y, mostrar):
    # FALTA LA SEGUNDA DERIVADA

    colores = ["purple", "red", "green", "orange", "gray"]
    metodos = ["Hacia Adelante", "Hacia Atrás", "Centrada"]

    x_funcion = np.linspace(min_x, min_y, 1000)
    f_funcion = sym.lambdify(x, funcion)
    y_funcion = [f_funcion(i) for i in x_funcion]
    
    analitica = sym.diff(funcion, x)
    f_analitica = sym.lambdify(x, analitica)
    y_analitica = [f_analitica(i) for i in x_funcion]

    if (mostrar):
        print("f(x) = {}".format(funcion))
        print("f'(x) = {}".format(analitica))

    y_metodos = []

    for i in range(3):

        if (mostrar):

            # plt.figure(figsize=(10, 5))
            plt.title("Diferencias Finitas " + metodos[i])
            plt.plot(x_funcion, y_funcion, color="black", label="f(x)")
            plt.plot(x_funcion, y_analitica, color="blue", label="f'(x)")
            
            print("---------------------------------------------")
            print(" DIFERENCIAS FINITAS {}".format(metodos[i].upper()))
            print("---------------------------------------------")
            print(" h\tTiempo\tError (Prom)\tError (Desv)\tf'(x)")
            print("---------------------------------------------")


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

            if (j == 0): y_metodos += [y_derivada]

            errores = [np.abs(y_derivada[k] - y_analitica[k]) for k in range(1000)]
            promedio = np.mean(errores)
            desviacion = np.std(errores)

            if (mostrar):
                print(" {}\t{:.4f}\t{:.10f}\t{:.10f}\t{}".format(hs[j], tiempo, promedio, desviacion, sym.expand(derivada)))
                plt.plot(x_funcion, y_derivada, color=colores[j], label="h = "+str(hs[j]))

        if (mostrar):

            print("---------------------------------------------\n")
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()
    
    print()
    plt.title("Métodos de Diferenciación")
    plt.plot(x_funcion, y_funcion, color="black", label="f(x)")
    plt.plot(x_funcion, y_analitica, color="blue", label="f'(x)")

    for i in range(3):
        plt.plot(x_funcion, y_metodos[i], color=colores[i], label=str(metodos[i]))
    
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()

    print()


# EJEMPLOS DE PRUEBA (También se encuentran en el informe)
def main():

    print("DIFERENCIACIÓN")

    print("EJEMPLO 1")
    funcion = 5*x**4 + 10*x**3 + 15*x**2 + x + 7
    hs = [1, 0.2, 0.03]
    ejemplo_derivada(funcion, hs, -1, 1, True)

    print("EJEMPLO 2")
    funcion = 3**(x + 2)
    hs = [1, 0.1, 0.01]
    ejemplo_derivada(funcion, hs, -0.5, 0.5, True)

    print("EJEMPLO 3")
    funcion = sym.sin(2*x**3)
    hs = [1, 0.1, 0.01]
    ejemplo_derivada(funcion, hs, -1, 1, True)


main()