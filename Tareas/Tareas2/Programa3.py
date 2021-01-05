import multiprocessing as mp
import sys
import numpy as np
"""
Refactoriza (reescribe) el Programa2 y elabora el Programa3 donde construyas un mecanismo de sincronización el cual permita escribir en orden todos los caracteres de cada proceso siguiendo una política de ordenpque será una lista de números enteros aleatorios con los índices k de cada proceso hijo. La escritura de los caracteres seguirá la secuencia de ck,i(p) donde cada secuencia ck,i estará definida por la política p
"""

def codigo_hijo(i,c):
     '''
     Función para proceso hijo que recibirá un valor entero y un
     caracter (i, c) enviados por el proceso padre, escribirá en la salida
     estándar i veces el caracter c.
     '''
     mutex.acquire()
     sys.stdout.write(c*i)
     mutex.release()


def politica(seed=None):
    '''
    Función que devuelve una lista aleatoria que definiremos como política
    y asignará los turnos en que los carácteres serán escritos
    '''
    if seed is not None:
        rn = np.random.RandomState(seed)
        pol = rn.choice(10,10,False)
        return pol

    pol = np.random.choice(10,10,False)
    return pol


Procesos = []
# Lista con cadenas correspondientes a cada hijo
cadenas_hijos = ['A','B','C','D','E','F','G','H','I','J','K']
i = 4
seed = 10

if __name__ == '__main__':
    mutex = mp.Lock()
    for j in range(10):
        pol = politica(seed)
        c = cadenas_hijos[pol[j]]
        proceso = mp.Process(target = codigo_hijo, args = (i,c))
        Procesos.append(proceso)



    for j in range(10):
        Procesos[j].start()

    for i in range(10):
        Procesos[i].join()
