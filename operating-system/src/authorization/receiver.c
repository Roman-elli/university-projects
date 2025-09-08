#include "../../include/functions.h"

void *receiver_work(void *arg) {
    char message_receiver[MESSAGE_SIZE];
		int online;

    write_log("THREAD RECEIVER CREATED");

    Queue_organizer *new_person;
    int fd_user, fd_back;
    int size;

    if ((fd_user = open(USER_PIPE, O_RDWR)) < 0) {
        write_log("Cannot open USER_PIPE for reading");
        pthread_exit(NULL);
    }

    if ((fd_back = open(BACK_PIPE, O_RDWR)) < 0) {
        write_log("Cannot open BACK_PIPE for reading");
        pthread_exit(NULL);
    }

    printf("Listening to all pipes!\n\n");
    while (1) {
        fd_set read_set;
        FD_ZERO(&read_set);
        FD_SET(fd_user, &read_set);
        FD_SET(fd_back, &read_set);

        if (select(fd_back + 1, &read_set, NULL, NULL, NULL) > 0) {
            if (FD_ISSET(fd_user, &read_set)) {
                size = read(fd_user, message_receiver, sizeof(message_receiver));
                if (size > 0) {
                    message_receiver[size] = '\0';
                    char *token = strtok(message_receiver, "\n");
                    while (token != NULL) {
                        sscanf(token, "%[^#]#%[^#]#%s", receive_id, receive_command, receive_data);
												int id = number_int_validation(receive_id);
												int data = number_int_validation(receive_data);
												sem_wait(sem_shared);
												online = check_user(id);
												sem_post(sem_shared);
                        if (strcmp(receive_command, "INSERT") != 0 && online >= 0) {
                         		new_person = insert_queue(id, receive_command, data);
                            if (strcmp(receive_command, "VIDEO") == 0) {
															if (request_video > server.queue_pos) {
																	snprintf(message_receiver, sizeof(message_receiver), "RECEIVER: VIDEO SERVICE REQUEST REJECTED (VIDEO QUEUE FULL) (ID = %d)", id);
																	write_log(message_receiver);
															}
															else{
                                pthread_mutex_lock(&mutex);
                                if (video_request_queue == NULL) {
                                    video_request_queue = new_person;
                                } else {
                                    Queue_organizer *current = video_request_queue;
                                    while (current->next != NULL) {
                                        current = current->next;
                                    }
                                    current->next = new_person;
                                }
                                request_video++;
                                pthread_cond_signal(&go_on_sender);
                                pthread_mutex_unlock(&mutex);
															}
                            } else if (strcmp(receive_command, "MUSIC") == 0 || strcmp(receive_command, "SOCIAL") == 0) {
															if (request_other > server.queue_pos){
					                        snprintf(message_receiver, sizeof(message_receiver), "RECEIVER: OTHER SERVICE REQUEST REJECTED (OTHER QUEUE FULL) (ID = %d)", id);
																	write_log(message_receiver);
																}else{
                                pthread_mutex_lock(&mutex);
                                if (other_request_queue == NULL) {
                                    other_request_queue = new_person;
                                } else {
                                    Queue_organizer *current = other_request_queue;
                                    while (current->next != NULL) {
                                        current = current->next;
                                    }
                                    current->next = new_person;
                                }
                                request_other++;
                                pthread_cond_signal(&go_on_sender);
                                pthread_mutex_unlock(&mutex);}
                            }
                        } else {
                            new_person = insert_queue(id, receive_command, data);
                            pthread_mutex_lock(&mutex);
                            if (other_request_queue == NULL) {
                                other_request_queue = new_person;
                            } else {
                                Queue_organizer *current = other_request_queue;
                                while (current->next != NULL) {
                                    current = current->next;
                                }
                                current->next = new_person;
                            }
                            request_other++;
                            pthread_cond_signal(&go_on_sender);
                            pthread_mutex_unlock(&mutex);
                        }
                        token = strtok(NULL, "\n"); // Next token
                    }
                }
            }
            if (FD_ISSET(fd_back, &read_set)) {
                size = read(fd_back, message_receiver, sizeof(message_receiver));
                if (size > 0) {
                    message_receiver[size - 1] = '\0';
                    sscanf(message_receiver, "%[^#]#%s", receive_id, receive_command);
                    int id = number_int_validation(receive_id);
                    if (request_other > server.queue_pos) {
                        snprintf(message_receiver, sizeof(message_receiver), "RECEIVER: OTHER SERVICE REQUEST REJECTED (OTHER QUEUE FULL) (ID = %d)", id);
                        write_log(message_receiver);
                    } else {
                        new_person = insert_queue(id, receive_command, data);
                        pthread_mutex_lock(&mutex);
                        if (other_request_queue == NULL) {
                            other_request_queue = new_person;
                        } else {
                            Queue_organizer *current = other_request_queue;
                            while (current->next != NULL) {
                                current = current->next;
                            }
                            current->next = new_person;
                        }
                        request_other++;
                        pthread_cond_signal(&go_on_sender);
                        pthread_mutex_unlock(&mutex);
                    }
                }
            }
        }
    }

    #ifdef DEBUG
        printf("Thread receiver is finishing\n");
    #endif
    close(fd_user);
    close(fd_back);
    pthread_exit(NULL);
}
