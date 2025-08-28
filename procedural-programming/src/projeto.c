#include "../include/projeto.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

void print_menu(System *reservation_queue, System *pre_reservation_queue){
        /* opening */
    printf("      ____      -------------------------------------------------------------------------------      ____     \n");
    printf("   __/  | \\__   | Welcome to ManuWash! Book car washes and maintenance services conveniently! |   __/ |  \\__   \n");
    printf("  '--0----0--'  -------------------------------------------------------------------------------  '--0----0--'  \n\n");

    /* define the real time moment */
    int x = 1;
    Time app_present_time;
    while(x){
        printf("Which date do your want to run ManuWash:\n\nYear >>> ");
        app_present_time.year = checkint();
        if(app_present_time.year >= 0 && leap_year(app_present_time.year)){
            printf("Month >>> ");
            app_present_time.month = checkint();
            if (app_present_time.month >=1 && app_present_time.month <= 12){
            printf("Day >>> ");
            app_present_time.day = checkint();
            if(check_day(app_present_time.day,app_present_time.month,1)) x = 0;
            else printf("\n*** Invalid Day ***\n");
            }
            else printf("\n*** Invalid Month ***\n");
        }
        else if(app_present_time.year >= 0 && !leap_year(app_present_time.year)){
            printf("Month >>> ");
            app_present_time.month = checkint();
            if (app_present_time.month >=1 && app_present_time.month <= 12){
            printf("Day >>> ");
            app_present_time.day = checkint();
            if(check_day(app_present_time.day,app_present_time.month,0)) x = 0;
            else printf("\n*** Invalid Day ***\n");
            }
            else printf("\n*** Invalid Month ***\n");
        }
        else printf("\n*** Invalid Year ***\n");
    }
    
    /* User interaction */
    x = 1;
    int option;

    while(x){
        printf("\nAvailable options:\n");
        printf("1: Book a wash or maintenance.\n");
        printf("2: Cancel a booking/Pre-booking.\n");
        printf("3: List bookings and pre-bookings for washes and maintenance sorted by date in ascending order.\n");
        printf("4: List bookings and pre-bookings of a client sorted by date in descending order.\n");
        printf("5: Options for task execution.\n");
        printf("6: Update waiting list.\n");
        printf("7: Load lists.\n");
        printf("8: Save lists.\n");
        printf("9: Exit program.\n");
        printf("\nEnter the option you want: ");

        option = checkint();

        switch(option){
            case 1:
                book_service(reservation_queue,pre_reservation_queue,app_present_time);
                break;
            case 2:
                cancel_service(reservation_queue,pre_reservation_queue, app_present_time);
                break;
            case 3:
                printf("\nList of reservations in ascending order: \n\n");
                print_queue(reservation_queue);
                printf("\nList of pre-reservations in ascending order: \n\n");
                print_queue(pre_reservation_queue);
                break;
            case 4:
                char name[MAX];
                printf("\nEnter the name of the person who wishes to access reservations and pre-reservations:\n>>> ");
                fgets(name,MAX,stdin);
                name[strcspn(name, "\n")] = '\0';
                check_specific_user(reservation_queue,name);
                check_specific_user(pre_reservation_queue,name);
                break;
            case 5:
                printf("\nAvailable options:\n\n");
                int choice = 0;
                while(choice != 3){
                    printf("1: Execute most recent task.\n");
                    printf("2: Change app real time.\n");
                    printf("3: Return to print_menu.\n\n>>> ");
                    choice = checkint();
                    if(choice == 1){
                        if(!isEmpty(reservation_queue)){
                        execute_service(reservation_queue,pre_reservation_queue);
                        printf("\nMost recent reservation executed.\n");
                        }else printf("\n*** There are no reservations to be executed at this time. ***\n");
                        choice = 3;
                    }
                    if(choice == 2){
                        int y = 1;
                        while(y){
                            printf("\nPlease fill in the details of the new date you are interested in so that we can update the lists.\n");
                            printf("Year >>> ");
                            app_present_time.year = checkint();;
                            if(app_present_time.year >= 0 && leap_year(app_present_time.year)){
                                printf("Month >>> ");
                                app_present_time.month = checkint();
                                if (app_present_time.month >=1 && app_present_time.month <= 12){
                                    printf("Day >>> ");
                                    app_present_time.day = checkint();
                                if(check_day(app_present_time.day,app_present_time.month,1)) y = 0;
                                else printf("Invalid Day.\n");
                                }
                                else printf("Invalid Month.\n");
                            }
                            else if(app_present_time.year >= 0 && !leap_year(app_present_time.year)){
                                printf("Month >>> ");
                                app_present_time.month = checkint();
                                if (app_present_time.month >=1 && app_present_time.month <= 12){
                                    printf("Day >>> ");
                                    app_present_time.day = checkint();
                                if(check_day(app_present_time.day,app_present_time.month,0)) y = 0;
                                else printf("Invalid Day.\n");
                                }
                                else printf("Invalid Month.\n");
                            }
                            else printf("Invalid Year.\n");
                        }
                        update_time(pre_reservation_queue, app_present_time);
                        update_time(reservation_queue,app_present_time);
                        printf("\nTime successfully updated!!\n");
                        choice = 3;
                    }
                }
                break;
            case 6:
                update_queues(pre_reservation_queue,reservation_queue);
                printf("\n*** Updated queue. ***\n");
                break;
            case 7:
                load_queue(reservation_queue, "reservation_list.txt");
                if(isEmpty(pre_reservation_queue)) load_queue(pre_reservation_queue, "pre_reservation_list.txt");
                update_time(pre_reservation_queue, app_present_time);
                update_time(reservation_queue,app_present_time);
                printf("\nLists successfully loaded! Appointments scheduled before the current time and with no available slots were not included.\n");
                break;
            case 8:
                save(reservation_queue,"reservation_list.txt");
                save(pre_reservation_queue,"pre_reservation_list.txt");
                printf("\nLists saved successfully!!\n");
                break;
            case 9: 
                x = 0;
                break;
            default: printf("\nOption does not exist. Please re-enter the option you want.\n\n");
        }
    }

    printf("\n      ____     ----------------------------------------------------       ____     \n");
    printf("   __/  | \\__  | Thank you for using ManuWash!!! Come back soon!! |    __/ |  \\__   \n");
    printf("  '--0----0--' ----------------------------------------------------   '--0----0--' \n\n");   
}

int leap_year(int x){
        if(x % 400 == 0) return 1;
        else{
                if((x % 4 == 0) && (x % 100 != 0)) return 1;
                else return 0;
        }
}

int check_day(int day, int month, int year){ 
        /* year == 1 (leap_year) <<>> year == 0 (not leap_year) */
        switch(month){
                case 1:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                case 2:
                        if(day >= 1 && day <= 29 && year == 1) return 1;
                        if(day >= 1 && day <= 28 && year == 0) return 1;
                        break;
                case 3:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                case 4:
                        if(day >= 1 && day <= 30) return 1;
                        break;
                case 5:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                case 6:
                        if(day >= 1 && day <= 30) return 1;
                        break;
                case 7:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                case 8:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                case 9:
                        if(day >= 1 && day <= 30) return 1;
                        break;
                case 10:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                case 11:
                        if(day >= 1 && day <= 30) return 1;
                        break;
                case 12:
                        if(day >= 1 && day <= 31) return 1;
                        break;
                default:
                break;
        }
        return 0;
}

System *create_queue(){
        System *aux = (System *) malloc(sizeof(System));
        if(aux != NULL){
                aux->next = NULL;
                return aux;
        }
        else {
                perror("\n*** Memory allocation error ***\n");
                return NULL;
        }             
}

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

void print_queue(System *queue){
        if(!isEmpty(queue)){
                printf("%8s%15s%12s%16s\n", "Date", "Time", "Service", "User");
                for(System *aux = queue->next; aux != NULL; aux = aux->next){
                        if(aux->user.func == 1){ 
                                printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s%10s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Lavagem",aux->user.name);
                        }
                        if(aux->user.func == 2){ 
                                printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s %10s\n", aux->user.day , aux->user.month , aux->user.year , aux->user.hour , aux->user.min , "Manutenção",aux->user.name);
                     }
                }
        }
        else printf("*** There are no entries in this list yet ***\n");
}

int isEmpty(System *queue){
        if (queue->next == NULL) return 1;
        else return 0;
}

void search(System *queue, Person key, System **ant, System **app_present_time){
        *ant = queue; 
        *app_present_time = queue->next;
        while ((*app_present_time) != NULL && 
                ((*app_present_time)->user.year < key.year ||
                ((*app_present_time)->user.year == key.year && (*app_present_time)->user.month < key.month) ||
                ((*app_present_time)->user.year == key.year && (*app_present_time)->user.month == key.month && (*app_present_time)->user.day < key.day) ||
                ((*app_present_time)->user.year == key.year && (*app_present_time)->user.month == key.month && (*app_present_time)->user.day == key.day && (*app_present_time)->user.hour < key.hour) ||
                ((*app_present_time)->user.year == key.year && (*app_present_time)->user.month == key.month && (*app_present_time)->user.day == key.day && (*app_present_time)->user.hour == key.hour && (*app_present_time)->user.min < key.min) ||
                ((*app_present_time)->user.year == key.year && (*app_present_time)->user.month == key.month && (*app_present_time)->user.day == key.day && (*app_present_time)->user.hour == key.hour && (*app_present_time)->user.min == key.min && (*app_present_time)->user.work == 2))) {
        *ant = *app_present_time;
        *app_present_time = (*app_present_time)->next;
    }
        if ((*app_present_time) != NULL && ((*app_present_time)->user.day != key.day || (*app_present_time)->user.month != key.month || (*app_present_time)->user.year != key.year || (*app_present_time)->user.hour != key.hour || (*app_present_time)->user.min != key.min)) {
                *app_present_time = NULL; /* elemento não encontrado */
    }
}

int check_time_spot(System *queue, Person p1){
        if(isEmpty(queue)) return 1;
        else{
                System *aux = queue->next;
                while(aux != NULL){
                        /* Mesma data e horario */
                        if(aux->user.year == p1.year && aux->user.month == p1.month && aux->user.day == p1.day && aux->user.hour == p1.hour && aux->user.min == p1.min && p1.work == 1) return 0;
                        /* Mesma data */
                        if(aux->user.year == p1.year && aux->user.month == p1.month && aux->user.day == p1.day && p1.work == 1){
                                /* Caso a hour seja x:00 */
                                if(p1.min == 0 && aux->user.hour == p1.hour-1 && aux->user.min == 30){
                                        if(aux->user.func == 2) return 0;
                                        /* Caso a anterior seja lavagem, a proxima esteja reservada e a marcação seja uma manutenção */
                                        else if(p1.func == 2 && aux->next != NULL && aux->next->user.hour == p1.hour && aux->next->user.min == 30) return 0;
                                }
                                /* Caso a hour seja x:30 */
                                if(p1.min == 30 && aux->user.hour == p1.hour && aux->user.min == 0){
                                        if(aux->user.func == 2) return 0;
                                        /* Caso a anterior seja lavagem, a proxima esteja reservada e a marcação seja uma manutenção  */
                                        else if(p1.func == 2 && aux->next != NULL && aux->next->user.hour == p1.hour+1 && aux->next->user.min == 0) return 0;
                                }
                                /* Caso seja manutenção o anterior esteja livre e o proximo esteja reservado*/
                                if((p1.min == 30 && p1.func == 2 && aux->user.hour == p1.hour+1 && aux->user.min == 0) || (p1.min == 0 && p1.func == 2 && aux->user.hour == p1.hour && aux->user.min == 30)) return 0;
                        }
                        aux = aux->next;
                }
        }
        return 1;
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

void search_booking_by_username(System *queue, Person key, System **ant, System **app_present_time, int service){
        *ant = queue; 
        *app_present_time = queue->next;
        if(service == 1) while ((*app_present_time) != NULL && (strcmp((*app_present_time)->user.name, key.name) != 0 
                              || (*app_present_time)->user.day != key.day || (*app_present_time)->user.month != key.month 
                              || (*app_present_time)->user.year != key.year || (*app_present_time)->user.hour != key.hour 
                              || (*app_present_time)->user.min != key.min)){
                *ant = *app_present_time;
                *app_present_time = (*app_present_time)->next;
                }
        if(service == 2) while ((*app_present_time) != NULL && ((*app_present_time)->user.day != key.day 
                                || (*app_present_time)->user.month != key.month 
                                || (*app_present_time)->user.year != key.year || (*app_present_time)->user.hour != key.hour 
                                || (*app_present_time)->user.min != key.min)){
                *ant = *app_present_time;
                *app_present_time = (*app_present_time)->next;
                }

    if (*app_present_time == NULL) {
        *ant = NULL; // elemento não encontrado
    }
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
                        temp->next = aux->next;  // app_present_timeiza o ponteiro do elemento anterior
                        free(aux);  // Libera a memória do elemento
                        aux = temp->next;  // app_present_timeiza o ponteiro auxiliar
                } else {
                aux->user.work = 2;
                temp = aux;  // app_present_timeiza o ponteiro temporário
                aux = aux->next;  // app_present_timeiza o ponteiro auxiliar
                }
        }
}

int checkint() {
    int x;
    while (scanf("%d", &x) != 1 || getchar() != '\n') {
        printf("Option does not exist. Please re-enter the option you want.\n>>> ");
        while (getchar() != '\n');
    }
    return x;
}

void update_time(System *list, Time app_present_time) {
    System *aux = list->next;
    System *temp = list;

    while (aux != NULL) {
        if (aux->user.year < app_present_time.year || 
            (aux->user.year == app_present_time.year && aux->user.month < app_present_time.month) || 
            (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day < app_present_time.day)) {
            
            temp->next = aux->next;     /* app_present_timeiza o ponteiro do elemento anterior */
            free(aux);                  /* Libera a memória do elemento   */
            aux = temp->next;           /* app_present_timeiza o ponteiro auxiliar   */
        } else {
            temp = aux;                 /* app_present_timeiza o ponteiro temporário */
            aux = aux->next;            /* app_present_timeiza o ponteiro auxiliar   */
        }
    }
}

void update_queue_by_real_time(System *list, Person app_present_time){
        System *aux = list->next;
        System *temp = list;
        while (aux != NULL) {
                if (aux->user.year < app_present_time.year || 
                (aux->user.year == app_present_time.year && aux->user.month < app_present_time.month) || 
                (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day < app_present_time.day) || 
                (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day == app_present_time.day && aux->user.hour < app_present_time.hour) ||
                (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day == app_present_time.day && aux->user.hour < app_present_time.hour) || 
                (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day == app_present_time.day && aux->user.hour == app_present_time.hour && aux->user.min < app_present_time.min) || 
                (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day == app_present_time.day && aux->user.hour == app_present_time.hour && aux->user.min == app_present_time.min)){
                temp->next = aux->next;  /* app_present_timeiza o ponteiro do elemento anterior */
                free(aux);               /* Libera a memória do elemento */
                aux = temp->next;        /* app_present_timeiza o ponteiro auxiliar */
                } else {
                temp = aux;              /* app_present_timeiza o ponteiro temporário */
                aux = aux->next;         /* app_present_timeiza o ponteiro auxiliar */
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

void load_queue(System *list, const char *file){

        char file_path[128];
        snprintf(file_path, sizeof(file_path), "data/%s", file);
        FILE *file_manager = fopen(file_path, "r");
        
        if (file_manager == NULL) {
                if(strcmp(file, "reservation_list.txt") == 0) printf("** No reservations on database. **\n");
                else if(strcmp(file, "pre_reservation_list.txt") == 0) printf("** No pre-reservations on database. **\n");
                else printf("** Error opening save files. **\n");
                return;
        }

        Person insert;
        /* Percorre as listas e lê os dados do file_manager */
        while (fscanf(file_manager, "%d %d %d %d %d %d %d", &insert.work, &insert.func, &insert.year, &insert.month, &insert.day, &insert.hour, &insert.min) == 7) {
                fgets(insert.name, MAX, file_manager);
                insert.name[strcspn(insert.name, "\n")] = '\0';
                if(strcmp(file,"reservation_list.txt") == 0 && check_time_spot(list,insert)) create_service(list, NULL, insert,0);
                else if (strcmp(file,"pre_reservation_list.txt") == 0) create_service(list, NULL, insert,0);
        }
        fclose(file_manager);
}

void save(System *list, const char *file){
        /* Abre o file_manager para escrita */
        mkdir("data", 0777);  // garante que a pasta exista
        char file_path[128];
        snprintf(file_path, sizeof(file_path), "data/%s", file);

        FILE *file_manager = fopen(file_path, "w");

        if (file_manager == NULL) {
                printf("Not possible to open %s\n", file_path);
                return;
        }
        
        /* Percorre a list e escreve dados no file_manager */
        System *app_present_time = list->next;
        while (app_present_time != NULL) {
                fprintf(file_manager, "%d %d %d %d %d %d %d", app_present_time->user.work, app_present_time->user.func, app_present_time->user.year, app_present_time->user.month, app_present_time->user.day, app_present_time->user.hour, app_present_time->user.min);
                fprintf(file_manager, "%s\n", app_present_time->user.name);
                app_present_time = app_present_time->next;
        }
        fclose(file_manager);
}

void destroi(System *queue){
        System *aux;
        while (!isEmpty (queue)) {
                aux = queue;
                queue = queue->next;
                free (aux);
        }
        free(queue);
}