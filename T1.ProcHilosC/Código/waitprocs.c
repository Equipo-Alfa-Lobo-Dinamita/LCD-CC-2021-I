#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

# define NUM_PROCESOS 5
int I = 0;

// El siguiente va a ser un código que va a ejecutar el proceso hijo
void codigo_del_proceso (int id)
{
   int i;
   //Cuenta 50 veces
   for (i = 0; i < 50; i++)
        printf("Proceso %d: i = %d, I = %d\n", id, i, I++ );
   exit (id); //Sale del proceso

}

int main(void)
{
    int p;
    //El número de procesos a crear:
    int id[NUM_PROCESOS] = {1, 2, 3, 4, 5};
    int pid;
    int salida;

    for (p = 0; p < NUM_PROCESOS; p++) {
      //Crea 5 procesos hijos
      pid = fork();
      //Caso en el que no se puede crear un proceso hijo
      if  (pid == -1){
          perror("Error al crear un proceso: ");
          exit(-1);
      }
      else if (pid == 0) /* codigo proceso hijo */ //Para cada hijo ejecuta el código codigo_del_proceso
          codigo_del_proceso (id[p]);
    }

    // codigo proceso padre
    for (p = 0; p < NUM_PROCESOS; p++) {
        //Cada proceso espera a que su hijo termine
        pid = wait(&salida);
        //Imprime el código del proceso con su estado recorrido 8 bits a la derecha
        printf("Proceso %d con id = %x terminado\n", pid, salida >> 8);
    }

    return(0);
}
