#!/usr/bin/env python
# coding: utf-8

import psutil
import os
import matplotlib.pyplot as plt
import multiprocessing as mp
import random
import time
from itertools import product




geneSet = " abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ!¡.,"



def obtener_aptitud(prediccion, objetivo):
    '''
    Función que calcula el error de la contraseña dada con respecto
    a la predicha
    -----------------------------------
    :param prediccion str: Cadena de la prediccion
    :param objetivo str: Cadena objetivo

    :returns int: Número de carácteres distintos de la prediccion
                con respecto al objetivo
    '''
    return sum(1 for esperado, real in zip(prediccion, objetivo)
               if esperado != real)

class Cromosoma:
    '''
    Clase que irá guardando el cromosoma y su distancia c.r al problema
    a estudiar
    '''
    def __init__(self, genes, aptitud):
        self.Genes = genes
        self.Aptitud = aptitud

def _generar_padre(geneSet,objetivo):
    '''
    Genera una string aleatoria a partir de un Set de genes
    -----------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param objetivo str: Cadena objetivo
    :returns Cromosoma: Cromosoma de un padre aleatorio
    '''
    genes = []
    longitud = len(objetivo)
    while len(genes) < longitud:
        tamañoMuestral = min(longitud - len(genes), len(geneSet))
        #Sample nos toma muestra aleatoria sin reemplazo
        genes.extend(random.sample(geneSet, tamañoMuestral))
    aptitud = obtener_aptitud(genes,objetivo)
    return Cromosoma(genes, aptitud)


def _mutar(padre, geneSet, objetivo):
    '''
    Función de mutación que reemplaza un octavo de genes del cromosoma padre
    ---------------------------------------------------------
    :param padre Cromosoma: Cromosoma padre
    :param geneSet str: Carácteres disponibles
    :param objetivo str: Cadena objetivo
    :returns Cromosoma: Cromosoma de la mutación del padre
    '''
    genesDelNiño = padre.Genes[:]
    idxs = random.sample(range(len(genesDelNiño)),int(len(genesDelNiño)/10))
     #Alterno es un carácter de emergencia por si resulta que
        #la mutación es el mismo gen
    for idx in idxs:
        nuevoGen, alterno = random.sample(geneSet, 2)
        genCorrecto = genesDelNiño[idx]==objetivo[idx]
        if nuevoGen == genesDelNiño[idx] and not genCorrecto:
            genesDelNiño[idx] = alterno
        elif not genCorrecto:
            genesDelNiño[idx] = nuevoGen
    aptitud = obtener_aptitud(genesDelNiño,objetivo)
    return Cromosoma(genesDelNiño, aptitud)

def _cruzar(padre1,padre2, objetivo):
    '''
    Función de cruza entre dos padres para obtener un hijo a partir de la
    combinación de sus genes
    ---------------------------------------------------
    :param padre Cromosoma1: Cromosoma primer padre
    :param padre Cromosoma2: Cromosoma segundo padre
    :param objetivo str: Cadena objetivo
    :returns Cromosoma: Cromosoma de la mutación del padre
    '''
    genesDelNiño = padre1.Genes[:]
    idxs = random.sample(range(len(genesDelNiño)),int(len(genesDelNiño)/2))
    for idx in idxs:
        genesDelNiño[idx] = padre2.Genes[idx]
    aptitud = obtener_aptitud(genesDelNiño,objetivo)
    return Cromosoma(genesDelNiño, aptitud)






def mostrar(candidato,time):
    '''
    Muestra las primeras letras de un cromosoma y su aptitud, así como
    el tiempo
    -----------------------------------------------
    :param candidato Cromosoma: Cromosoma de un candidato a mostrar
    :param time float: Tiempo de inicio
    '''
    if len(candidato.Genes)>50:
        print("Tiempo {:.2f}\t String: {}\t Error:{}".format(time,''.join(candidato.Genes[:50]),
                                             candidato.Aptitud))
    else:
        print("String: {}\t Error:{}".format(''.join(candidato.Genes),
                                             candidato.Aptitud))


# In[4]:



def sig_generacion(geneSet,poblacion, objetivo,
               Padres=[],pmutar = 0.5, pelite = 0.4, resultado=True):
    '''
    Dada una generación de cromosomas (Conjunto de cromosomas),
    regresa una generación posterior con las operaciones de mutacion
    y cruza. Para cada operación genética, se ordenará de mejor a peor
    aptitud de cromosoma, siendo aquellos de mejor aptitud los de mayor
    probabilidad de lograr mutarse o cruzarse.
    -------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite. (Default=.4)
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)

    :returns [Cromosoma]: Conjunto de cromosomas correspondientes a una generación
                        posterior.
    '''

    if Padres == []:
        Padres = [_generar_padre(geneSet, objetivo)
                  for padre in range(poblacion)]
    Padres = sorted(Padres, key = lambda x: x.Aptitud)



    nueva_generacion = []

    for padre in Padres:
        if random.random() < pmutar:
            # Mutar
            gen_a_mutar = 0
            while (random.random()>pelite and gen_a_mutar<len(Padres)-1):
                gen_a_mutar += 1

            mutacion = _mutar(Padres[gen_a_mutar] ,geneSet, objetivo)
            nueva_generacion.append(mutacion)
        else:
            # Cruzar
            gen_1 = 0
            while (random.random()<pelite and gen_1<len(Padres)-1):
                gen_1 += 1

            gen_2 = 0
            while (random.random()<pelite and gen_1 != gen_2 and
                   gen_2<len(Padres)-2):
                gen_2 += 1 + (gen_1==gen_2) #Para evitar que sean iguales

            cruza = _cruzar(Padres[gen_1],Padres[gen_2],objetivo)
            nueva_generacion.append(cruza)


    nueva_generacion = sorted(nueva_generacion, key = lambda x: x.Aptitud)
    if resultado:
        #print([x.Aptitud for x in nueva_generacion])
        mostrar(nueva_generacion[0],time.process_time())

    return nueva_generacion



def iteracion_generaciones(geneSet,poblacion, objetivo, iteraciones, Padres=[],
                       pmutar = 0.5, pelite = 0.8,seed=None):
    '''
    Evoluciona una generación de padres a lo largo de distintas generaciones.
    ----------------------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)
    :param seed int: Semilla aleatoria, en caso de no especificar, será aleatoria.
                    (Default=None)

    :returns Cromosoma: Mejor candidato
    '''
    random.seed(seed)
    Padres = [_generar_padre(geneSet, objetivo)
                  for padre in range(poblacion)]
    resultado = False
    errores = []
    for iteracion in range(iteraciones):

        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

        Padres = sig_generacion(geneSet,poblacion,objetivo,Padres,
                                resultado=resultado)
        errores.append(Padres[0].Aptitud)

        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado
    plt.plot(errores)
    return Padres[0]


##### Modelo Pool

def crear_hijo(Padres,pmutar,pelite,objetivo):
    '''
    Función que elige una operación entre mutar y cruzar, y dados los padres,
    selecciona a alguno para la operación.
    ------------------------------------------------------------
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada.
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar].
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param objetivo str: Cadena objetivo

    :returns Cromosoma: 1 Cruza o mutación
    '''
    if random.random() < pmutar:
        # Mutar
        gen_a_mutar = 0
        #mutacion = Padres[gen_a_mutar]
        while (random.random()>pelite and gen_a_mutar<len(Padres)-1):
            gen_a_mutar += 1

        mutacion = _mutar(Padres[gen_a_mutar] ,geneSet, objetivo)

        return mutacion

    else:
        # Cruzar
        gen_1 = 0
        while (random.random()<pelite and gen_1<len(Padres)-1):
            gen_1 += 1

        gen_2 = 0
        while (random.random()<pelite and gen_1 != gen_2 and
               gen_2<len(Padres)-2):
            gen_2 += 1 + (gen_1==gen_2) #Para evitar que sean iguales

        cruza = _cruzar(Padres[gen_1],Padres[gen_2],objetivo)
        return cruza



def sig_generacion_pool(geneSet,poblacion, objetivo,
                   Padres=[],pmutar = 0.5, pelite = 0.4, resultado=True):
    '''
    Dada una generación, regresa la siguiente generación de genes usando
    la clase Pool.
    ---------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)

    :returns [Cromosoma]: Siguiente Generación
    '''

    if Padres == []:
        Padres = [_generar_padre(longitudObjetivo, geneSet, objetivo)
                  for padre in range(poblacion)]
    Padres = sorted(Padres, key = lambda x: x.Aptitud)



    nueva_generacion = []


    # MP
    # Aquí sucede el cambio del método anterior, lo que sucede aquí
    # Es que se inicializa una Pool que se divide entre los procesadores
    # del sistema
    pool = mp.Pool(mp.cpu_count())
    parametros = [(Padres, pmutar, pelite, objetivo) for _ in range(poblacion)]
    nueva_generacion = pool.starmap(crear_hijo,parametros) # Mappeo a códigos hijo
    # Fin paralelismo

    nueva_generacion = sorted(nueva_generacion, key = lambda x: x.Aptitud)

    if resultado:
        mostrar(nueva_generacion[0],time.process_time())

    return nueva_generacion





def iteracion_generaciones_pool(geneSet,poblacion, objetivo, iteraciones,
                                    Padres=[], pmutar = 0.5, pelite = 0.8,
                                    seed=None):
    '''
    Evoluciona una generación de padres a lo largo de distintas generaciones usando
    el método Pool.
    ----------------------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)
    :param seed int: Semilla aleatoria, en caso de no especificar, será aleatoria.
                    (Default=None)

    :returns Cromosoma: Mejor candidato
    '''
    random.seed(seed)
    Padres = [_generar_padre(geneSet, objetivo)
                  for padre in range(poblacion)]
    resultado = False
    errores = []

    for iteracion in range(iteraciones):

        #print([padre.Genes for padre in Padres])
        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

        Padres = sig_generacion_pool(geneSet,poblacion,objetivo,Padres,
                                resultado=resultado)

        errores.append(Padres[0].Aptitud)

        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

    plt.plot(errores)
    return Padres[0]




# Método concurrente 1: 1 proceso para cada gen, con una población
# grande, se cuelga el sistema
def crear_hijo_concurrente(Padres,pmutar,pelite,objetivo,q):
    '''
    Función que elige una operación entre mutar y cruzar, y dados los padres,
    selecciona a alguno para la operación, esta función recibirá de igual manera
    una cola en el que insertará el resultado.
    ------------------------------------------------------------
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada.
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar].
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param objetivo str: Cadena objetivo
    :param q mp.Queue: Cola que recibirá el hijo
    '''
    random.seed()
    if random.random() < pmutar:
        # Mutar
        gen_a_mutar = 0
        #mutacion = Padres[gen_a_mutar]
        while (random.random()>pelite and gen_a_mutar<len(Padres)-1):
            gen_a_mutar += 1

        mutacion = _mutar(Padres[gen_a_mutar] ,geneSet, objetivo)

        q.put(mutacion)

    else:
        # Cruzar
        gen_1 = 0
        while (random.random()<pelite and gen_1<len(Padres)-1):
            gen_1 += 1

        gen_2 = 0
        while (random.random()<pelite and gen_1 != gen_2 and
               gen_2<len(Padres)-2):
            gen_2 += 1 + (gen_1==gen_2) #Para evitar que sean iguales

        cruza = _cruzar(Padres[gen_1],Padres[gen_2],objetivo)
        q.put(cruza)

def sig_generacion_concurrente(geneSet,poblacion, objetivo,
                   Padres=[],pmutar = 0.5, pelite = 0.4, resultado=True):
    '''
    Dada una generación, regresa la siguiente generación de genes usando
    el primer método de concurrencia usando procesos. Generará 1 proceso
    para cada gen, pero con una población grande, se cuelga el sistema.
    ---------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)

    :returns [Cromosoma]: Siguiente Generación
    '''
    if Padres == []:
        Padres = [_generar_padre(longitudObjetivo, geneSet, objetivo)
                  for padre in range(poblacion)]
    Padres = sorted(Padres, key = lambda x: x.Aptitud)



    nueva_generacion = []


    # MP
    #Inicializa una cola y distintos procesos para cada gen
    q = mp.Manager().Queue()

    procesos = [mp.Process(target=crear_hijo_concurrente,
                           args=(Padres,pmutar,pelite,objetivo,q))
                for i in range(poblacion)]

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()
    #Cada proceso insertó a los genes en la cola, ahora se recuperan
    while q.empty() is False:
        nueva_generacion.append(q.get())


    nueva_generacion = sorted(nueva_generacion, key = lambda x: x.Aptitud)

    if resultado:
        mostrar(nueva_generacion[0],time.process_time())

    return nueva_generacion


def iteracion_generaciones_concurrente(geneSet,poblacion, objetivo, iteraciones,
                                    Padres=[], pmutar = 0.5, pelite = 0.8,
                                    seed=None):
    '''
    Evoluciona una generación de padres a lo largo de distintas generaciones usando
    el primer método de uso de procesos.
    ----------------------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)
    :param seed int: Semilla aleatoria, en caso de no especificar, será aleatoria.
                    (Default=None)

    :returns Cromosoma: Mejor candidato
    '''
    random.seed(seed)
    Padres = [_generar_padre(geneSet, objetivo)
                  for padre in range(poblacion)]
    resultado = False
    errores = []

    for iteracion in range(iteraciones):

        #print([padre.Genes for padre in Padres])
        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

        Padres = sig_generacion_concurrente(geneSet,poblacion,objetivo,Padres,
                                resultado=resultado)

        errores.append(Padres[0].Aptitud)

        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

    plt.plot(errores)
    return Padres[0]


#Método de resolver el problema usando el segundo método concurrente,
# dividirá la tarea entre 4 procesadores

def crear_hijos_concurrente2(Padres,pmutar,pelite,objetivo,num_hijos,q):
    '''
    Función que elige una operación entre mutar y cruzar, y dados los padres,
    selecciona a alguno para la operación, esta función recibirá de igual manera
    una cola en el que insertará los resultados del proceso.
    ------------------------------------------------------------
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada.
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar].
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param objetivo str: Cadena objetivo
    :param num_hijos int: El número de hijos que el proceso generará
    :param q mp.Queue: Cola que recibirá la lista de hijos
    '''
    hijos = []
    random.seed()
    for hijo in range(num_hijos):

        if random.random() < pmutar:
            # Mutar
            gen_a_mutar = 0
            #mutacion = Padres[gen_a_mutar]
            while (random.random()>pelite and gen_a_mutar<len(Padres)-1):
                gen_a_mutar += 1
            mutacion = _mutar(Padres[gen_a_mutar] ,geneSet, objetivo)
            hijos.append(mutacion)


        else:
            # Cruzar

            gen_1 = 0
            while (random.random()<pelite and gen_1<len(Padres)-1):
                gen_1 += 1

            gen_2 = 0
            while (random.random()<pelite and gen_1 != gen_2 and
                   gen_2<len(Padres)-2):
                gen_2 += 1 + (gen_1==gen_2) #Para evitar que sean iguales

            cruza = _cruzar(Padres[gen_1],Padres[gen_2],objetivo)
            hijos.append(cruza)
    q.put(hijos)

def sig_generacion_concurrente2(geneSet,poblacion, objetivo,
                   Padres=[],pmutar = 0.5, pelite = 0.4, resultado=True):
    '''
    Dada una generación, regresa la siguiente generación de genes usando
    el primer método de concurrencia usando procesos. Generará 1 proceso
    para cada gen, pero con una población grande, se cuelga el sistema.
    ---------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)

    :returns [Cromosoma]: Siguiente Generación
    '''

    if Padres == []:
        Padres = [_generar_padre(longitudObjetivo, geneSet, objetivo)
                  for padre in range(poblacion)]
    Padres = sorted(Padres, key = lambda x: x.Aptitud)



    nueva_generacion = []


    # MP
    # Generará una cola y distintos procesos en los cuales se divididirá
    # la tarea de crear una generación. De tal manera que haga 4 procesos.
    nueva_generacion = []
    processes = mp.cpu_count()
    q = mp.Manager().Queue()
    intervalo = int(poblacion/processes)
    procesos = [mp.Process(target=crear_hijos_concurrente2,
                           args=(Padres,pmutar,pelite,objetivo,intervalo,q))
                for i in range(processes)]

    for proceso in procesos:
        proceso.start()

    for i in range(len(procesos)):
        procesos[i].join()


    while not q.empty():
            nueva_generacion+= q.get()

    nueva_generacion = sorted(nueva_generacion, key = lambda x: x.Aptitud)

    if resultado:

        #print([x.Aptitud for x in nueva_generacion])
        mostrar(nueva_generacion[0],time.process_time())

    return nueva_generacion



def iteracion_generaciones_concurrente2(geneSet,poblacion, objetivo, iteraciones,
                                    Padres=[], pmutar = 0.5, pelite = 0.8,
                                    seed=None):
    '''
    Evoluciona una generación de padres a lo largo de distintas generaciones usando
    el segundo método de uso de procesos.
    ----------------------------------------------------------------------
    :param geneSet str: Carácteres disponibles
    :param poblacion int: Número de cromosomas en la siguiente generacion
    :param objetivo str: Cadena objetivo
    :param iteraciones int: Número de iteraciones (generaciones) en las que
                        evolucionará una generación inicial.
    :param Padres [Cromosoma]: Conjunto de cromosomas, en caso de ser
                        una lista vacía, se inicializará una generación
                        aleatoria de cromosomas de igual población a la
                        señalada (Default=[])
    :param pmutar float: Probabilidad de mutar [1-pmutar=Probabilidad de
                        cruzar] (Default=0.5)
    :param pelite float: Probabilidad del primer elemento en ser cruzado/mutado
                        en caso de que no sea el primer elemento el elegido, será
                        el segundo cromosoma el que tenga la probabilidad de ser
                        elegido y así sucesivamente, correspondiendo el cromosoma
                        elegido a una variable aleatoria geométrica con parámetro
                        pelite.
    :param resultado Bool: En caso de ser verdadero, se mostrará el mejor candidato
                        (Default=True)
    :param seed int: Semilla aleatoria, en caso de no especificar, será aleatoria.
                    (Default=None)

    :returns Cromosoma: Mejor candidato
    '''
    random.seed(seed)
    Padres = [_generar_padre(geneSet, objetivo) for padre in range(poblacion)]
    resultado = False
    errores = []

    for iteracion in range(iteraciones):

        #print([padre.Genes for padre in Padres])
        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

        Padres = sig_generacion_concurrente2(geneSet,poblacion,objetivo,Padres,resultado=resultado)

        errores.append(Padres[0].Aptitud)

        if iteracion%int(iteraciones/10) == 0:
            resultado = not resultado

    plt.plot(errores)
    return Padres[0]




## Funciones para la comparación
def cpu_usage(q,finish):
    '''
    Función que monitoreará el uso de los CPUs mientras
    una bandera auxiliar lo indique así hasta un máximo de 500 registros
    donde cada registro se toma cada 0.15 fracción de segundo.
    ----------------------------------------------------------
    :param q mp.Queue: Cola donde se guardará el uso de los procesadores
    :param finish mp.Value: Booleano que indicará cuando detener el registro
                        de los datos.
    '''
    usage = []
    max_count = 500
    i = 0
    while not finish.value and i<max_count:
        i+=1
        time.sleep(0.15)
        usage.append(psutil.cpu_percent(percpu=True))
    #print('Put')
    q.put(usage)
    return





def comparacion(objetivo,poblacion=mp.cpu_count(), iteraciones=500,
                concurrente1=True,concurrente2=True):
    '''
    Función que mostrará el desempeño de los distintos modelos a lo largo de
    las iteraciones al mismo tiempo en que se monitoreará el uso de los distintos
    procesadores a lo largo del tiempo. Al final imprime la comparativa del
    tiempo que tardó cada modelo.
    -------------------------------------------------------------
    :param objetivo str: Cadena Objetivo a predecir
    :param población int: Número de cromosomas en cada generación.
                        (Default=mp.cpu_count())
    :param iteraciones int: Número de iteraciones de cada modelo.(Default=500)
    :param concurrente1 Bool: Bandera que indicará si se utilizará el
                        primer modelo de procesos o no (A grande población,
                        no se recomienda, pues cuelga el sistema)
                        (Default=True)
    :param concurrente2 Bool: Bandera que indicará si se utilizará el
                        segundo modelo de procesos o no. (Default=True)
    :returns [([float],str)]: Listas con el uso de los distintos CPUs así como
                        el nombre del modelo del cual corresponde cada historia
                        de registros de uso.
    '''
    print(f'Poblacion: {poblacion}, Iteraciones: {iteraciones}')
    geneSet = " abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ!¡.,"
    usages = []

    q = mp.Queue()

    finish = mp.Value('i', False)
    cpu_process_secuencial = mp.Process(target=cpu_usage,args=(q,finish))
    cpu_process_secuencial.start()
    start = time.process_time()
    print('Secuencial:')
    iteracion_generaciones(geneSet,poblacion,objetivo,iteraciones,
                           pmutar=0.6,pelite=0.65)
    end_secuencial = (time.process_time()-start)
    finish.value = True
    usage_secuencial= q.get()
    cpu_process_secuencial.join()
    usages.append((usage_secuencial,'Secuencial'))

    end_concurrente1 = 'No aplica'

    if concurrente1:
        print('Concurrente1:')
        finish.value = False
        cpu_process_concurrente = mp.Process(target=cpu_usage,args=(q,finish))
        cpu_process_concurrente.start()
        start_concurrente = time.process_time()
        iteracion_generaciones_concurrente(geneSet,poblacion,objetivo,iteraciones,
                                           pmutar=0.6,pelite=0.65)
        end_concurrente1 = (time.process_time()- start_concurrente)
        finish.value = True
        cpu_process_concurrente.join()
        usage_concurrente= q.get()
        usages.append((usage_concurrente,'Concurrente1'))

    end_concurrente2 = 'No aplica'
    if concurrente2:
        print('Concurrente2:')
        finish.value = False
        cpu_process_concurrente2 = mp.Process(target=cpu_usage,args=(q,finish))
        cpu_process_concurrente2.start()
        start_concurrente2 = time.process_time()
        iteracion_generaciones_concurrente2(geneSet,poblacion,objetivo,iteraciones,
                                           pmutar=0.6,pelite=0.65)
        end_concurrente2 = (time.process_time()- start_concurrente2)
        finish.value = True
        cpu_process_concurrente2.join()
        usage_concurrente2= q.get()
        usages.append((usage_concurrente2,'Concurrente2'))


    finish.value = False
    print('Pool:')
    cpu_process_pool = mp.Process(target=cpu_usage,args=(q,finish))
    cpu_process_pool.start()
    start_pool = time.process_time()
    iteracion_generaciones_pool(geneSet,poblacion,objetivo,iteraciones,
                                    pmutar=0.6,pelite=0.65)
    end_pool = (time.process_time()- start_pool)
    finish.value = True
    usage_pool= q.get()
    cpu_process_pool.join()
    usages.append((usage_pool,'pool'))

    print(f'\nSecuencial: {end_secuencial:>4.3f}\t Concurrente1: {end_concurrente1:>4.3f}\nConcurrente2: {end_concurrente2:>4.3f}\t Pool: {end_pool:>4.3f} \n','*'*50)

    return usages






def plot_cpu(objetivo,poblacion,iteraciones,concurrente1=True,concurrente2=True):
    '''
    Función que imprime la comparativa de cada modelo y al final, el uso en los primeros
    instantes de los distintos CPUs para comparar su desempeño. Al final salva las gráficas
    en la carpeta Plots/
    -------------------------------------------------------------
    :param objetivo str: Cadena Objetivo a predecir
    :param población int: Número de cromosomas en cada generación.
    :param iteraciones int: Número de iteraciones de cada modelo.
    :param concurrente1 Bool: Bandera que indicará si se utilizará el
                        primer modelo de procesos o no (A grande población,
                        no se recomienda, pues cuelga el sistema)
                        (Default=True)
    :param concurrente2 Bool: Bandera que indicará si se utilizará el
                        segundo modelo de procesos o no. (Default=True)
    '''
    uso_cpu = comparacion(objetivo,poblacion,iteraciones,
                            concurrente1, concurrente2)


    for modelo,nombre in uso_cpu:
        fig = plt.figure(figsize=(30,7))
        usage_max = min(len(modelo),150)
        usage = modelo[:usage_max]
        for i in range(mp.cpu_count()):
            plt.plot([cpu[i] for cpu in usage], label = f'CPU{i}')
        plt.legend(loc='best')
        plt.title(f'Uso del cpu en modelo {nombre}\nPoblacion: {poblacion}')
        fig.savefig(f'Plots/Modelo{nombre}_Poblacion{poblacion}.png', dpi=fig.dpi)



if __name__ == '__main__':
    objetivo = open('Lorem ipsum')
    objetivo = objetivo.read()
    #usage = comparacion(objetivo,iteraciones=200)
    plot_cpu(objetivo,8,50,concurrente1=True)
    plot_cpu(objetivo,50,50,concurrente1=True)
    plot_cpu(objetivo,500,50,concurrente1=False)
