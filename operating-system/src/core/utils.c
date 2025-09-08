#include "../../include/functions.h"

void write_log(char* message){
	time_t actual_time;
    struct tm *time_info;

    time(&actual_time);
    time_info = localtime(&actual_time);

    #ifdef DEBUG
    printf("%s\n", message);
    #endif
    sem_wait(sem_log);
    fprintf(file, "%02d:%02d:%02d %s\n", time_info->tm_hour, time_info->tm_min, time_info->tm_sec, message);
    fflush(file);
    sem_post(sem_log);
}

void error(char *s) {
    perror(s);
    exit(1);
}

int number_int_validation(const char *argv) {
    if (atoi(argv) == 0) {
				write_log("ERROR IN INT CONVERTION");
        return -1;
    }
    return atoi(argv);
}

void free_queue(Queue_organizer **head_other, Queue_organizer **head_video) {
	char message_free[MESSAGE_SIZE];
    Queue_organizer *current_other = *head_other;
    Queue_organizer *next_other;

    while (current_other != NULL) {
        next_other = current_other->next;
        snprintf(message_free, sizeof(message_free), "5G_AUTH_PLATFORM SIMULATOR: %s AUTHORIZATION REQUEST (ID = %d)  PROCESSING IMCOMPLETED", current_other->type, current_other->user_id);
        write_log(message_free);
        free(current_other);
        current_other = next_other;
    }
    *head_other = NULL;

    Queue_organizer *current_video = *head_video;
    Queue_organizer *next_video;

    while (current_video != NULL) {
        next_video = current_video->next;
		snprintf(message_free, sizeof(message_free), "5G_AUTH_PLATFORM SIMULATOR: %s AUTHORIZATION REQUEST (ID = %d)  PROCESSING IMCOMPLETED", current_video->type, current_video->user_id);
		write_log(message_free);
        free(current_video);
        current_video = next_video;
    }
    *head_video = NULL;
}
