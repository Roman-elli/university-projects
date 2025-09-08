#include "../include/functions.h"

#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/msg.h>
#include <semaphore.h>

#define DEBUG
#define PIPE_NAME "USER_PIPE"
#define QUEUE_KEY 12345

void mq_analyser();
void sigint_handler(int signum);
void *music_handler(void *arg);
void read_mobile_config_file(char* filename);
void *social_handler(void *arg);
void *video_handler(void *arg);
int fd;

pthread_t social_pthread, music_pthread, video_pthread;
char message_video[MESSAGE_SIZE];
char message_social[MESSAGE_SIZE];
char message_music[MESSAGE_SIZE];
int fd;
int plafond;
int user_request;
int video_duration;
int music_duration;
int social_duration;
int mobile_data;
int message_length;

int main(int argc, char *argv[]) {
    if(argc != 2){
        printf("Uso: %s <file de configuração>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    signal(SIGINT, sigint_handler);

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

    if ((fd = open(PIPE_NAME, O_WRONLY)) < 0) {
        perror("Error opening mobile user pipe.");
        exit(EXIT_FAILURE);
    }


    snprintf(message, sizeof(message), "%d#INSERT#%d\n", id, plafond);
    sem_wait(sem_mobile);
    if (write(fd, message, strlen(message)) < 0) {
        perror("Failed to write on mobile pipe.");
        exit(EXIT_FAILURE);
    }
    sem_post(sem_mobile);

    pthread_create(&social_pthread, NULL, social_handler, NULL);
    pthread_create(&music_pthread, NULL, music_handler, NULL);
    pthread_create(&video_pthread, NULL, video_handler, NULL);
    mq_analyser();
    pthread_join(social_pthread, NULL);
    pthread_join(music_pthread, NULL);
    pthread_join(video_pthread, NULL);
    close(fd);
    pthread_mutex_unlock(&mutex);
    pthread_mutex_destroy(&mutex);
    return 0;
}

void sigint_handler(int signum) {
    #ifdef DEBUG
    printf("\nNumber of user_requests exhausted...\n");
    #endif
    close(fd);
    pthread_mutex_unlock(&mutex);
    pthread_mutex_destroy(&mutex);
    exit(EXIT_SUCCESS);
}

void *social_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (user_request > 0) {
            user_request--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (user_request == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_social, 0, sizeof(message_social));

        snprintf(message_social, sizeof(message_social), "%d#SOCIAL#%d\n", id, mobile_data);

        sem_wait(sem_mobile);

        if (write(fd, message_social, strlen(message_social)) < 0) {
            perror("Failed to write on mobile pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(social_duration);
    }
    pthread_exit(NULL);
}

void read_mobile_config_file(char* filename){
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        write_log("Error reading mobile user config file.");
        exit(1);
    }

    if (fscanf(file, "%d %d %d %d %d %d", &plafond, &user_request, &video_duration, &music_duration, &social_duration, &mobile_data) != 6) {
        write_log("Error reading values from the mobile configuration file.");
        fclose(file);
        exit(1);
    }
    fclose(file);
}

void *music_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (user_request > 0) {
            user_request--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (user_request == 0) {
                kill(getpid(), SIGINT);
                break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_music, 0, sizeof(message_music));
        snprintf(message_music, sizeof(message_music), "%d#MUSIC#%d\n", id, mobile_data);

        sem_wait(sem_mobile);
        if (write(fd, message_music, strlen(message_music)) < 0) {
            perror("Failed to write on mobile pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(music_duration);
    }
    pthread_exit(NULL);
}

void *video_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (user_request > 0) {
            user_request--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (user_request == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_video, 0, sizeof(message_video));
        snprintf(message_video, sizeof(message_video), "%d#VIDEO#%d\n", id, mobile_data);

        sem_wait(sem_mobile);
        if (write(fd, message_video, strlen(message_video)) < 0) {
            perror("Failed to write on mobile pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(video_duration);
    }
    pthread_exit(NULL);
}

void mq_analyser(){
  // Obter o identificador da fila de mensagens
  mq_user msg;
  int mq_id = msgget(QUEUE_KEY, 0666);
  if (mq_id == -1) {
      perror("msgget failed");
      exit(EXIT_FAILURE);
  }
  while(user_request > 0){
    // Receber uma mensagem
    if (msgrcv(mq_id, &msg, sizeof(msg.answer), id, 0) == -1) {
        perror("msgrcv failed");
        exit(EXIT_FAILURE);
    }

    if(msg.answer == 80){
        printf("\n[SYSTEM WARNING] 80%% of the ceiling used\n");
    }else if(msg.answer == 90){
        printf("\n[SYSTEM WARNING] 90%% of the ceiling used\n");
    }else{
      printf("\n[SYSTEM WARNING] 100%% of the ceiling used\n");
      close(fd);
      pthread_mutex_unlock(&mutex);
      exit(EXIT_SUCCESS);
      }
    }
}
