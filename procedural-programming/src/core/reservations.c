#include "../../include/projeto.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void book_service(System *reservation_queue, System *pre_reservation_queue, Time app_present_time){
        Person insert;
        printf("\n [1] Booking ---- [2] Pre-booking\n\n>>> ");
                insert.work = checkint();
                if(insert.work == 1 || insert.work == 2){
                        printf("\n [1] Wash (30 MINUTES) ---- [2] Maintenance (1 HOURs)\n\n>>> ");
                        insert.func = checkint();;
                        if((insert.work == 1 || insert.work == 2) && (insert.func == 1 || insert.func == 2)){
                        printf("\nWrite your name: ");
                        fgets(insert.name, MAX, stdin);
                        insert.name[strcspn(insert.name, "\n")] = '\0';
                        printf("\nActual date: %02d / %02d / %d *\n\nInsert your booking time info.\n\nYear: ", app_present_time.day,app_present_time.month,app_present_time.year);
                        insert.year = checkint();

                        /* Caso o year seja leap_year */
                                if(leap_year(insert.year) && insert.year >= app_present_time.year){
                                printf("Month: ");
                                insert.month = checkint();

                                /* Caso month seja valido */
                                if(insert.month >=1 && insert.month <= 12 && (insert.year > app_present_time.year || (insert.year == app_present_time.year && insert.month >= app_present_time.month))){
                                        printf("Day: ");
                                        insert.day = checkint();

                                        /* Caso o day seja válido */
                                        if(check_day(insert.day,insert.month,1) && (insert.year > app_present_time.year || (insert.year == app_present_time.year && insert.month > app_present_time.month) || (insert.year == app_present_time.year && insert.month == app_present_time.month && insert.day >= app_present_time.day))){
                                        
                                        /* print_queue as reservas e pré-reservas específicas do day */
                                        if(insert.work == 1) print_specific_bookings(reservation_queue, insert);
                                        else print_specific_bookings(pre_reservation_queue, insert);
                                        
                                        printf("\nHours of operation from 8:00 a.m. to 6:00 p.m. (Maintenance can be booked until 5:00 p.m.)\n");
                                        printf("\nHour: ");
                                        insert.hour = checkint();
                                        if(insert.hour >= 8 && insert.hour < 18){
                                                printf("\nMinutes are marked only at 0 and 30 minutes.\n\nMinutes: ");
                                                insert.min = checkint();
                                                if(insert.min != 0 && insert.min != 30) printf("*** This minutes are invalid ***\n");
                                                else if (insert.func == 2 && insert.hour == 17 && insert.min == 30) printf("*** Is not possible to schedule a booking for this date. ***\n"); 
                                                else if(insert.work == 1) create_service(reservation_queue, pre_reservation_queue,insert,1);
                                                else create_service(pre_reservation_queue, NULL,insert,1);
                                        }
                                        else printf("\n*** Invalid hour. ***\n");
                                        }
                                        else printf("\n*** Invalid day. ***\n");
                                }
                                else printf("\n*** Invalid month. ***\n");  
                                }

                                /* Caso o year não seja leap_year */
                                else if(insert.year >= app_present_time.year){
                                printf("Month: ");
                                insert.month = checkint();

                                /* Caso month seja valido */
                                if(insert.month >= 1 && insert.month <= 12 && (insert.year > app_present_time.year || (insert.year == app_present_time.year && insert.month >= app_present_time.month))){
                                        printf("Day: ");
                                        insert.day = checkint();

                                        /* Caso o day seja válido */
                                        if(check_day(insert.day, insert.month,0) && (insert.year > app_present_time.year || (insert.year == app_present_time.year && insert.month > app_present_time.month) || (insert.year == app_present_time.year && insert.month == app_present_time.month && insert.day >= app_present_time.day))){
                                        
                                        /* print_queue as reservas e pré-reservas específicas do day */
                                        if(insert.work == 1) print_specific_bookings(reservation_queue, insert);
                                        else print_specific_bookings(pre_reservation_queue, insert);
                                        
                                        printf("\nHours of operation from 8:00 a.m. to 6:00 p.m. (Maintenance can be booked until 5:00 p.m.)\n");
                                        printf("\nHora: ");
                                        insert.hour = checkint();
                                        
                                        if(insert.hour >= 8 && insert.hour < 18){
                                                printf("\nMinutes are marked only at 0 and 30 minutes.\n\nMinutes: ");
                                                insert.min = checkint();
                                                
                                                if(insert.min != 0 && insert.min != 30) printf("*** Invalid minutes ***\n");
                                                else if (insert.func == 2 && insert.hour == 17 && insert.min == 30) printf("Is not possible to schedule a booking for this date.\n"); 
                                                else if(insert.work == 1) create_service(reservation_queue, pre_reservation_queue,insert,1);
                                                else create_service(pre_reservation_queue, NULL,insert,1);  
                                        }
                                        else printf("\n*** Invalid hour ***\n");
                                        }
                                        else printf("\n*** Invalid day ***\n");
                                }
                                else printf("\n*** Invalid month ***\n");              
                                }
                                else printf("\n*** Invalid year ***\n"); 
                        }              
                        else printf("\n*** This function does not exist. Please re-enter the option you want ***\n");
                }else printf("\n***This function does not exist. Please re-enter the option you want. ***\n");
}

void create_service (System *list, System *pre_reservation_list, Person p1, int x){ 
        if(check_time_spot(list,p1)){
                System *no, *ant, *temp_pointer;
                no = (System *) malloc (sizeof (System));
                if (no != NULL) {
                        no->user = p1;
                        search (list, p1, &ant, &temp_pointer);
                        no->next = ant->next;
                        ant->next = no; 
                        if(p1.work == 1 && x == 1)printf("\nReservation successfully completed!!\n");
                        else if(x == 1) printf("\nPre-reservation successfully completed\n");
                }
        }
        else{
                int option = 0;
                printf("This time slot is already booked. Would you like to join a waiting list for this time slot?\n");
                while(!option){
                        printf("[1] Yes ---- [2] No\n>>> ");
                        option = checkint();
                        if(option == 1){
                                p1.work = 2;
                                create_service(pre_reservation_list, NULL,p1,0);
                                printf("Your pre-booking has been successfully completed\n");
                        }
                        else if(option == 2) printf("I apologize for the inconvenience. If you still wish to book a service, check the third function of the application and check the available times!\n");              
                        else{
                                printf("Invalid option. Please re-enter the desired option.\n");
                                option = 0;
                        }
                }
        }
}

void print_user_reservations(System *queue, System *pre_reservation_queue, char *name){
        int exists = 0;
        printf("Bookings of %s:\n", name);
        printf("\n%8s%15s%12s\n", "Date", "Time", "Service");
        for(System *aux = queue->next; aux != NULL; aux = aux->next){
                if(strcmp(aux->user.name, name) == 0){
                        exists++;
                        if(aux->user.func == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Wash");
                        else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Maintenance");     
                }
        }
        if(exists == 0) printf("%8s%14s%10s\n", "----", "-------", "------");       
        exists = 0;
        printf("\nPre-bookings of %s:\n\n", name);
        printf("%8s%15s%12s\n", "Date", "Time", "Service");
        for(System *aux = pre_reservation_queue->next; aux != NULL; aux = aux->next){
                if(strcmp(aux->user.name, name) == 0){
                        exists++;
                        if(aux->user.func == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Lavagem");
                           
                        else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Manutenção");
             }
        
        }
        if(exists == 0) printf("%8s%14s%10s\n", "----", "-------", "------");       
}

void print_specific_bookings(System *list, Person p1){
        printf("Reservations made at %02d / %02d / %d:\n", p1.day,p1.month,p1.year);
        System *aux = list->next;
        int exists = 0;
        printf("%8s%15s%12s%12s%16s\n", "Date", "Time", "Service", "Type", "User");
        while((aux) != NULL){
                if(aux->user.day == p1.day && aux->user.month == p1.month && aux->user.year == p1.year){
                        if(aux->user.func == 1){
                                if(aux->user.work == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Lavagem", "Reserva", aux->user.name);
                                                               
                                else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Lavagem", "Pré-reserva", aux->user.name);
                        }
                        if(aux->user.func == 2){
                                if(aux->user.work == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Manutenção", "Reserva", aux->user.name);
                                                                      
                                else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Manutenção", "Pré-reserva", aux->user.name);
                        }
                        exists++;
                        }
                aux = aux->next;
                }
        if(exists == 0) printf("%8s%14s%10s%12s%16s\n", "----", "-------", "------", "----", "-------");       
}

void check_specific_user(System *list, char *name){
        System *aux = list->next;
        int counter = 0;
        int exists = 0;
        if(!isEmpty(list) && aux->user.work == 1) printf("\nReservations of %s:\n", name);
        else if(!isEmpty(list)) printf("\n Pre-reservations of %s:\n", name);
        printf("\n%8s%15s%12s\n", "Date", "Time", "Service");
        while((aux) != NULL){
                counter++;
                aux = aux->next;
        }
        while(counter != 0){
                System *aux = list;
                for(int i = 0; i <= counter; i++){
                        if(i == counter && strcmp(aux->user.name,name) == 0){
                                exists++;
                                if(aux->user.func == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Lavagem");
                        if(aux->user.func == 2) printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Manutenção");
                            
                        }
                        aux = aux->next;               
                }
                counter--;
        }
        if(exists == 0) printf("%8s%14s%10s\n", "----", "-------", "------");       
}

void cancel_service(System *reservation_list, System *pre_reservation_list, Time actual){
        Person user;
        int error = 0;
        printf("Fill in the details to cancel!\n");
        printf("Write the book owner name: ");
        fgets(user.name,MAX,stdin);
        user.name[strcspn(user.name, "\n")] = '\0';
        print_user_reservations(reservation_list, pre_reservation_list, user.name);
        printf("\n[1] Cancel booking ---- [2] Cancel pre-booking\n\n>>> ");
        user.work = checkint();
        if(user.work == 1 || user.work == 2){
                printf("* Real time date: %02d / %02d / %d *\n", actual.day,actual.month,actual.year);
                printf("Year: ");
                user.year = checkint();
                if(user.year >= actual.year){
                        printf("Month: ");
                        user.month = checkint();
                        if(user.month >=1 && user.month <= 12 && (user.year > actual.year || (user.year == actual.year && user.month >= actual.month))){
                                printf("Day : ");
                                user.day = checkint();
                                if((user.year > actual.year || (user.year == actual.year && user.month > actual.month) || (user.year == actual.year && user.month == actual.month && user.day >= actual.day))){
                                        printf("Hour: ");
                                        user.hour = checkint();
                                        if(user.hour >= 8 && user.hour <= 17){
                                                printf("Minutes: ");
                                                user.min = checkint();
                                        }else{ printf("\nInvalid hour\n"); error++;}
                                }else {printf("\nInvalid day\n"); error++;}
                        }else {printf("\nInvalid month\n"); error++;}
                }else {printf("\nInvalid year\n"); error++;}
        }else {printf("\nThis function don't exists\n"); error++;}

        System *ant, *app_present_time;
        if(user.work == 1 && error == 0){
                /* Eliminar e checar pré-reserva! */
                search_booking_by_username (reservation_list, user, &ant, &app_present_time,1);
                if (app_present_time != NULL) {
                        ant->next = app_present_time->next;
                        free(app_present_time);
                        printf("The %s booking was successfully cancelled.\n", user.name);
                        /* Verifica pré-reserva e substitui */
                        update_queues(pre_reservation_list,reservation_list);
                }
                else printf("User not found\n");
        }
        else if(user.work == 2 && error == 0){
                /* Eliminar pré-reserva */
                search_booking_by_username (pre_reservation_list, user, &ant, &app_present_time,1);
                if (app_present_time != NULL) {
                        ant->next = app_present_time->next;
                        free (app_present_time);
                        printf("The %s pre-booking was successfully cancelled.\n", user.name);
                }
                else printf("User not found\n");
        }
}

void update_queues(System *pre_reservation_list, System *reservation_list){
        System *aux = pre_reservation_list->next;
        System *temp = pre_reservation_list;
        while (aux != NULL) {
                aux->user.work = 1;
                if(check_time_spot(reservation_list, aux->user)){
                        create_service(reservation_list, NULL,aux->user,0);
                        temp->next = aux->next;  // atualiza o ponteiro do elemento anterior
                        free(aux);  // Libera a memória do elemento
                        aux = temp->next;  // app_present_timeiza o ponteiro auxiliar
                } else {
                aux->user.work = 2;
                temp = aux;  // app_present_timeiza o ponteiro temporário
                aux = aux->next;  // app_present_timeiza o ponteiro auxiliar
                }
        }
}

void execute_service(System *reservation_list, System *pre_reservation_list){
        System *aux = reservation_list->next;
        if(!isEmpty(reservation_list)){
                reservation_list->next = aux->next;
                if(!isEmpty(pre_reservation_list)){
                        update_queue_by_real_time(pre_reservation_list,aux->user);                        
                }
                free(aux);
        }
}