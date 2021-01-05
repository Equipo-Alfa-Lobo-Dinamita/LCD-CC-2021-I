import multiprocessing as mp
import sys
"""
Refactoriza (reescribe) el programa anterior y elabora el Programa2 que incluya un mecanismo de sincronización el cual permita escribir en orden todos los caracteres de cada proceso. Es decir, que se obtengala secuencia c1,1...c1,i, c2,1...c2,i, ..., c10,1...c10,i donde cada subsecuencia ck,i para cada k= 1,2, ...,10 es la secuencia de caracteres del proceso hijo k con longitud i.
Hint:Prueba usar turnos.
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


Procesos = []
# Lista con cadenas correspondientes a cada hijo
cadenas_hijos = ['A','B','C','D','E','F','G','H','I','J','K']
i = 4
if __name__ == '__main__':
    mutex = mp.Lock()
    for j in range(10):
        c = cadenas_hijos[j]
        proceso = mp.Process(target = codigo_hijo, args = (i,c))
        Procesos.append(proceso)

    for j in range(10):
        Procesos[j].start()

    for i in range(10):
        Procesos[i].join()
