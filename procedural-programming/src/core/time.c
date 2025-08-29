#include "../../include/project.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

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

void update_time(System *list, Time app_present_time) {
    System *aux = list->next;
    System *temp = list;

    while (aux != NULL) {
        if (aux->user.year < app_present_time.year || 
            (aux->user.year == app_present_time.year && aux->user.month < app_present_time.month) || 
            (aux->user.year == app_present_time.year && aux->user.month == app_present_time.month && aux->user.day < app_present_time.day)) {
            
            temp->next = aux->next;
            free(aux);
            aux = temp->next;
        } else {
            temp = aux;
            aux = aux->next;
        }
    }
}