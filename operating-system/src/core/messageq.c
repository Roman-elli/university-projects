#include "../../include/functions.h"

void message_queue(){
    mq_id = msgget(QUEUE_KEY, 0666 | IPC_CREAT);
    if (mq_id == -1) {
        perror("msgget failed");
        exit(EXIT_FAILURE);
    }
}

