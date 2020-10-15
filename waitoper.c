#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
   int i;
   int a,b;
   pid_t pidh1,pidh2,pidx;
   int prod,mayor;
   int res;

   printf("\nDame dos enteros: \n");
   //recibe de input dos números
   scanf("%d%d", &a, &b);
   //Crea el proceso hijo
   pidh1 = fork();

// código del padre 1
   if(pidh1)
   {
     // A su vez, va a crear otro proceso hijo
      pidh2 = fork();
      //Código del padre 2
      if(pidh2)
      {
        for(i = 0; i < 2; i++)
        {
           pidx = wait(&res);
           //Corre el resultado del hijo 2
 	   if (pidx == pidh1)
             prod = res;
             //corre el resultado del hijo 1
           else
             mayor = res;
        }
        printf("\n El producto de %d y %d es %d", a,b,prod >> 8);
        printf("\n El mayor de %d y %d es %d \n", a,b,mayor >> 8); //Reducir el valor de saldia, recorrer 8 bits a la derecha el valor
      }
      //Código del hijo 2 que calcula el dato mayor
      else
      {
         if(a > b)
           exit(a);
         else
           exit(b);
      }
   }
// hijo 1 que calcula el producto de dos números
   else
      {
	 prod = a * b;
	 exit(prod);
      }

  return(0);

 }
