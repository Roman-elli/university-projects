#include <stdio.h>
#include <string.h>
#include "../include/projeto.h"

int main(){   

    Sistema *filaR = cria();
    Sistema *filaP = cria();
    
    menu(filaR, filaP);

    destroi(filaR);
    destroi(filaP);

    return 0;
}