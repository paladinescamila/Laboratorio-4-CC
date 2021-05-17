# UNIDAD 5: DIFERENCIACIÓN E INTEGRACIÓN

import time
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

x = sym.Symbol("x")


# Método de Diferencias Finitas Hacia Adelante
def diferencia_hacia_adelante(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: primera derivada f'(x).
    """

    derivada = (f.subs(x,x+h) - f) / h
    return derivada


# Método de Diferencias Finitas Hacia Atrás
def diferencia_hacia_atras(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: primera derivada f'(x).
    """

    derivada = (f - f.subs(x,x-h)) / h
    return derivada


# Método de Diferencias Finitas Centrada
def diferencia_centrada(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: primera derivada f'(x).
    """

    derivada = (f.subs(x,x+h) - f.subs(x,x-h)) / (2*h)
    return derivada


# Segunda derivada
def segunda_derivada(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: segunda derivada f''(x).
    """

    derivada = (f.subs(x,x+h) -2*f + f.subs(x,x-h)) / (h**2)
    return derivada


# Integral por Regla del Punto Medio o Rectángulo
def punto_medio(f, a, b, n):
    """
    Entrada: función f(x), dos reales a & b, y un entero n.
    Salida: integral definida de f(x) con límites a y b, con n paneles.
    """

    xi = np.linspace(a, b, n)
    f = sym.lambdify(x, f)

    integral = 0
    for i in range(n):
        integral += (xi[i] - xi[i-1]) * f((xi[i-1] + xi[i]) / 2)

    return integral


# Integral por Regla del Trapezoide
def trapezoide(f, a, b, n):
    """
    Entrada: función f(x), dos reales a & b, y un entero n.
    Salida: integral definida de f(x) con límites a y b con n paneles.
    """

    xi = np.linspace(a, b, n)
    f = sym.lambdify(x, f)

    integral = 0
    for i in range(n):
        integral += (xi[i] - xi[i-1]) * (f(xi[i-1]) + f(xi[i]))

    return integral / 2


# Integral por Regla del Simpson
def simpson(f, a, b, n):
    """
    Entrada: función f(x), dos reales a & b, y un entero n.
    Salida: integral definida de f(x) con límites a y b con n paneles.
    """

    xi = np.linspace(a, b, n)
    f = sym.lambdify(x, f)

    integral = 0
    for i in range(n):
        integral += (xi[i] - xi[i-1]) * (f(xi[i-1]) + 4*f((xi[i-1]+xi[i])/2) + f(xi[i]))

    return integral / 6


# Pintar ejemplo de derivada con cada método
def ejemplo_derivada(funcion, hs, a, b, mostrar):
    """
    Entrada: una función funcion(x), una lista de reales hs, dos reales a & b
            y un booleano mostrar.
    Salida: la derivada analítica de la función, las derivadas calculadas por los
            métodos de diferenciación finita para cada h, los tiempos de ejecución, 
            los errores promedio y las desviaciones de los errores.
    """

    x_funcion = np.linspace(a, b, 1000)
    f_funcion = sym.lambdify(x, funcion)
    y_funcion = [f_funcion(i) for i in x_funcion]
    
    analitica = sym.diff(funcion, x)
    f_analitica = sym.lambdify(x, analitica)
    y_analitica = [f_analitica(i) for i in x_funcion]

    nh = len(hs)
    t_metodos, p_metodos, d_metodos, f_metodos, y_metodos = [], [], [], [], []
    derivadas = [[None for _ in range(nh)] for _ in range(3)]
    tiempos = [[None for _ in range(nh)] for _ in range(3)]
    promedios = [[None for _ in range(nh)] for _ in range(3)]
    desviaciones = [[None for _ in range(nh)] for _ in range(3)]

    if (mostrar):
        
        print("f(x) = {}".format(funcion))
        print("f'(x) = {}".format(analitica))
        print("a = {}\nb = {}\nhs = {}".format(a, b, hs))

        colores = ["purple", "red", "green", "orange", "gray"]
        metodos = ["Hacia Adelante", "Hacia Atrás", "Centrada"]
        if (nh > 5): colores = ["purple" for _ in range(nh)]

    for i in range(3):

        if (mostrar):

            plt.title("Diferencias Finitas " + metodos[i])
            plt.plot(x_funcion, y_funcion, color="black", label="f(x)")
            plt.plot(x_funcion, y_analitica, color="blue", label="f'(x)")
            
            print("----------------------------------------------")
            print(" DIFERENCIAS FINITAS {}".format(metodos[i].upper()))
            print("----------------------------------------------")
            print(" h\tTiempo\tError (Prom)\tError (Desv)\tf'(x)")
            print("----------------------------------------------")

        for j in range(nh):

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

            if (j == 0):
                t_metodos += [tiempo]
                p_metodos += [promedio]
                d_metodos += [desviacion]
                f_metodos += [derivada]
                y_metodos += [y_derivada]
            
            derivadas[i][j], tiempos[i][j] = derivada, tiempo
            promedios[i][j], desviaciones[i][j] = promedio, desviacion

            if (mostrar):
                print(" {}\t{:.4f}\t{:.10f}\t{:.10f}\t{}".format(hs[j], tiempo, promedio, desviacion, sym.expand(derivada)))
                # print("\t\t{} & {:.10f} & {:.10f} & {:.10f} \\\\".format(hs[j], tiempo, promedio, desviacion))
                # print("\t\t{} & ${}$ \\\\".format(hs[j], sym.expand(derivada)))
                plt.plot(x_funcion, y_derivada, color=colores[j], label="h = "+str(hs[j]))

        if (mostrar):

            print("----------------------------------------------\n")
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()
    
    if (mostrar):

        print()
        plt.title("Métodos de Diferenciación con h = "+str(hs[0]))
        plt.plot(x_funcion, y_funcion, color="black", label="f(x)")
        plt.plot(x_funcion, y_analitica, color="blue", label="f'(x)")

        print("-----------------------------------------------------")
        print("                DIFERENCIAS FINITAS                 ")
        print("-----------------------------------------------------")
        print(" Método\t\tTiempo\tError (Prom)\tError (Desv)\tf'(x)")
        print("-----------------------------------------------------")
        for i in range(3):
            print(" {}\t{:.5f}\t{:.10f}\t{:.10f}\t{}".format(metodos[i], t_metodos[i], p_metodos[i], d_metodos[i], f_metodos[i]))
            plt.plot(x_funcion, y_metodos[i], color=colores[i], label=str(metodos[i]))
        print("-----------------------------------------------------")
        
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()
        print()

    return analitica, derivadas, tiempos, promedios, desviaciones


# Pintar ejemplo de integral con cada método
def ejemplo_integral(funcion, ns, a, b, mostrar):
    """
    Entrada: una función funcion(x), una lista de enteros ns, dos reales a & b
            y un booleano mostrar.
    Salida: la integral definida analítica de la función, las integrales definidas 
            calculadas por las reglas de cuadratura compuesta para cada n, los 
            tiempos de ejecución, los errores promedio y las desviaciones de los errores.
    """
    
    analitica = float(sym.integrate(funcion, (x, a, b)))

    nn = len(ns)
    t_metodos, e_metodos, f_metodos = [], [], []
    integrales = [[None for _ in range(nn)] for _ in range(3)]
    tiempos = [[None for _ in range(nn)] for _ in range(3)]
    errores = [[None for _ in range(nn)] for _ in range(3)]

    if (mostrar):

        print("f(x) = {}".format(funcion))
        print("a = {}\nb = {}\nn = {}".format(a, b, ns))
        print("∫f(x)dx = {}".format(analitica))

        metodos = ["Punto Medio", "Trapeziode", "Simpson"]
        if (nn > 5): colores = ["purple" for _ in range(nn)]

    for i in range(3):

        if (mostrar):
            
            print("---------------------------------------------------")
            print("               REGLA DEL {}              ".format(metodos[i].upper()))
            print("---------------------------------------------------")
            print(" n\tTiempo\tError\t\t∫f(x)dx")
            print("---------------------------------------------------")

        for j in range(nn):

            if (i == 0):
                inicio = time.time()
                integral = punto_medio(funcion, a, b, ns[j])
                tiempo = time.time() - inicio

            elif (i == 1):
                inicio = time.time()
                integral = trapezoide(funcion, a, b, ns[j])
                tiempo = time.time() - inicio

            else:
                inicio = time.time()
                integral = simpson(funcion, a, b, ns[j])
                tiempo = time.time() - inicio

            error = np.abs(analitica - integral)

            if (j == 0):
                t_metodos += [tiempo]
                e_metodos += [error]
                f_metodos += [integral]
            
            integrales[i][j], tiempos[i][j], errores[i][j] = integral, tiempo, error

            if (mostrar):
                print(" {}\t{:.5f}\t{:.2f}\t{}".format(ns[j], tiempo, error, integral))

        if (mostrar):
            print("---------------------------------------------------\n")

    if (mostrar):
    
        print()

        print("-----------------------------------------------------")
        print("                  INTEGRAL DEFINIDA                  ")
        print("-----------------------------------------------------")
        print(" Método\t\tTiempo\tError\t∫f(x)dx")
        print("-----------------------------------------------------")
        for i in range(3):
            print(" {}\t{:.5f}\t{:.2f}\t{}".format(metodos[i], t_metodos[i], e_metodos[i], f_metodos[i]))
        print("-----------------------------------------------------")

        f = sym.lambdify(x, funcion)
        t = np.linspace(a, b, 1000)
        plt.title("Integral definida")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.plot(t, f(t), color="black")
        plt.fill_between(t, f(t), where=[(i > a) and (i < b) for i in t], color="lightblue")
        plt.show()
        print()

    return analitica, integrales, tiempos, errores


# EJEMPLOS DE PRUEBA (También se encuentran en el informe)
def main():

    print("DIFERENCIACIÓN")

    print("EJEMPLO 1")
    funcion = 5*x**4 + 10*x**3 + 15*x**2 + x + 7
    hs = [1, 0.3, 0.05, 0.007]
    ejemplo_derivada(funcion, hs, -1, 1, True)

    print("EJEMPLO 2")
    funcion = 3**(x + 2)
    hs = [1, 0.4, 0.06, 0.008]
    ejemplo_derivada(funcion, hs, 2, 5, True)

    print("EJEMPLO 3")
    funcion = sym.sin(2*x**3)
    hs = [1, 0.2, 0.03, 0.004]
    ejemplo_derivada(funcion, hs, -0.5, 0.5, True)

    print("INTEGRACIÓN")

    print("EJEMPLO 1")
    funcion = 3*sym.cos(x)
    ns = [1000, 3000, 5000, 7000]
    ejemplo_integral(funcion, ns, -4.5, 3, True)

    print("EJEMPLO 2")
    funcion = x**2 + 7*x**3 + 2*x + 1
    ns = [2000, 4000, 6000, 8000]
    ejemplo_integral(funcion, ns, -10, 20, True)

    print("EJEMPLO 3")
    funcion = 2**(-x+5)
    ns = [1000, 2000, 3000, 4000]
    ejemplo_integral(funcion, ns, -18.5, -10, True)


# main()