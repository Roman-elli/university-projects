#include "../../include/project.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

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
        while (fscanf(file_manager, "%d %d %d %d %d %d %d", &insert.work, &insert.func, &insert.year, &insert.month, &insert.day, &insert.hour, &insert.min) == 7) {
                fgets(insert.name, MAX, file_manager);
                insert.name[strcspn(insert.name, "\n")] = '\0';
                if(strcmp(file,"reservation_list.txt") == 0 && check_time_spot(list,insert)) create_service(list, NULL, insert,0);
                else if (strcmp(file,"pre_reservation_list.txt") == 0) create_service(list, NULL, insert,0);
        }
        fclose(file_manager);
}

void save(System *list, const char *file){
        mkdir("data", 0777);
        char file_path[128];
        snprintf(file_path, sizeof(file_path), "data/%s", file);

        FILE *file_manager = fopen(file_path, "w");

        if (file_manager == NULL) {
                printf("Not possible to open %s\n", file_path);
                return;
        }
        
        System *current_node = list->next;
        while (current_node != NULL) {
                fprintf(file_manager, "%d %d %d %d %d %d %d", current_node->user.work, current_node->user.func, current_node->user.year, current_node->user.month, current_node->user.day, current_node->user.hour, current_node->user.min);
                fprintf(file_manager, "%s\n", current_node->user.name);
                current_node = current_node->next;
        }
        fclose(file_manager);
}