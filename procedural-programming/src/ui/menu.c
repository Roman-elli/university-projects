#include <stdio.h>
#include <string.h>
#include "../../include/projeto.h"

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


