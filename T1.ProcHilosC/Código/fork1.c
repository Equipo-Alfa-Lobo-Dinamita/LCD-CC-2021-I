
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

//Se usa void porque no recibe ningún parámetro
int main(void) {
  //pid recibe un valor entero
  int fpid;
  //Creamos un proceso hijo
  fpid = fork();

  printf("ID del proceso: %d\n", fpid );

  //Podemos omitir las llaves en este caso porque solo hay una instrucción
  if (fpid == 0) {
    printf("Proceso hijo\n");
  }

  else{
    printf("Proceso padre\n");
  }

  return 0;
}
