#--------------- Ejemplo Mutex---------------------
import time
from threading import Thread
from threading import Lock
import random

def myfunc(i, mutex):
    try:
        mutex.acquire(1)
        time.sleep(1)
        print("Thread:",i)
    except Exception as e:
        print(e)
    finally:
        mutex.release()


mutex = Lock()
for i in range(0,10):
    t = Thread(target=myfunc, args=(i,mutex))
    t.start()
    print("main loop", i)


#--------------Fisofos----------------------



class filosofo(multiprocessing.Process):
    #  1==libre, 0==ocupado, inicializamos la lista en 1s porque todos los tenedores están libres
    tenedores = [1]*10
    def __init__(self,numero):
        '''
         0<= numero <=10
        '''
        super(filosofo, self).__init__()
        self.numero = numero
        self.tenedorIzquierdo = tenedores[numero]
        self.tenedorDerecho = tenedores[(numero+1)%10]


    def run(self):
        print("Child Process PID: {}".format(multiprocessing.current_process().pid))
        return


    def agarrarTenedor(self,lado):
        while True:
            if lado  == "izquierda":
                if self.tenedorIzquierdo == 1:
                    self.tenedorIzquierdo = 0
                    return
                else:
                    print("Tenedor izquierdo esta ocupado")
                    wait(10)

            elif lado  == "derecha":
                if self.tenedorDerecho == 1:
                    self.tenedorDerecho = 0
                    return
                else:
                    print("Tenedor derecho esta ocupado")
                    wait(10)
        return

    def comer(self):
        os.sleep(1)
        return

    def rutina(self):
        pname = self.numero()
        while(notHungry()):
            sleep(100)

        if (pname%2 == 0):
            try:
                self.agarrarTenedor(izquierda)
                self.agarrarTenedor(derecha)
                self.comer()
                self.dejarTenedor(derecha)
                self.dejarTenedor(izquierda)
        else:
            try:
                self.agarrarTenedor(derecha)
                self.agarrarTenedor(izquierda)
                self.comer()
                self.dejarTenedor(derecha)
                self.dejarTenedor(izquierda)

        return




def hacerfilosofo(numero):
    filosofo_actual = filosofo(numero)
    filosofo_actual.rutina()
    return


def notHungry():
    return (random.randint(1, 5) != 3)


filosofos = {}
for numero in range(10):
    filosofo[numero] = Thread(target = hacerfilosofo, args = (numero,))
for numero in range(10):
    filosofo[numero].start()
for numero in range(10):
    filosofo[numero].join()
#for numero in range(10):#
#    filosofo[numero].rutina()
