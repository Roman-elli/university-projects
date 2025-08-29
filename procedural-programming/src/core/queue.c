#include "../../include/project.h"

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

void search(System *queue, Person key, System **ant, System **current_node){
        *ant = queue; 
        *current_node = queue->next;
        while ((*current_node) != NULL && 
                ((*current_node)->user.year < key.year ||
                ((*current_node)->user.year == key.year && (*current_node)->user.month < key.month) ||
                ((*current_node)->user.year == key.year && (*current_node)->user.month == key.month && (*current_node)->user.day < key.day) ||
                ((*current_node)->user.year == key.year && (*current_node)->user.month == key.month && (*current_node)->user.day == key.day && (*current_node)->user.hour < key.hour) ||
                ((*current_node)->user.year == key.year && (*current_node)->user.month == key.month && (*current_node)->user.day == key.day && (*current_node)->user.hour == key.hour && (*current_node)->user.min < key.min) ||
                ((*current_node)->user.year == key.year && (*current_node)->user.month == key.month && (*current_node)->user.day == key.day && (*current_node)->user.hour == key.hour && (*current_node)->user.min == key.min && (*current_node)->user.work == 2))) {
        *ant = *current_node;
        *current_node = (*current_node)->next;
    }
        if ((*current_node) != NULL && ((*current_node)->user.day != key.day || (*current_node)->user.month != key.month || (*current_node)->user.year != key.year || (*current_node)->user.hour != key.hour || (*current_node)->user.min != key.min)) {
                *current_node = NULL;
    }
}

int check_time_spot(System *queue, Person p1){
        if(isEmpty(queue)) return 1;
        else{
                System *aux = queue->next;
                while(aux != NULL){
                        if(aux->user.year == p1.year && aux->user.month == p1.month && aux->user.day == p1.day && aux->user.hour == p1.hour && aux->user.min == p1.min && p1.work == 1) return 0;
                        if(aux->user.year == p1.year && aux->user.month == p1.month && aux->user.day == p1.day && p1.work == 1){
                                if(p1.min == 0 && aux->user.hour == p1.hour-1 && aux->user.min == 30){
                                        if(aux->user.func == 2) return 0;
                                        else if(p1.func == 2 && aux->next != NULL && aux->next->user.hour == p1.hour && aux->next->user.min == 30) return 0;
                                }
                                if(p1.min == 30 && aux->user.hour == p1.hour && aux->user.min == 0){
                                        if(aux->user.func == 2) return 0;
                                        else if(p1.func == 2 && aux->next != NULL && aux->next->user.hour == p1.hour+1 && aux->next->user.min == 0) return 0;
                                }
                                if((p1.min == 30 && p1.func == 2 && aux->user.hour == p1.hour+1 && aux->user.min == 0) || (p1.min == 0 && p1.func == 2 && aux->user.hour == p1.hour && aux->user.min == 30)) return 0;
                        }
                        aux = aux->next;
                }
        }
        return 1;
}

void search_booking_by_username(System *queue, Person key, System **ant, System **current_node, int service){
        *ant = queue; 
        *current_node = queue->next;
        if(service == 1) while ((*current_node) != NULL && (strcmp((*current_node)->user.name, key.name) != 0 
                              || (*current_node)->user.day != key.day || (*current_node)->user.month != key.month 
                              || (*current_node)->user.year != key.year || (*current_node)->user.hour != key.hour 
                              || (*current_node)->user.min != key.min)){
                *ant = *current_node;
                *current_node = (*current_node)->next;
                }
        if(service == 2) while ((*current_node) != NULL && ((*current_node)->user.day != key.day 
                                || (*current_node)->user.month != key.month 
                                || (*current_node)->user.year != key.year || (*current_node)->user.hour != key.hour 
                                || (*current_node)->user.min != key.min)){
                *ant = *current_node;
                *current_node = (*current_node)->next;
                }

    if (*current_node == NULL) {
        *ant = NULL;
    }
}

void update_queue_by_real_time(System *list, Person person){
        System *aux = list->next;
        System *temp = list;
        while (aux != NULL) {
                if (aux->user.year < person.year || 
                (aux->user.year == person.year && aux->user.month < person.month) || 
                (aux->user.year == person.year && aux->user.month == person.month && aux->user.day < person.day) || 
                (aux->user.year == person.year && aux->user.month == person.month && aux->user.day == person.day && aux->user.hour < person.hour) ||
                (aux->user.year == person.year && aux->user.month == person.month && aux->user.day == person.day && aux->user.hour < person.hour) || 
                (aux->user.year == person.year && aux->user.month == person.month && aux->user.day == person.day && aux->user.hour == person.hour && aux->user.min < person.min) || 
                (aux->user.year == person.year && aux->user.month == person.month && aux->user.day == person.day && aux->user.hour == person.hour && aux->user.min == person.min)){
                temp->next = aux->next;
                free(aux);
                aux = temp->next;
                } else {
                        temp = aux;
                        aux = aux->next;
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