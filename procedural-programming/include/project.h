#ifndef PROJECT_H
#define PROJECT_H
#define MAX 50

typedef struct {
    char name[MAX];
    int hour,min,day,month,year, work, func;  
}Person;

typedef struct{
    int day,month,year;
}Time;

typedef struct queue_node{
    Person user;
    struct queue_node *next;    
}System;   

void print_menu(System *reservation_queue, System *pre_reservation_queue);
int leap_year(int x);
int check_day(int day, int month, int year);
System *create_queue();
int isEmpty(System *queue);
void destroi(System *queue);
int check_time_spot(System *list, Person p1);
void search(System *queue, Person key, System **ant, System **current_node);
void search_booking_by_username(System *queue, Person key, System **ant, System **current_node, int service);
void create_service(System *list,System *pre_reservation_list, Person p1, int x);
void print_queue(System *queue);
void print_user_reservations(System *queue, System *pre_reservation_queue, char *name);
void print_specific_bookings(System *queue, Person insert);
void book_service(System *reservation_queue, System *pre_reservation_queue, Time app_present_time);
void check_specific_user(System *list, char *name);
int checkint();
void cancel_service(System *reservation_list, System *pre_reservation_list, Time actual);
void load_queue(System *reservation_list, const char *file);
void save(System *list, const char *file);
void update_time(System *list, Time app_present_time);
void update_queue_by_real_time(System *list, Person person);
void update_queues(System *pre_reservation_list, System *reservation_list);
void execute_service(System *reservation_list, System *pre_reservation_list);

#endif