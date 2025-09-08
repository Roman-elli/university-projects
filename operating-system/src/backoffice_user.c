#include "../include/functions.h"

#define BACK_MESSAGE_SIZE 50
#define DEBUG
#define PIPE_NAME "BACK_PIPE"
#define QUEUE_KEY 12345

int main(void) {
    pthread_t mq_pthread;

    signal(SIGINT, sigint_backoffice_handler);
    char message[BACK_MESSAGE_SIZE];
    char back_id[BACK_MESSAGE_SIZE];
    char back_command[BACK_MESSAGE_SIZE];

    pthread_create(&mq_pthread, NULL, mq_backoffice_analyser, NULL);

    if ((fd_backoffice = open(PIPE_NAME, O_WRONLY)) < 0) {
        perror("Cannot open pipe for writing.");
        exit(EXIT_FAILURE);
    }

    while (1) {

        if (fgets(message, BACK_MESSAGE_SIZE, stdin) == NULL) {
            perror("Error reading input.");
            exit(EXIT_FAILURE);
        }

        if (sscanf(message, "%29[^#]#%29s\n", back_id, back_command) != 2) {
            #ifdef DEBUG
            printf("Error: invalid input format!\n");
            #endif
            continue;
        }

        if (strcmp(back_id, "1") == 0) {
            if (strcmp(back_command, "data_stats") == 0 || strcmp(back_command, "reset") == 0) {
                if (write(fd_backoffice, message, strlen(message)) < 0) {
                    perror("Failed to write to pipe.");
                    exit(EXIT_FAILURE);
                }

                #ifdef DEBUG
                printf("Executing %s operation...\n", back_command);
                #endif
            } else {
                #ifdef DEBUG
                printf("Error: '%s' is not a valid command! Valid commands are 'data_stats' and 'reset'\n", back_command);
                #endif
                exit(EXIT_FAILURE);
            }
        } else{
            #ifdef DEBUG
            printf("Error: '%s' is not a valid BackOffice User ID! Valid BackOffice User ID is '1'\n", back_id);
            #endif
            exit(EXIT_FAILURE);
        }
    }
    pthread_join(mq_pthread, NULL);
    return 0;
}




