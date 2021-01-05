import multiprocessing as mp
import sys
"""
Realiza el Programa1 que instancie, como clase o con el método Process, 10 procesos. Cada uno de los procesos hijos recibirán un valor entero y un caracter (i, c) enviados por el proceso padre, los procesos escribirán en la salida estándar i veces el caracter c.
"""

def codigo_hijo(i,c):
     '''
     Función para proceso hijo que recibirá un valor entero y un
     caracter (i, c) enviados por el proceso padre, escribirá en la salida
     estándar i veces el caracter c.
     '''
     sys.stdout.write('\n'+c*i)

Procesos = []
if __name__ == '__main__':
    for i in range(1,11):
        c = chr(108 + i) #Carácter en ASCII para ir variando parámetros
        proceso = mp.Process(target = codigo_hijo, args = (i,c))
        Procesos.append(proceso)
    for i in range(10):
        Procesos[i].start()
    for i in range(10):
        Procesos[i].join()
