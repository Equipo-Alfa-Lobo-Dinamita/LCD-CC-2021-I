// # es una Llamada a una macro
#include <stdio.h>
#include <sys/types.h> //Se definen tipos de datos derivado básicos Parte del estandar POSICS
#include <unistd.h> //Nos ayuda a manejar las variables y constantes para hacer la crración de procesos y sincronisación de procesos Parte del estandar POSICS

int main(void) {
  //Las siguientes funciones están incluidas en unistd.h
  // %d recibe la cadena que está después de la coma %d recibe decimal
  // %s recibe strings
  // %c recibe chars
  printf("ID de proceso:%d \n",getpid() );
  printf("ID de proceso padre:%d\n",getppid() );
  printf("ID de usuario propietario:%d\n", getuid() );

  return 0;
}
