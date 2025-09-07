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


#define MESSAGE_SIZE 50
#define DEBUG
#define PIPE_NAME "BACK_PIPE"
#define QUEUE_KEY 12345

typedef struct{
	int total_video;
	int auth_video;
	int total_social;
	int auth_social;
	int total_music;
	int auth_music;
}Shared_report;

typedef struct
{
  long mtype;
  Shared_report answer;
} mq_back;

void sigint_handler(int signum);
void *mq_analyser(void *arg);

int fd;
pthread_t mq_pthread;

int main(void) {
    signal(SIGINT, sigint_handler);
    char message[MESSAGE_SIZE];
    char back_id[MESSAGE_SIZE];
    char back_command[MESSAGE_SIZE];

    pthread_create(&mq_pthread, NULL, mq_analyser, NULL);
    // Abre o pipe para escrita
    if ((fd = open(PIPE_NAME, O_WRONLY)) < 0) {
        perror("Cannot open pipe for writing.");
        exit(EXIT_FAILURE);
    }

    while (1) {

        // Lê a entrada do usuário
        if (fgets(message, MESSAGE_SIZE, stdin) == NULL) {
            perror("Error reading input.");
            exit(EXIT_FAILURE);
        }


        // Processa a entrada
        if (sscanf(message, "%29[^#]#%29s\n", back_id, back_command) != 2) {
            #ifdef DEBUG
            printf("Error: invalid input format!\n");
            #endif
            continue;
        }

        // Verifica se o ID é válido (1)
        if (strcmp(back_id, "1") == 0) {
            if (strcmp(back_command, "data_stats") == 0 || strcmp(back_command, "reset") == 0) {
                // Escreve a mensagem no pipe
                if (write(fd, message, strlen(message)) < 0) {
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

void sigint_handler(int signum) {
    printf("\nReceived SIGINT signal. Exiting...\n");
    // Fecha o descritor de arquivo antes de sair
    close(fd);
    exit(EXIT_SUCCESS);
}

void *mq_analyser(void *arg){
  // Obter o identificador da fila de mensagens
  mq_back msg;
  int mq_id = msgget(QUEUE_KEY, 0666);
  if (mq_id == -1) {
      perror("msgget failed");
      exit(EXIT_FAILURE);
  }
  while(1){
    // Receber uma mensagem
    if (msgrcv(mq_id, &msg, sizeof(msg.answer), 2, 0) == -1) {
        perror("msgrcv failed");
        exit(EXIT_FAILURE);
    }

    // Processar a mensagem recebida
		printf("+---------+------------+-----------+\n");
    printf("| %-7s | %-10s | %-9s |\n", "Service", "Total Data", "Auth Reqs");
    printf("+---------+------------+-----------+\n");

    // Linhas de dados
    printf("| %-7s | %10d | %9d |\n", "VIDEO", msg.answer.total_video, msg.answer.auth_video);
    printf("| %-7s | %10d | %9d |\n", "MUSIC", msg.answer.total_music, msg.answer.auth_music);
    printf("| %-7s | %10d | %9d |\n", "SOCIAL", msg.answer.total_social, msg.answer.auth_social);

    // Rodapé da tabela
    printf("+---------+------------+-----------+\n");
  }
  pthread_exit(NULL);
}
