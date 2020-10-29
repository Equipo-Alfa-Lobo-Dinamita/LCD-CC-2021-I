
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

#include <sys/wait.h>
//investigar el tipo de variable pid_t

int main(void) {

  pid_t pid;
  int status, died;

  switch(pid = fork()){

    case -1: printf("Error...\n");
            exit(-1);

    case 0: printf("\t Código del hijo: \n");
            int i=1;
            while (i<=10) {
              printf("\t\tEsta es una tarea del proceso hijo: %d\n", i++);
              sleep(1);
            }
            exit(1);

    default: printf("Código del padre \n");
            died = wait(&status); //Espera a que el hijo acabe su proceso. uso &status para poder cachar lo que está sucediendo cuando usamos wait.
            printf("Terminó el proceso hijo %d \n", died );
  }
  // La función main puede o no recibir /regresar argumentos
  return 0;
}
