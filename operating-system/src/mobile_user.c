//Beatriz Alexandra Azeitona Mourato nº2022224891
//Thales Barbuto Romanelli Lopes nº2022169928

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

#define MESSAGE_SIZE 512
#define DEBUG
#define PIPE_NAME "USER_PIPE"
#define QUEUE_KEY 12345


typedef struct
{
  long mtype;
  int answer;
} mq_user;

void mq_analyser();
void sigint_handler(int signum);
int valida_numero(const char *argv);
void *music_handler(void *arg);
void *social_handler(void *arg);
void *video_handler(void *arg);
int fd;
sem_t *sem_mobile;

pthread_t social_pthread, music_pthread, video_pthread;
char message[MESSAGE_SIZE];
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
int id;
int message_length;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

int main(int argc, char *argv[]) {
    if (argc != 7) {
        printf("Uso: %s <plafond inicial> <número de pedidos de autorização> <intervalo VIDEO> <intervalo MUSIC> <intervalo SOCIAL> <dados a reservar>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    signal(SIGINT, sigint_handler);
    printf("ANTES\n");

    sem_mobile = sem_open("MOBILE", O_CREAT, 0666, 1);
    if (sem_mobile == SEM_FAILED) {
       perror("Erro ao abrir o semáforo");  // Imprime o erro baseado no valor de errno
       return 1;  // Retorna 1 indicando falha
   }

    plafond = valida_numero(argv[1]);
    pedidos = valida_numero(argv[2]);
    intervalo_video = valida_numero(argv[3]) * 1000;
    intervalo_music = valida_numero(argv[4]) * 1000;
    intervalo_social = valida_numero(argv[5]) * 1000;
    dados = valida_numero(argv[6]);
    id = getpid();

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

int valida_numero(const char *argv) {
    int valor = atoi(argv);
    if (valor == 0 && argv[0] != '0') {
        printf("Argumento inválido. Por favor, digite um número!\n");
        exit(EXIT_FAILURE);
    }
    return valor;
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
