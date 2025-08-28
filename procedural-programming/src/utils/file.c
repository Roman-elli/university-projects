#include "../../include/projeto.h"

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