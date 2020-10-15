#include <pthread.h>
#include <stdio.h>

//El siguiente es el código que va a ejecutar el hilo, va a contar 50 iteraciones
void *codigo_del_hilo(void *id)
{
 int i;
 for(i = 0; i < 50; i++)
  printf("\n Soy el hilo: %d, iter = %d", *(int*)id, i);
 pthread_exit(id); //Sale del hilo, pues no es proceso, es hilo
}
//código principal
int main(void)
{
  pthread_t hilo;
  int id = 245;
  int *salida;
  //Crea un hilo con NULL se crearán sus atributos por defecto, el parámetro codigo_del_hilo indica la función que va a ejecutar
  // Si fue exitosa la creación del hilo, regresa 0
  pthread_create(&hilo, NULL, codigo_del_hilo, &id);
  pthread_join(hilo, NULL);
  printf("\n Hilo %d terminado \n", *salida);
  return(0);
}
