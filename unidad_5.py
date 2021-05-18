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
    Salida: primera derivada aproximada f'(x).
    """

    derivada = (f.subs(x,x+h) - f) / h
    return derivada


# Método de Diferencias Finitas Hacia Atrás
def diferencia_hacia_atras(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: primera derivada aproximada f'(x).
    """

    derivada = (f - f.subs(x,x-h)) / h
    return derivada


# Método de Diferencias Finitas Centrada
def diferencia_centrada(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: primera derivada aproximada f'(x).
    """

    derivada = (f.subs(x,x+h) - f.subs(x,x-h)) / (2*h)
    return derivada


# Segunda Derivada
def segunda_derivada(f, h):
    """
    Entrada: una función f(x) y un real h.
    Salida: segunda derivada aproximada f''(x).
    """

    derivada = (f.subs(x,x+h) -2*f + f.subs(x,x-h)) / (h**2)
    return derivada


# Integral por Regla del Punto Medio o Rectángulo
def punto_medio(f, a, b, n):
    """
    Entrada: función f(x), dos reales a & b, y un entero n.
    Salida: integral definida aproximada de f(x) con límites a y b, con n paneles.
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
    Salida: integral definida aproximada de f(x) con límites a y b con n paneles.
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
    Salida: integral definida aproximada de f(x) con límites a y b con n paneles.
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
            y un booleano "mostrar".
    Salida: la derivada analítica, las derivadas calculadas por los métodos para cada h, 
            los tiempos de ejecución, los errores promedio y las desviaciones de los errores.
    """

    x_funcion = np.linspace(a, b, 1000)
    
    analitica = sym.diff(funcion, x)
    f_analitica = sym.lambdify(x, analitica)
    y_analitica = [f_analitica(i) for i in x_funcion]

    nh = len(hs)
    derivadas = [[None for _ in range(nh)] for _ in range(3)]
    tiempos = [[None for _ in range(nh)] for _ in range(3)]
    promedios = [[None for _ in range(nh)] for _ in range(3)]
    desviaciones = [[None for _ in range(nh)] for _ in range(3)]

    if (mostrar):
        
        print("f(x) = {}".format(funcion))
        print("f'(x) = {}".format(analitica))
        print("a = {}\nb = {}\nhs = {}".format(a, b, hs))

        t_metodos, p_metodos, d_metodos, f_metodos, y_metodos = [], [], [], [], []
        colores = ["purple", "red", "green", "orange", "gray"]
        metodos = ["Hacia Adelante", "Hacia Atrás", "Centrada"]
        if (nh > 5): colores = ["purple" for _ in range(nh)]

    for i in range(3):

        if (mostrar):

            plt.title("Diferencias Finitas " + metodos[i])
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

            if (j == 0 and mostrar):
                t_metodos.append(tiempo)
                p_metodos.append(promedio)
                d_metodos.append(desviacion)
                f_metodos.append(derivada)
                y_metodos.append(y_derivada)
            
            derivadas[i][j], tiempos[i][j] = derivada, tiempo
            promedios[i][j], desviaciones[i][j] = promedio, desviacion

            if (mostrar):
                print(" {}\t{:.4f}\t{:.10f}\t{:.10f}\t{}".format(hs[j], tiempo, promedio, desviacion, sym.expand(derivada)))
                # print("\t\t{} & {:.10f} & {:.10f} & {:.10f} \\\\".format(hs[j], tiempo, promedio, desviacion))
                # print("\t\t{} & ${}$ \\\\".format(hs[j], sym.expand(derivada)))
                plt.plot(x_funcion, y_derivada, color=colores[j], label="h = "+str(hs[j]), linewidth=2)

        if (mostrar):

            print("----------------------------------------------\n")
            plt.plot(x_funcion, y_analitica, color="black", label="Analítica")
            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()
    
    if (mostrar):

        print()
        plt.title("Métodos de Diferenciación con h = "+str(hs[0]))
        print("-----------------------------------------------------")
        print("                DIFERENCIAS FINITAS                 ")
        print("-----------------------------------------------------")
        print(" Método\t\tTiempo\tError (Prom)\tError (Desv)\tf'(x)")
        print("-----------------------------------------------------")
        for i in range(3):
            print(" {}\t{:.5f}\t{:.10f}\t{:.10f}\t{}".format(metodos[i], t_metodos[i], p_metodos[i], d_metodos[i], f_metodos[i]))
            # print("\t\t{} & {:.5f} & {:.5f} & {:.5f} \\\\".format(metodos[i], t_metodos[i], p_metodos[i], d_metodos[i]))
            # print("\t\t{} & ${}$ \\\\".format(hs[j], f_metodos))
            plt.plot(x_funcion, y_metodos[i], color=colores[i], label=str(metodos[i]), linewidth=2)
        print("-----------------------------------------------------")
        
        plt.plot(x_funcion, y_analitica, color="black", label="Analítica", linewidth=2)
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()
        print()

    return analitica, derivadas, tiempos, promedios, desviaciones


# Pintar ejemplo de integral con cada método
def ejemplo_integral(funcion, n, a, b, mostrar):
    """
    Entrada: una función funcion(x), un entero n, dos reales a & b y un booleano "mostrar".
    Salida: la integral definida analítica, las integrales definidas calculadas por cada 
            método, los tiempos de ejecución, los errores promedio y las desviaciones de los errores.
    """
    
    analitica = float(sym.integrate(funcion, (x, a, b)))
    integrales, tiempos, errores = [], [], []

    inicio = time.time()
    integrales.append(punto_medio(funcion, a, b, n))
    tiempos.append(time.time() - inicio)
    errores.append(np.abs(analitica - integrales[0]))

    inicio = time.time()
    integrales.append(trapezoide(funcion, a, b, n))
    tiempos.append(time.time() - inicio)
    errores.append(np.abs(analitica - integrales[1]))

    inicio = time.time()
    integrales.append(simpson(funcion, a, b, n))
    tiempos.append(time.time() - inicio)
    errores.append(np.abs(analitica - integrales[2]))

    if (mostrar):

        metodos = ["Punto Medio", "Trapeziode", "Simpson"]
        print("f(x) = {}".format(funcion))
        print("a = {}\nb = {}\nn = {}".format(a, b, n))
        print("∫f(x)dx = {}".format(analitica))

        print("---------------------------------------------------")
        print("                INTEGRACIÓN NUMÉRICA               ")
        print("---------------------------------------------------")
        print(" Método\t\tTiempo\tError\t\t∫f(x)dx")
        print("---------------------------------------------------")

        for i in range(3):
            print(" {}\t{:.5f}\t{:.5f}\t{}".format(metodos[i], tiempos[i], errores[i], integrales[i]))

        print("---------------------------------------------------\n")

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
    funcion = 2*x**4 + 3*x**2 + x
    hs = [1, 2, 3, 4]
    ejemplo_derivada(funcion, hs, 0, 3, True)

    print("EJEMPLO 2")
    funcion = 3**(x + 2) + x
    hs = [1, 2, 3, 4]
    ejemplo_derivada(funcion, hs, 7, 10, True)

    print("EJEMPLO 3")
    funcion = sym.sin(2*x**3)
    hs = [0.1, 0.2, 0.3, 0.4]
    ejemplo_derivada(funcion, hs, 1, 2, True)

    print("INTEGRACIÓN")

    print("EJEMPLO 1")
    funcion = 3*x*sym.cos(x)
    ejemplo_integral(funcion, 1000, -4.5, 3, True)

    print("EJEMPLO 2")
    funcion = x**2 + 7*x**3 + 2*x + 1
    ejemplo_integral(funcion, 2000, -10, 20, True)

    print("EJEMPLO 3")
    funcion = 2**(-x + 5)
    ejemplo_integral(funcion, 3000, -18.5, -10, True)


main()


# ----------------------------------------------------------------------------
# FUNCIONES AUXILIARES

def graficar(x, y, color, title, xlabel, ylabel, label):

    for i in range(len(y)): 
        plt.plot(x, y[i], color=color[i], label=label[i], marker="o")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()


def imprimir(titulo, x, y, columnas):

    print("------------------------------------------------------")
    print(" " + titulo)
    print("------------------------------------------------------")
    print(" {}\t{}\t{}\t{}".format(columnas[0], columnas[1], columnas[2], columnas[3]))
    print("------------------------------------------------------")

    for i in range(len(x)):
        y1, y2, y3 = y[0][i], y[1][i], y[2][i]
        print(" {}\t{:.5f}\t{:.5f}\t{:.5f}".format(x[i], y1, y2, y3))
            
    print("------------------------------------------------------")