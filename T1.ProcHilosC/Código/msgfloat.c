#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h> //archivos de cabecera

int main(void) {

  int pid, pipefd[2]; //creamos un arreglo que guardará 2 enteros. pero después pipefd pasará a ser un canal de comunicación

    float x,y;

        pipe(pipefd); //pipe comunica dos procesos. Pipefd se convertirá en el canal de comunicación debido a la tarea de transformar la variable en canal de comunicación
        pid = fork();

        if (pid){  //código del padre
          close(pipefd[0]);   //cierra el canal en el lugar 0
          printf("\n Soy el padre, dame un número real:" );
          scanf("%f", &x); //es un input
          printf("\n" );
          write(pipefd[1], &x, sizeof(float)); //escribe en la segunda casilla el valor de x.
          // A un canal de comunicación siempre hay que determinar el tamaño de lo que hay que intrpducir en pipe.
          // Esa es la función de sizeof
        }

        else{
          printf("Soy el hijo, " );
          close(pipefd[1]);
          read(pipefd[0], &y, sizeof(float));
          printf("Mensaje recibido: %f", y);
        }


  return 0;
}
