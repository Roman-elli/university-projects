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
#include "../include/functions.h"

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
int pedidos;
int intervalo_video;
int intervalo_music;
int intervalo_social;
int dados;
int message_length;

int main(int argc, char *argv[]) {
    if(argc != 2){
        printf("Uso: %s <arquivo de configuração>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    signal(SIGINT, sigint_handler);

    read_mobile_config_file(argv[1]);

    intervalo_video *= 1000;
    intervalo_music *= 1000;
    intervalo_social *= 1000;
    id = getpid();

    sem_mobile = sem_open("MOBILE", O_CREAT, 0666, 1);
    if (sem_mobile == SEM_FAILED) {
       perror("Erro ao abrir o semáforo");  // Imprime o erro baseado no valor de errno
       return 1;  // Retorna 1 indicando falha
   }

    

#ifdef DEBUG
    printf("Plafond: %d, Pedidos: %d, Intervalo_video: %dus, Intervalo_music: %dus, Intervalo_social: %dus, Dados: %d, ID: %d\n",
           plafond, pedidos, intervalo_video, intervalo_music, intervalo_social, dados, id);
#endif

    if ((fd = open(PIPE_NAME, O_WRONLY)) < 0) {
        perror("Não foi possível abrir o pipe para escrita.");
        exit(EXIT_FAILURE);
    }


    snprintf(message, sizeof(message), "%d#INSERT#%d\n", id, plafond);
    sem_wait(sem_mobile);
    if (write(fd, message, strlen(message)) < 0) {
        perror("Falha ao escrever no pipe.");
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
    printf("\nNúmero de pedidos esgotado...\n");
    #endif
    close(fd);
    pthread_mutex_unlock(&mutex);
    pthread_mutex_destroy(&mutex);
    exit(EXIT_SUCCESS);
}

void *social_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (pedidos > 0) {
            pedidos--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (pedidos == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_social, 0, sizeof(message_social));

        snprintf(message_social, sizeof(message_social), "%d#SOCIAL#%d\n", id, dados);

        sem_wait(sem_mobile);

        if (write(fd, message_social, strlen(message_social)) < 0) {
            perror("Falha ao escrever no pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(intervalo_social);
    }
    pthread_exit(NULL);
}

void read_mobile_config_file(char* filename){
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        write_log("Erro ao ler ficheiro");
        exit(1);
    }

    if (fscanf(file, "%d %d %d %d %d %d", &plafond, &pedidos, &intervalo_video, &intervalo_music, &intervalo_social, &dados) != 6) {
        write_log("Erro ao ler valores do arquivo de configuração");
        fclose(file);
        exit(1);
    }
    fclose(file);
}

void *music_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (pedidos > 0) {
            pedidos--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (pedidos == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
       pthread_mutex_unlock(&mutex);
        memset(message_music, 0, sizeof(message_music));
        snprintf(message_music, sizeof(message_music), "%d#MUSIC#%d\n", id, dados);

        sem_wait(sem_mobile);
        if (write(fd, message_music, strlen(message_music)) < 0) {
            perror("Falha ao escrever no pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(intervalo_music);
    }
    pthread_exit(NULL);
}

void *video_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (pedidos > 0) {
            pedidos--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (pedidos == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_video, 0, sizeof(message_video));
        snprintf(message_video, sizeof(message_video), "%d#VIDEO#%d\n", id, dados);

        sem_wait(sem_mobile);
        if (write(fd, message_video, strlen(message_video)) < 0) {
            perror("Falha ao escrever no pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(intervalo_video);
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
  while(pedidos > 0){
    // Receber uma mensagem
    if (msgrcv(mq_id, &msg, sizeof(msg.answer), id, 0) == -1) {
        perror("msgrcv failed");
        exit(EXIT_FAILURE);
    }

    if(msg.answer == 80){
        printf("\n[SYSTEM WARNING] 80%% do plafond utilizado\n");
    }else if(msg.answer == 90){
        printf("\n[SYSTEM WARNING] 90%% do plafond utilizado\n");
    }else{
      printf("\n[SYSTEM WARNING] 100%% do plafond utilizado\n");
      close(fd);
      pthread_mutex_unlock(&mutex);
      exit(EXIT_SUCCESS);
      }
    }
}
