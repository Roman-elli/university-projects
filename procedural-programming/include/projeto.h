#ifndef PROJETO_H
#define PROJETO_H
#define MAX 50

/*
 .work == 1 (reserva) <<>> .work == 2 (pré-reserva)
 .func == 1 (Lavagem) <<>> .work == 2 (Manutenção) 
 */

typedef struct {
    char name[MAX];
    int hour,min,day,month,year, work, func;  
}Person;

typedef struct{
    int day,month,year;
}Time;

/* Estrutura que armazena cada estrutura de user (Person) e o ponteiro que aponta para o próximo da list */
typedef struct noFila{
    Person user;
    struct noFila *next;    
}System;   

void print_menu(System *reservation_queue, System *pre_reservation_queue);                                        /* impressão do print_menu */
int leap_year(int x);                                /* Verificação de year leap_year */
int check_day(int day, int month, int year);         /* Verifica se o day inserido é válido */
System *create_queue();                                    /* Inicializa as listas */
int isEmpty(System *queue);                           /* Verifica se a list esta isEmpty */
void destroi(System *queue);                        /* Liberta toda a memória alocada em uma list específica */
int check_time_spot(System *list, Person p1);        /* Verifica se um horário específico está disponível para reserva */
void search(System *queue, Person key, System **ant, System **app_present_time);                      /* search um elemento específico da list levando em conta a data e horário */
void procuranome(System *queue, Person key, System **ant, System **app_present_time, int service);      /* search um elemento específico da list levando em conta o name de uma Person */
void create_service(System *list,System *pre_reservation_list, Person p1, int x);      /* create_service um elemento na list caso seja possível */
void print_queue(System *queue);                                        /* print_queue a list em ordem temporal */
void print_user_reservations(System *queue, System *pre_reservation_queue, char *name);        /* print_queue as reservas e pré-reservas de uma Person específica */
void print_specific_bookings(System *queue, Person insert);                     /* print_queue a list de reservas e pré-reservas de um determinado day */
void book_service(System *reservation_queue, System *pre_reservation_queue, Time app_present_time);          /* book_service todos os dados necessários para que se faça uma reserva ou uma pré-reserva */
void check_specific_user(System *list, char *name);                            /* print_queue de as reservas e pré-reservas de um cliente específico em ordem de data de forma descrescente*/
int checkint();                                                     /* Checa o que o usuário escreve e verifica se há algum caracter inválido */
void cancel_service(System *reservation_list, System *pre_reservation_list, Time actual);         /* cancel_service um elemento da list de acordo com as informações dadas */
void load_queue(System *reservation_list, const char *file);                /* Coleta todas as informações salvas em um file específico e as create_service em sua respetiva list */
void save(System *list, const char *file);                    /* Salva todos os dados das listas em seus respetivos ficheiros */
void update_time(System *list, Time app_present_time);                     /* app_present_timeiza as listas para as novas definições de tempo app_present_time */
void update_queue(System *list, Person app_present_time);                    /* Após a execução de uma reserva, verifica todas as pré-reservas anteriores a ordem executada e as cancel_service */
void update_queues(System *pre_reservation_list, System *reservation_list);                /* app_present_timeiza a queue de pré-reservas após a remoção de um usuário das reservas */
void execute_service(System *reservation_list, System *pre_reservation_list);                     /* execute_service a ordem mais antiga das reservas */

#endif