#include "../include/functions.h"

// MQ info
int mq_id;

Servidor server;

// PIPE CONFIG

fd_set read_set;
int fd_user;
int fd_back;
char sem_name[20];
char message[MESSAGE_SIZE];
char message_stats[MESSAGE_SIZE];
char receive_command[MESSAGE_SIZE];
char receive_id[MESSAGE_SIZE];
char receive_data[MESSAGE_SIZE];
int data;
int id;

// SHARED_MEMORY_INFO
Shared_data *shared_var;
int shmid;

Shared_report *shared_report;
int shmid_report;

Queue_organizer* fila_video;
Queue_organizer* fila_other;
int (*unnamed_pipe)[2];
pid_t* auth_manager_pid;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t go_on_sender = PTHREAD_COND_INITIALIZER;

int request_video;
int request_other;
int size;

// SEMAFORO INFO
sem_t *sem_log;
sem_t *sem_shared;
sem_t *sem_report;
sem_t *sem_online;
sem_t *sem_monitor;
sem_t *sem_mobile;
sem_t** semaphores;
sem_t *sem_queue;
sem_t *sem_extra;

// PROCCESS PID
FILE *arquivo;
pid_t auth_engine_pid;
pid_t monitor_pid;
pid_t monitor_back_pid;

pthread_t sender_pthread, receiver_pthread;

void start_program(){
	server.numero_usuario = 0;
	request_video = 0;
	request_other = 0;
	for(int i = 0; i < server.mobile_users; i++) shared_var[i].on = 0;


	shared_report->total_video = 0;
	shared_report->auth_video = 0;
	shared_report->total_social = 0;
	shared_report->auth_social = 0;
	shared_report->total_music = 0;
	shared_report->auth_music = 0;
}

void cria_semaforo() {
    sem_unlink("LOG");
    sem_log = sem_open("LOG", O_CREAT|O_EXCL, 0666, 1);
    if (sem_log == SEM_FAILED) {
        write_log("Failed to create LOG semaphore");
        exit(EXIT_FAILURE);
    }

    sem_unlink("SHARED");
    sem_shared = sem_open("SHARED", O_CREAT|O_EXCL, 0700, 1);
    if (sem_shared == SEM_FAILED) {
        write_log("Failed to create SHARED semaphore");
        exit(EXIT_FAILURE);
    }

    sem_unlink("REPORT");
    sem_report = sem_open("REPORT", O_CREAT|O_EXCL, 0666, 1);
    if (sem_report == SEM_FAILED) {
        write_log("Failed to create REPORT semaphore");
        exit(EXIT_FAILURE);
    }

    sem_unlink("ONLINE");
    sem_online = sem_open("ONLINE", O_CREAT|O_EXCL, 0666, server.auth_servers_max);
    if (sem_online == SEM_FAILED) {
        write_log("Failed to create ONLINE semaphore");
        exit(EXIT_FAILURE);
    }

    sem_unlink("EXTRA");
    sem_extra = sem_open("EXTRA", O_CREAT|O_EXCL, 0666, server.auth_servers_max + 1);
    if (sem_extra == SEM_FAILED) {
        write_log("Failed to create EXTRA semaphore");
        exit(EXIT_FAILURE);
    }

    sem_unlink("QUEUE");
    sem_queue = sem_open("QUEUE", O_CREAT|O_EXCL, 0666, 1);
    if (sem_queue == SEM_FAILED) {
        write_log("Failed to create QUEUE semaphore");
        exit(EXIT_FAILURE);
    }

    semaphores = (sem_t**)malloc((server.auth_servers_max + 1) * sizeof(sem_t*));
    if (semaphores == NULL) {
        write_log("Failed to allocate memory for semaphores");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < server.auth_servers_max + 1; i++) {
        semaphores[i] = NULL;
        char sem_name[256];
        sprintf(sem_name, "ONLINE_%d", i);
        sem_unlink(sem_name);
        semaphores[i] = sem_open(sem_name, O_CREAT | O_EXCL, 0666, 1);
        if (semaphores[i] == SEM_FAILED) {
            write_log("sem_open failed for semaphores[i]");
            exit(EXIT_FAILURE);
        }
    }

    sem_unlink("MONITOR");
    sem_monitor = sem_open("MONITOR", O_CREAT|O_EXCL, 0666, 0);
    if (sem_monitor == SEM_FAILED) {
        write_log("Failed to create MONITOR semaphore");
        exit(EXIT_FAILURE);
    }

    sem_unlink("MOBILE");
    sem_mobile = sem_open("MOBILE", O_CREAT|O_EXCL, 0666, 1);
    if (sem_mobile == SEM_FAILED) {
        write_log("Failed to create MOBILE semaphore");
        exit(EXIT_FAILURE);
    }
}

void destroi_semaforo(){
	sem_close(sem_log);
	sem_unlink("LOG");

	sem_close(sem_shared);
	sem_unlink("SHARED");

	sem_close(sem_report);
	sem_unlink("REPORT");

	sem_close(sem_queue);
	sem_unlink("QUEUE");

	sem_close(sem_online);
	sem_unlink("ONLINE");

	sem_close(sem_extra);
	sem_unlink("EXTRA");

	for (int i = 0; i < server.auth_servers_max+1; i++) {
        if (semaphores[i]) {
            sem_close(semaphores[i]);
            sprintf(sem_name, "ONLINE_%d", i);
            sem_unlink(sem_name);
        }
    }
	free(semaphores);

	sem_close(sem_monitor);
	sem_unlink("MONITOR");

	sem_close(sem_mobile);
	sem_unlink("MOBILE");
}

void sigint_system_handler(int signum) {
    end_program();
}

void sigint_monitor_handler(int signum) {
	#ifdef DEBUG
	  printf("Monitor Engine Received SIGINT signal. Exiting...\n");
	#endif

		waitpid(monitor_back_pid, NULL, 0);
    exit(EXIT_SUCCESS);
}

void sigint_monitorback_handler(int signum){
		exit(EXIT_SUCCESS);
}

void sigint_auth_handler(int signum){
		for (int i = 0; i < server.auth_servers_max; i++) {
				close(unnamed_pipe[i][0]); // Fecha o descritor de leitura
				close(unnamed_pipe[i][1]); // Fecha o descritor de escrita
				waitpid(auth_manager_pid[i], NULL, 0);
		}

		// Libera a memória alocada para os ponteiros de array
		free(unnamed_pipe);
		free(auth_manager_pid);

		#ifdef DEBUG
		  printf("Authorization Manager Received SIGINT signal. Exiting...\n");
		#endif
    exit(EXIT_SUCCESS);
}

void sigint_request_handler(int signum){
    exit(EXIT_SUCCESS);
}

void erro(char *s) {
    perror(s);
    exit(1);
}

void read_file(char *filename){
	FILE* file = fopen(filename, "r");
	if (file != NULL){
		if (fscanf(file, "%d", &server.mobile_users) == 1 &&
            fscanf(file, "%d", &server.queue_pos) == 1 &&
            fscanf(file, "%d", &server.auth_servers_max) == 1 &&
            fscanf(file, "%d", &server.auth_proc_time) == 1 &&
            fscanf(file, "%d", &server.max_video_wait) == 1 &&
            fscanf(file, "%d", &server.max_others_wait) == 1) {

            #ifdef DEBUG
            printf("Mobile Users: %d\n", server.mobile_users);
            printf("Queue Position: %d\n", server.queue_pos);
            printf("Auth Servers Max: %d\n", server.auth_servers_max);
            printf("Auth Proc Time: %d\n", server.auth_proc_time);
            printf("Max Video Wait: %d\n", server.max_video_wait);
            printf("Max Others Wait: %d\n", server.max_others_wait);
            #endif
        } else {
            write_log("Erro ao ler valores do arquivo.");
            exit(1);
        }
		fclose(file);
	}else {
   write_log("Erro ao ler ficheiro");
	exit(1);
	}
}

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
	    		write_log("Erro ao criar o unnamed pipe");
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


		fila_video = NULL;
		fila_other = NULL;

    pthread_create(&receiver_pthread, NULL, receiver_work, NULL);
    pthread_create(&sender_pthread, NULL, sender_work, NULL);

    pthread_join(receiver_pthread, NULL);
    pthread_join(sender_pthread, NULL);
}

void monitor_engine() {
    mq_user msg;
		float usage_ratio;
		char message_monitor[MESSAGE_SIZE];

		monitor_back_pid = fork();
		if(monitor_back_pid == 0){
				signal(SIGINT, sigint_monitorback_handler);
				while(1){
					sleep(30);
					sem_wait(sem_report);
					data_stats();
					sem_post(sem_report);
				}
				exit(EXIT_SUCCESS);
		}

    while (1) {
				sem_wait(sem_monitor);
        sem_wait(sem_shared);
        for (int i = 0; i < server.mobile_users; i++) {
            usage_ratio = (float)shared_var[i].used_data / shared_var[i].data_total;
            if (usage_ratio >= 1 && shared_var[i].mq_cem == 0) {
								shared_var[i].mq_cem++;
								snprintf(message_monitor, sizeof(message_monitor), "ALERT 100%% (USER %d) TRIGGERED", i);
								write_log(message_monitor);
                msg.answer = 100;
            } else if (usage_ratio >= 0.9 && shared_var[i].mq_noventa == 0) {
								shared_var[i].mq_noventa++;
								snprintf(message_monitor, sizeof(message_monitor), "ALERT 90%% (USER %d) TRIGGERED", i);
								write_log(message_monitor);
                msg.answer = 90;
            } else if (usage_ratio >= 0.8 && shared_var[i].mq_oitenta == 0) {
								shared_var[i].mq_oitenta++;
								snprintf(message_monitor, sizeof(message_monitor), "ALERT 80%% (USER %d) TRIGGERED", i);
								write_log(message_monitor);
                msg.answer = 80;
            } else {
                continue;
            }
						msg.mtype = shared_var[i].user_id;
						sem_wait(sem_queue);
            if (msgsnd(mq_id, &msg, sizeof(msg.answer), IPC_NOWAIT) == -1) {
                write_log("msgsnd failed");
            }
						sem_post(sem_queue);
        }
        sem_post(sem_shared);
    }
}

void message_queue(){
	// Criar a fila de mensagens
    mq_id = msgget(QUEUE_KEY, 0666 | IPC_CREAT);
    if (mq_id == -1) {
        perror("msgget failed");
        exit(EXIT_FAILURE);
    }
}

void create_shared_memory(){
	// Criando a memória compartilhada
    if ((shmid = shmget(IPC_PRIVATE, server.mobile_users * sizeof(Shared_data), IPC_CREAT | 0766)) < 0) {
    	write_log("Error in shmget with IPC_CREAT");
    	exit(1);
	}

	// Associando a memória compartilhada ao espaço de endereço do processo
	if ((shared_var = (Shared_data *) shmat(shmid, NULL, 0)) == (Shared_data *) -1) {
    	write_log("Shmat error!");
    	exit(1);
	}



	// Criando a memória compartilhada
    if ((shmid_report = shmget(IPC_PRIVATE, sizeof(Shared_report), IPC_CREAT | 0766)) < 0) {
    	write_log("Error in shmget with IPC_CREAT");
    	exit(1);
	}

	// Associando a memória compartilhada ao espaço de endereço do processo
	if ((shared_report = (Shared_report *) shmat(shmid_report, NULL, 0)) == (Shared_report *) -1) {
    	write_log("Shmat error!");
    	exit(1);
	}
}

void write_log(char* message){
		time_t tempo_atual;
    struct tm *info_tempo;

    time(&tempo_atual);
    info_tempo = localtime(&tempo_atual);

    #ifdef DEBUG
    printf("%s\n", message);
    #endif
    sem_wait(sem_log);
    fprintf(arquivo, "%02d:%02d:%02d %s\n", info_tempo->tm_hour, info_tempo->tm_min, info_tempo->tm_sec, message);
    fflush(arquivo);
    sem_post(sem_log);
}

void *sender_work(void *arg) {
    write_log("THREAD SENDER CREATED");
		char message_sender[MESSAGE_SIZE];
		int other_full = 0;
		int video_full = 0;
		int extra_type = 0;

    for (int i = 0; i < server.auth_servers_max; i++) close(unnamed_pipe[i][0]); // Fechamento dos descritores de leitura
    time_t end_time;
    int i;

    while(1) {
        pthread_mutex_lock(&mutex);

        while(request_video == 0 && request_other == 0) {
            pthread_cond_wait(&go_on_sender, &mutex);
        }


				//	CRIA AUTH ENGINE EXTRA
				if(request_other >= server.queue_pos && other_full == 0 && video_full == 0 && extra_type == 0){
							extra_type = 1;
							other_full = 1;
							if (pipe(unnamed_pipe[server.auth_servers_max]) == -1) {
				    		perror("Erro ao criar o pipe");
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
							perror("Erro ao criar o pipe");
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

				// DESTROI AUTH ENGINE EXTRA
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
						if (sem_trywait(semaphores[i]) == 0) { // Tenta adquirir o semáforo da engine
								break; // Sai do loop assim que encontrar uma engine livre
						}
							i++;
					}
					sem_post(semaphores[i]); // Libera o semáforo do servidor específico
				}
				else if (extra_type == 1){
					sem_wait(sem_extra);
					i = 0;
					while(i <= server.auth_servers_max) {
						if (sem_trywait(semaphores[i]) == 0) { // Tenta adquirir o semáforo da engine
								break; // Sai do loop assim que encontrar uma engine livre
						}
							i++;
					}
					sem_post(semaphores[i]); // Libera o semáforo do servidor específic
				}


        end_time = time(NULL);
        if(request_video > 0) {
            Queue_organizer *message_video = fila_video;
            fila_video = fila_video->next;
            if(difftime(end_time, message_video->time)*1000 < server.max_video_wait){
								snprintf(message_sender, sizeof(message_sender), "SENDER: VIDEO AUTHORIZATION REQUEST (ID = %d) SENT FOR PROCESSING ON AUTHORIZATION_ENGINE %d", message_video->user_id,i);
								write_log(message_sender);
                write(unnamed_pipe[i][1], message_video, sizeof(Queue_organizer));
                free(message_video); // Libera a memória alocada para a mensagem
                request_video--;
            } else {
								snprintf(message_sender, sizeof(message_sender), "SENDER: TIME LIMIT REACHED FOR VIDEO REQUEST (ID = %d)", message_video->user_id);
                write_log(message_sender);
								free(message_video); // Libera a memória alocada para a mensagem
                request_video--;
            }
        } else if(request_other > 0) {
            Queue_organizer *message_other = fila_other;
            fila_other = fila_other->next;
            if(difftime(end_time, message_other->time)*1000 < server.max_video_wait) {
								snprintf(message_sender, sizeof(message_sender), "SENDER: %s AUTHORIZATION REQUEST (ID = %d) SENT FOR PROCESSING ON AUTHORIZATION_ENGINE %d", message_other->type,message_other->user_id,i);
								write_log(message_sender);
                write(unnamed_pipe[i][1], message_other, sizeof(Queue_organizer));
                free(message_other); // Libera a memória alocada para a mensagem
                request_other--;
            } else {
								snprintf(message_sender, sizeof(message_sender), "SENDER: TIME LIMIT REACHED FOR OTHER REQUEST (ID = %d)", message_other->user_id);
								write_log(message_sender);
								free(message_other); // Libera a memória alocada para a mensagem
                request_other--;
            }
        }


				if(extra_type == 0)sem_post(sem_online); // Libera o semáforo para o próximo sender
				else if(extra_type == 1)sem_post(sem_extra);
        pthread_mutex_unlock(&mutex);
    }
}

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
												int id = valida_numero(receive_id);
												int data = valida_numero(receive_data);
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
                                if (fila_video == NULL) {
                                    fila_video = new_person;
                                } else {
                                    Queue_organizer *current = fila_video;
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
                                if (fila_other == NULL) {
                                    fila_other = new_person;
                                } else {
                                    Queue_organizer *current = fila_other;
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
                            if (fila_other == NULL) {
                                fila_other = new_person;
                            } else {
                                Queue_organizer *current = fila_other;
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
                    int id = valida_numero(receive_id);
                    if (request_other > server.queue_pos) {
                        snprintf(message_receiver, sizeof(message_receiver), "RECEIVER: OTHER SERVICE REQUEST REJECTED (OTHER QUEUE FULL) (ID = %d)", id);
                        write_log(message_receiver);
                    } else {
                        new_person = insert_queue(id, receive_command, data);
                        pthread_mutex_lock(&mutex);
                        if (fila_other == NULL) {
                            fila_other = new_person;
                        } else {
                            Queue_organizer *current = fila_other;
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

int check_user(int id){
	for(int i = 0; i < server.mobile_users; i++)
		if(shared_var[i].user_id == id) return i;
	return -1;
}

int check_offline(){
	for(int i = 0; i < server.mobile_users; i++)
		if(shared_var[i].on == 0) return i;
	return -1;
}

Queue_organizer* insert_queue(int user_id, char *type, int data) {
    Queue_organizer *new_node = (Queue_organizer *)malloc(sizeof(Queue_organizer));
    if (new_node == NULL) {
        perror("Failed to allocate memory for new other node");
        exit(EXIT_FAILURE);
    }
    new_node->user_id = user_id;
    strcpy(new_node->type, type);
    new_node->data = data;
    new_node->time = time(NULL);
    new_node->next = NULL;
    return new_node;
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

    // Prepara o conjunto de sinais para bloquear SIGINT
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
								new_user.mq_oitenta = 0;
								new_user.mq_noventa = 0;
								new_user.mq_cem = 0;
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
		                    if (ratio >= 1 && shared_var[indice].mq_cem == 0) {
														shared_var[indice].on = 0;
		                        sem_post(sem_monitor);
		                    } else if (ratio >= 0.9 && shared_var[indice].mq_noventa == 0) {
		                        sem_post(sem_monitor);
		                    } else if (ratio >= 0.8 && shared_var[indice].mq_oitenta == 0) {
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

void reset(){
	sem_wait(sem_report);
	shared_report->total_video = 0;
	shared_report->auth_video = 0;
	shared_report->total_social = 0;
	shared_report->auth_social = 0;
	shared_report->total_music = 0;
	shared_report->auth_music = 0;
	sem_post(sem_report);
}

void data_stats(){
		mq_back msg;
	 // Enviar a mensagem
    msg.mtype = 2;  // 1 para accepted, como exemplo
    msg.answer.total_video = shared_report->total_video;
		msg.answer.auth_video = shared_report->auth_video;
		msg.answer.total_social = shared_report->total_social;
		msg.answer.auth_social = shared_report->auth_social;
		msg.answer.total_music = shared_report->total_music;
		msg.answer.auth_music = shared_report->auth_music;

		sem_wait(sem_queue);
    // Enviar a mensagem
    if (msgsnd(mq_id, &msg, sizeof(msg.answer), IPC_NOWAIT) == -1) {
        write_log("msgsnd failed");
        exit(EXIT_FAILURE);
    }
		sem_post(sem_queue);

}

int valida_numero(const char *argv) {
    if (atoi(argv) == 0) {
				write_log("ERROR IN INT CONVERTION");
        return -1;
    }
    return atoi(argv);
}

void free_queue(Queue_organizer **head_other, Queue_organizer **head_video) {
		char message_free[MESSAGE_SIZE];
    // Liberar a fila 'Queue_other'
    Queue_organizer *current_other = *head_other;
    Queue_organizer *next_other;

    while (current_other != NULL) {
        next_other = current_other->next; // Salve o próximo nó
				snprintf(message_free, sizeof(message_free), "5G_AUTH_PLATFORM SIMULATOR: %s AUTHORIZATION REQUEST (ID = %d)  PROCESSING IMCOMPLETED", current_other->type, current_other->user_id);
				write_log(message_free);
        free(current_other);              // Libere o nó atual
        current_other = next_other;       // Mova para o próximo nó
    }
    *head_other = NULL; // Certifique-se de que o cabeçalho agora aponta para NULL

    // Liberar a fila 'Queue_video'
    Queue_organizer *current_video = *head_video;
    Queue_organizer *next_video;

    while (current_video != NULL) {
        next_video = current_video->next; // Salve o próximo nó
				snprintf(message_free, sizeof(message_free), "5G_AUTH_PLATFORM SIMULATOR: %s AUTHORIZATION REQUEST (ID = %d)  PROCESSING IMCOMPLETED", current_video->type, current_video->user_id);
				write_log(message_free);
        free(current_video);              // Libere o nó atual
        current_video = next_video;       // Mova para o próximo nó
    }
    *head_video = NULL; // Certifique-se de que o cabeçalho agora aponta para NULL
}

void end_program(){
	// WAIT FOR AUTHORIZATION REQUEST MANAGER
	write_log("SIGNAL SIGINT RECEIVED");
	write_log("5G_AUTH_PLATFORM SIMULATOR WAITING FOR LAST TASKS TO FINISH");
	waitpid(auth_engine_pid, NULL, 0);
	waitpid(monitor_pid, NULL, 0);


		// Clean pipes
	unlink(USER_PIPE);
	unlink(BACK_PIPE);
	close(fd_user);
  close(fd_back);

    // Clean shared memory
	shmdt(shared_var);
	shmctl(shmid, IPC_RMID, NULL);

	// Clean condition variables
	pthread_cond_broadcast(&go_on_sender);
	pthread_mutex_unlock(&mutex);
	pthread_mutex_destroy(&mutex);

	// Clean queues
	free_queue(&fila_other, &fila_video);

	// Close MQ
	if (msgctl(mq_id, IPC_RMID, NULL) == -1) {
        perror("msgctl failed");
        exit(EXIT_FAILURE);
    }
	write_log("5G_AUTH_PLATFORM SIMULATOR CLOSING");
	// Close file writer
	fclose(arquivo);
	destroi_semaforo();
	exit(EXIT_SUCCESS);
}
