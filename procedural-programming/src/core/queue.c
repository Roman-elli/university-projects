#include "../../include/projeto.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

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

void destroi(System *queue){
        System *aux;
        while (!isEmpty (queue)) {
                aux = queue;
                queue = queue->next;
                free (aux);
        }
        free(queue);
}