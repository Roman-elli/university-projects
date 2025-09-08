#include "../../include/functions.h"

void authorization(){
		if ((mkfifo(USER_PIPE, O_CREAT|O_EXCL|0666)<0) && (errno!= EEXIST)) {
			write_log("Cannot create pipe: USER_PIPE");
			exit(0);
		}
		if ((mkfifo(BACK_PIPE, O_CREAT|O_EXCL|0666)<0) && (errno!= EEXIST)) {
			write_log("Cannot create pipe: BACK_PIPE");
			exit(0);
		}
		char message_auth[MESSAGE_SIZE];
		unnamed_pipe = malloc((server.auth_servers_max+1) * sizeof(int[2]));
		auth_manager_pid = malloc((server.auth_servers_max+1) * sizeof(pid_t));
    for (int i = 0; i < server.auth_servers_max; i++) {
	    	if (pipe(unnamed_pipe[i]) == -1) {
	    		write_log("Error creating unnamed pipe");
	    		exit(EXIT_FAILURE);
				}


        auth_manager_pid[i] = fork();
        if (auth_manager_pid[i] == 0) {
						signal(SIGINT, sigint_request_handler);
            snprintf(message_auth, sizeof(message_auth), "AUTHORIZATION_ENGINE %d READY", i);
            write_log(message_auth);
            auth_engine(i);
            exit(0);
        }else if (auth_manager_pid[i] == -1) {
            write_log("AUTHORIZATION_ENGINE CREATION PROCCESS FAILED");
            exit(1);
        }
    }


    video_request_queue = NULL;
    other_request_queue = NULL;

    pthread_create(&receiver_pthread, NULL, receiver_work, NULL);
    pthread_create(&sender_pthread, NULL, sender_work, NULL);

    pthread_join(receiver_pthread, NULL);
    pthread_join(sender_pthread, NULL);
}

void auth_engine(int engine_id) {
    Queue_organizer received_message;
    fd_set read_set_auth;
		char message_auth[MESSAGE_SIZE];
    float ratio;
    close(unnamed_pipe[engine_id][1]);
    double sleep_time = server.auth_proc_time*1000;
    Shared_data new_user;
    int indice;

		sigset_t set;

    sigemptyset(&set);
    sigaddset(&set, SIGINT);

    while (1) {
        indice = 0;
        FD_ZERO(&read_set_auth);
        FD_SET(unnamed_pipe[engine_id][0], &read_set_auth);

        if (select(unnamed_pipe[engine_id][0] + 1, &read_set_auth, NULL, NULL, NULL) > 0) {
						sigprocmask(SIG_BLOCK, &set, NULL);
            if(engine_id != server.auth_servers_max) sem_wait(sem_online);
						sem_wait(sem_extra);
						sem_wait(semaphores[engine_id]);
            read(unnamed_pipe[engine_id][0], &received_message, sizeof(Queue_organizer));
            if(strcmp(received_message.type, "INSERT") == 0) {
								new_user.user_id = received_message.user_id;
								new_user.data_total = received_message.data;
								new_user.used_data = 0;
								new_user.on = 1;
								new_user.mq_eighty = 0;
								new_user.mq_ninety = 0;
								new_user.mq_hundred = 0;
                sem_wait(sem_shared);
                indice = check_offline();
                if(indice != -1) {
                    shared_var[indice] = new_user;
										sem_post(sem_shared);
                }else sem_post(sem_shared);
            }else{
                if(received_message.user_id == 1) {
                    if(strcmp(received_message.type, "reset") == 0) {
											#ifdef DEBUG
												printf("Reset system in process...\n");
											#endif

                        reset();
                    } else {
											#ifdef DEBUG
												printf("Sending data stats to backuser...\n");
											#endif
                        data_stats();
                    }
                } else {
                    indice = check_user(received_message.user_id);
										if(shared_var[indice].on == 1){
												sem_wait(sem_shared);
		                    shared_var[indice].used_data += received_message.data;
												snprintf(message_auth, sizeof(message_auth), "AUTHORIZATION_ENGINE %d: %s AUTHORIZATION REQUEST (ID = %d)  PROCESSING COMPLETED", engine_id, received_message.type, received_message.user_id);
												write_log(message_auth);
		                    ratio = (float)shared_var[indice].used_data / shared_var[indice].data_total;
		                    if (ratio >= 1 && shared_var[indice].mq_hundred == 0) {
														shared_var[indice].on = 0;
		                        sem_post(sem_monitor);
		                    } else if (ratio >= 0.9 && shared_var[indice].mq_ninety == 0) {
		                        sem_post(sem_monitor);
		                    } else if (ratio >= 0.8 && shared_var[indice].mq_eighty == 0) {
		                        sem_post(sem_monitor);
		                    }
                    		sem_post(sem_shared);
										}

                    if(strcmp(received_message.type, "VIDEO") == 0) {
                        sem_wait(sem_report);
                        shared_report->total_video += received_message.data;
                        shared_report->auth_video++;
                        sem_post(sem_report);
                    } else if(strcmp(received_message.type, "MUSIC") == 0) {
                        sem_wait(sem_report);
                        shared_report->total_music += received_message.data;
                        shared_report->auth_music++;
                        sem_post(sem_report);
                    } else if(strcmp(received_message.type, "SOCIAL") == 0) {
                        sem_wait(sem_report);
                        shared_report->total_social += received_message.data;
                        shared_report->auth_social++;
                        sem_post(sem_report);
                    }
                }
            }
						sigprocmask(SIG_UNBLOCK, &set, NULL);
            usleep(sleep_time);
						sem_post(sem_extra);
						sem_post(semaphores[engine_id]);
            if(engine_id != server.auth_servers_max) sem_post(sem_online);
        }
    }
}


