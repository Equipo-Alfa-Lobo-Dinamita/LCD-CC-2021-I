#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//Define el número de hilos a crear
#define NUM_HILOS 5

//Todos los hilos van a compartir la variable I
int I = 0;
//Código de los hilos:
void *codigo_del_hilo(void *id)
{
    int i;
    for(i = 0; i < 50; i++)
    //Nos dice qué hilo va en cuál iteración de la I
      printf("Hilo %d; i = %d, I = %d\n", *(int*)id, i, I++);
 pthread_exit(id);
}


int main(void)
{
    int h;
    pthread_t hilos[NUM_HILOS];
    int id[NUM_HILOS] = {1, 2, 3, 4, 5};
    int error;
    int *salida;
    //Ejecuta éste bloque para cada hilo
    for (h = 0; h < NUM_HILOS; h++){
        error = pthread_create(&hilos[h], NULL, codigo_del_hilo, &id[h]);
        if (error){
          fprintf(stderr, "Error %d %s\n", error, strerror (error));
          exit(-1);
        }

    }

    //Este bloque va a esperar a que cada hilo termina e imprime que ese hilo ya terminó
    for (h = 0; h < NUM_HILOS; h++){
        error = pthread_join(hilos[h], (void **)&salida);
        if (error)
          fprintf(stderr, "Error %d %s\n", error, strerror (error));
        else
          printf("hilo %d terminado\n", *salida);
    }
}
