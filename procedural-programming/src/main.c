#include <stdio.h>
#include <string.h>
#include "../include/project.h"

int main(){   

    System *reservation_queue = create_queue();
    System *pre_reservation_queue = create_queue();
    
    print_menu(reservation_queue, pre_reservation_queue);

    destroi(reservation_queue);
    destroi(pre_reservation_queue);

    return 0;
}