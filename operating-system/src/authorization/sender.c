#include "../../include/functions.h"

void *sender_work(void *arg) {
    write_log("THREAD SENDER CREATED");
		char message_sender[MESSAGE_SIZE];
		int other_full = 0;
		int video_full = 0;
		int extra_type = 0;

    for (int i = 0; i < server.auth_servers_max; i++) close(unnamed_pipe[i][0]);
    time_t end_time;
    int i;

    while(1) {
        pthread_mutex_lock(&mutex);

        while(request_video == 0 && request_other == 0) {
            pthread_cond_wait(&go_on_sender, &mutex);
        }
        if(request_other >= server.queue_pos && other_full == 0 && video_full == 0 && extra_type == 0){
                    extra_type = 1;
                    other_full = 1;
                    if (pipe(unnamed_pipe[server.auth_servers_max]) == -1) {
                    perror("Error creating pipe.");
                    exit(EXIT_FAILURE);
                    }
                    auth_manager_pid[server.auth_servers_max] = fork();
                    if (auth_manager_pid[server.auth_servers_max] == 0) {
            auth_engine(server.auth_servers_max);
            exit(0);
                    }
                    else if(auth_manager_pid[server.auth_servers_max] == -1) {
                write_log("AUTHORIZATION_ENGINE EXTRA CREATION PROCCESS FAILED");
                exit(1);
            }
                    write_log("SENDER: (OTHER QUEUE FULL) EXTRA AUTHORIZATION_ENGINE READY");
        }else if(request_video >= server.queue_pos && other_full == 0 && video_full == 0 && extra_type == 0){
                extra_type = 1;
                video_full = 1;
                if (pipe(unnamed_pipe[server.auth_servers_max]) == -1) {
                    perror("Error creating pipe.");
                    exit(EXIT_FAILURE);
                }
                auth_manager_pid[server.auth_servers_max] = fork();
                if (auth_manager_pid[server.auth_servers_max] == 0) {
                    auth_engine(server.auth_servers_max);
                    exit(0);
                }
                else if(auth_manager_pid[server.auth_servers_max] == -1) {
                        write_log("AUTHORIZATION_ENGINE EXTRA CREATION PROCCESS FAILED");
                        exit(1);
                }
                write_log("SENDER: (VIDEO QUEUE FULL) EXTRA AUTHORIZATION_ENGINE READY");
        }

        if(extra_type == 1 && other_full == 1 && request_other <= 0.5*server.queue_pos){
                extra_type = 0;
                other_full = 0;
                kill(auth_manager_pid[server.auth_servers_max], SIGKILL);
                write_log("SENDER: (OTHER QUEUE REACH 50%) EXTRA AUTHORIZATION_ENGINE ELIMINATED");
                close(unnamed_pipe[server.auth_servers_max][0]);
                close(unnamed_pipe[server.auth_servers_max][1]);
        }else if(extra_type == 1 && video_full == 1 && request_video <= 0.5*server.queue_pos){
                extra_type = 0;
                video_full = 0;
                kill(auth_manager_pid[server.auth_servers_max], SIGKILL);
                write_log("SENDER: (VIDEO QUEUE REACH 50%) EXTRA AUTHORIZATION_ENGINE ELIMINATED");
                close(unnamed_pipe[server.auth_servers_max][0]);
                close(unnamed_pipe[server.auth_servers_max][1]);
        }


        if(extra_type == 0){
            sem_wait(sem_online);
            i = 0;
            while(i < server.auth_servers_max) {
                if (sem_trywait(semaphores[i]) == 0) {
                        break;
                }
                    i++;
            }
            sem_post(semaphores[i]);
        }
        else if (extra_type == 1){
            sem_wait(sem_extra);
            i = 0;
            while(i <= server.auth_servers_max) {
                if (sem_trywait(semaphores[i]) == 0) {
                        break;
                }
                    i++;
            }
            sem_post(semaphores[i]);
        }

        end_time = time(NULL);
        if(request_video > 0) {
            Queue_organizer *message_video = video_request_queue;
            video_request_queue = video_request_queue->next;
            if(difftime(end_time, message_video->time)*1000 < server.max_video_wait){
								snprintf(message_sender, sizeof(message_sender), "SENDER: VIDEO AUTHORIZATION REQUEST (ID = %d) SENT FOR PROCESSING ON AUTHORIZATION_ENGINE %d", message_video->user_id,i);
								write_log(message_sender);
                write(unnamed_pipe[i][1], message_video, sizeof(Queue_organizer));
                free(message_video);
                request_video--;
            } else {
								snprintf(message_sender, sizeof(message_sender), "SENDER: TIME LIMIT REACHED FOR VIDEO REQUEST (ID = %d)", message_video->user_id);
                write_log(message_sender);
								free(message_video);
                request_video--;
            }
        } else if(request_other > 0) {
            Queue_organizer *message_other = other_request_queue;
            other_request_queue = other_request_queue->next;
            if(difftime(end_time, message_other->time)*1000 < server.max_video_wait) {
								snprintf(message_sender, sizeof(message_sender), "SENDER: %s AUTHORIZATION REQUEST (ID = %d) SENT FOR PROCESSING ON AUTHORIZATION_ENGINE %d", message_other->type,message_other->user_id,i);
								write_log(message_sender);
                write(unnamed_pipe[i][1], message_other, sizeof(Queue_organizer));
                free(message_other);
                request_other--;
            } else {
								snprintf(message_sender, sizeof(message_sender), "SENDER: TIME LIMIT REACHED FOR OTHER REQUEST (ID = %d)", message_other->user_id);
								write_log(message_sender);
								free(message_other);
                request_other--;
            }
        }


				if(extra_type == 0)sem_post(sem_online);
				else if(extra_type == 1)sem_post(sem_extra);
        pthread_mutex_unlock(&mutex);
    }
}
