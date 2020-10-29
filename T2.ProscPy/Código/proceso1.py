from multiprocessing import Process
import os

def info():
    print ('El nombre del modulo:', __name__)
    if hasattr(os, 'getppid'):
        print ('Proceso padre PID:', os.getppid())
    print ('PID:', os.getpid())

def greeting(nombre):
    print('\nSoy codigo del proceso creado')
    print (f'hello {nombre}')
    print ('Proceso padre PID:', os.getppid())
    print ('PID:', os.getpid())

if __name__ == '__main__':
    info()
    p = Process(target=greeting, args=('Comunidad de la LCD',))
    p.start()
    p.join()
