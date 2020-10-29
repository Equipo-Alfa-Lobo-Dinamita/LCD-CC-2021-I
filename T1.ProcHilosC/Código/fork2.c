#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
  int i = 1;

  //La estructura switch es para ejecutar código dependiendo de ciertas condiciones
  switch(fork()){

    // Código para el error
    //si el programa no puede ejecutar el código, devuelve -1
    case -1:
      perror("Error al crear el proceso"); //incluida en unistd.h
      exit(-1);
      break; //Termino el switch


    //Cuando fork devuelve un 0, se creo un proceso hijo
    case 0:
    //código para el proceso hijo
      while (i<=10) {
        //Pone a dormir a la ejecución 1 segundo
        sleep(1);
        // \t es un tabulador
        printf("\t Soy el proceso hijo %d\n", i++ );
      }
      break;

    //Falta el proceso padre con cualquier otro ID
    //default sirve como un else
    default:
      //código proceso padre
      while (i<=10) {
        printf("Soy el proceso padre: %d\n", i++ );
        sleep(2);
      }

  }
  return 0;
}
