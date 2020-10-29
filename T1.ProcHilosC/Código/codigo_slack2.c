#include <pthread.h> //Agregamos esta cabecera para implementar el uso de hilos
#include <stdio.h>
void *codigo_del_hilo(void *id)
{
 int i;
 for(i = 0; i < 50; i++)
 //El *(int*) es un casteo, o conversion explicita a ese tipo de dato
 //Primero trae lo del apuntador y luego lo convierte a entero
  printf("\n Soy el hilo: %d, iter = %d", *(int*)id, i);
 pthread_exit(id);
}
int main(void)
{
  pthread_t hilo1, hilo2;
  int id1 = 11;
  int id2 = 55;
  //int *salida;
  //Creamos dos hilos
  pthread_create(&hilo1, NULL, codigo_del_hilo, &id1);
  pthread_create(&hilo2, NULL, codigo_del_hilo, &id2);
  //Después esperamos a que los hilos terminen
  pthread_join(hilo1, NULL);
  pthread_join(hilo2, NULL);
  printf("\n Hilos terminados \n");
  return(0);
}
