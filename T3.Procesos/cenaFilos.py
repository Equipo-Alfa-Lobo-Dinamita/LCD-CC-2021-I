#Entonces el de varios turnos
class filosofo:
    def __init__(self,...):

    def agarraTenedor(self,direccion):
        stuff
    def dejarTenedor(self,direccion):
        stuff
    def comer(self):
        stuff

filosofo1=filosofo()
filosofo2=filosofo()
filosofo3=filosofo()
filosofo4=filosofo()
filosofo5=filosofo()
mesa = [filosofo1,filosofo2,filosofo3,filosofo4,filosofo5]



#Hilo i

def izq_tomar(filosofo):
    try{
    filosofo.tomarTenedor(izq)
    while(!derecha.libre){
        wait()
    }
    filosofo.agarraTenedor(derecha)
    filosofo.comer()
    filosofo.dejarTenedor(izq)
    filosofo.dejarTenedor(derecha)
    }

def derecha_tomar(filosofo):
    try{
        filosofo.agarraTenedor(derecha)
        while(!izq.libre){
            wait()
        }
        filosofo.agarraTenedor(izq)
        filosofo.comer()
        filosofo.dejarTenedor(izq)
        filosofo.dejarTenedor(derecha)
    }


filosofo1.add(izq_tomar)
for i in range(1,len(mesa)):
    mesa[i].add(derecha_tomar)

# Varios turnos

for i in range(len(mesa)):
    if i%1:
        mesa[i].add(izq_tomar)
    else:
        mesa[i].add(derecha_tomar)
