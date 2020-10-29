
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>


int main(void) {

  int i;
  int padre;

  padre = 1;

  for (i = 1; i <=3; i++) {
    if (padre == 1) {
      //Creamos otro proceso
      if (fork() ==0){ //proceso hijo
        printf("\t Proceso hijo %d, con ID: %d y padre ID: %d\n",i, getpid(),getppid() );
        padre=0;
      }

      else{ //proceso padre
        printf("Proceso padre con ID: %d\n", getpid() );
        padre=1;
      }
    }
  }


  return 0;
}
