#include "../../include/functions.h"

void mq_mobile_analyser(){
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
      close(fd_mobile);
      pthread_mutex_unlock(&mutex);
      exit(EXIT_SUCCESS);
      }
    }
}


void *mq_backoffice_analyser(void *arg){
  mq_back msg;
  int mq_id = msgget(QUEUE_KEY, 0666);
  if (mq_id == -1) {
      perror("msgget failed");
      exit(EXIT_FAILURE);
  }
  while(1){
    if (msgrcv(mq_id, &msg, sizeof(msg.answer), 2, 0) == -1) {
        perror("msgrcv failed");
        exit(EXIT_FAILURE);
    }

	printf("+---------+------------+-----------+\n");
    printf("| %-7s | %-10s | %-9s |\n", "Service", "Total Data", "Auth Reqs");
    printf("+---------+------------+-----------+\n");
    printf("| %-7s | %10d | %9d |\n", "VIDEO", msg.answer.total_video, msg.answer.auth_video);
    printf("| %-7s | %10d | %9d |\n", "MUSIC", msg.answer.total_music, msg.answer.auth_music);
    printf("| %-7s | %10d | %9d |\n", "SOCIAL", msg.answer.total_social, msg.answer.auth_social);
    printf("+---------+------------+-----------+\n");
  }
  pthread_exit(NULL);
}