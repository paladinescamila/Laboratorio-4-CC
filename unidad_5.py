# UNIDAD 5: DIFERENCIACIÓN E INTEGRACIÓN

import time
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

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


# Segunda derivada (CREO QUE NO ERA NECESARIO)
def segunda_derivada(f, h):
    """
    Entrada: una función f(x) y un entero h.
    Salida: segunda derivada f''(x).
    """

    derivada = (f.subs(x,x+h) -2*f + f.subs(x,x-h)) / (h**2)
    return derivada


# Integral por Regla del Rectángulo
def punto_medio(f, a, b, n):
    """
    Entrada: función f(x), dos reales a y b, y un entero n.
    Salida: integral definida de f(x) con límites a y b con n paneles.
    """

    xi = [i for i in np.linspace(a, b, n)]
    f = sym.lambdify(x, f)

    integral = 0
    for i in range(n):
        integral += (xi[i] - xi[i-1]) * f((xi[i-1] + xi[i]) / 2)

    return integral


# Integral por Regla del Trapezoide
def trapezoide(f, a, b, n):
    """
    Entrada: función f(x), dos reales a y b, y un entero n.
    Salida: integral definida de f(x) con límites a y b con n paneles.
    """

    xi = [i for i in np.linspace(a, b, n)]
    f = sym.lambdify(x, f)

    integral = 0
    for i in range(n):
        integral += (xi[i] - xi[i-1]) * (f(xi[i-1]) + f(xi[i]))

    return integral / 2


# Integral por Regla del Simpson
def simpson(f, a, b, n):
    """
    Entrada: función f(x), dos reales a y b, y un entero n.
    Salida: integral definida de f(x) con límites a y b con n paneles.
    """

    xi = [i for i in np.linspace(a, b, n)]
    f = sym.lambdify(x, f)

    integral = 0
    for i in range(n):
        integral += (xi[i] - xi[i-1]) * (f(xi[i-1]) + 4*f((xi[i-1]+xi[i])/2) + f(xi[i]))

    return integral / 6


# Pintar ejemplo de derivada con cada método
def ejemplo_derivada(funcion, hs, min_x, max_x, mostrar):
    # FALTA LA SEGUNDA DERIVADA

    colores = ["purple", "red", "green", "orange", "gray"]
    metodos = ["Hacia Adelante", "Hacia Atrás", "Centrada"]

    x_funcion = np.linspace(min_x, max_x, 1000)
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
            
            print("----------------------------------------------")
            print(" DIFERENCIAS FINITAS {}".format(metodos[i].upper()))
            print("----------------------------------------------")
            print(" h\tTiempo\tError (Prom)\tError (Desv)\tf'(x)")
            print("----------------------------------------------")


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

            print("----------------------------------------------\n")
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()
    
    print()
    plt.title("Métodos de Diferenciación con h = "+str(hs[0]))
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


# Pintar ejemplo de integral con cada método
def ejemplo_integral(funcion, min_x, max_x, mostrar):

    analitica = float(sym.integrate(funcion, (x, min_x, max_x)))

    inicio = time.time()
    integral_punto_medio = punto_medio(funcion, min_x, max_x, 1000)
    tiempo_m = time.time() - inicio
    error_m = np.abs(analitica - integral_punto_medio)

    inicio = time.time()
    integral_trapezoide = trapezoide(funcion, min_x, max_x, 1000)
    tiempo_t = time.time() - inicio
    error_t = np.abs(analitica - integral_trapezoide)

    inicio = time.time()
    integral_simpson = simpson(funcion, min_x, max_x, 1000)
    tiempo_s = time.time() - inicio
    error_s = np.abs(analitica - integral_simpson)

    if (mostrar):

        print("f(x) = {}".format(funcion))
        print("∫f(x)dx = {}".format(analitica))
        print("---------------------------------------------------------------")
        print("                       INTEGRAL DEFINIDA                       ")
        print("---------------------------------------------------------------")
        print(" Método\t\tTiempo\t\tError\t\t∫f(x)dx")
        print("---------------------------------------------------------------")
        print(" Punto medio\t{:.5f}\t\t{:.5f}\t\t{:.10f}".format(tiempo_m, error_m, integral_punto_medio))
        print(" Trapezoide\t{:.5f}\t\t{:.5f}\t\t{:.10f}".format(tiempo_t, error_t, integral_trapezoide))
        print(" Simpson\t{:.5f}\t\t{:.5f}\t\t{:.10f}".format(tiempo_s, error_s, integral_simpson))
        print("---------------------------------------------------------------")

        f = sym.lambdify(x, funcion)
        t = np.linspace(min_x, max_x, 1000)
        plt.title("Integral definida")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.plot(t, f(t), color="black")
        plt.axvline(x=min_x, color='b')
        plt.axvline(x=max_x, color='b')
        plt.fill_between(t, f(t), where=[(i > min_x) and (i < max_x) for i in t], color="lightblue")
        plt.show()

        print()


# EJEMPLOS DE PRUEBA (También se encuentran en el informe)
def main():

    print("DIFERENCIACIÓN")

    print("EJEMPLO 1")
    funcion = 5*x**4 + 10*x**3 + 15*x**2 + x + 7
    hs = [1, 0.3, 0.05, 0.007]
    ejemplo_derivada(funcion, hs, -1, 1, True)

    print("EJEMPLO 2")
    funcion = 3**(x + 2)
    hs = [2, 0.4, 0.06, 0.008]
    ejemplo_derivada(funcion, hs, -0.5, 0.5, True)

    print("EJEMPLO 3")
    funcion = sym.sin(2*x**3)
    hs = [1, 0.2, 0.03, 0.004]
    ejemplo_derivada(funcion, hs, -1, 1, True)

    print("INTEGRACIÓN")

    print("EJEMPLO 1")
    funcion = 3*sym.cos(x)
    ejemplo_integral(funcion, -5, 5, True)

    print("EJEMPLO 2")
    funcion = x**2 + 7*x**3 + 2*x + 1
    ejemplo_integral(funcion, -10, 20, True)

    print("EJEMPLO 3")
    funcion = 2**(-x+5)
    ejemplo_integral(funcion, -20, -10, True)


main()