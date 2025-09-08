#include "../include/functions.h"

#define DEBUG
#define PIPE_NAME "USER_PIPE"
#define QUEUE_KEY 12345

int main(int argc, char *argv[]) {
    if(argc != 2){
        printf("Uso: %s <file de configuração>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    signal(SIGINT, sigint_mobile_handler);

    read_mobile_config_file(argv[1]);

    video_duration *= 1000;
    music_duration *= 1000;
    social_duration *= 1000;
    id = getpid();

    sem_mobile = sem_open("MOBILE", O_CREAT, 0666, 1);
    if (sem_mobile == SEM_FAILED) {
       perror("Error opening semaphor");
       return 1;
   }

#ifdef DEBUG
    printf("Plafond: %d, Requests: %d, Video duration: %dus, Music duration: %dus, Social duration: %dus, Data: %d, ID: %d\n",
           plafond, user_request, video_duration, music_duration, social_duration, mobile_data, id);
#endif

    if ((fd_mobile = open(PIPE_NAME, O_WRONLY)) < 0) {
        perror("Error opening mobile user pipe.");
        exit(EXIT_FAILURE);
    }


    snprintf(message, sizeof(message), "%d#INSERT#%d\n", id, plafond);
    sem_wait(sem_mobile);
    if (write(fd_mobile, message, strlen(message)) < 0) {
        perror("Failed to write on mobile pipe.");
        exit(EXIT_FAILURE);
    }
    sem_post(sem_mobile);

    pthread_create(&social_pthread, NULL, social_handler, NULL);
    pthread_create(&music_pthread, NULL, music_handler, NULL);
    pthread_create(&video_pthread, NULL, video_handler, NULL);
    mq_mobile_analyser();
    pthread_join(social_pthread, NULL);
    pthread_join(music_pthread, NULL);
    pthread_join(video_pthread, NULL);
    close(fd_mobile);
    pthread_mutex_unlock(&mutex);
    pthread_mutex_destroy(&mutex);
    return 0;
}

