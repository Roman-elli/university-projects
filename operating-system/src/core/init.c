#include "../../include/functions.h"

// =====================
// SERVER CONFIGURATION
// =====================
Servidor server;

// =====================
// PIPE CONFIGURATION
// =====================
fd_set read_set;

char message[MESSAGE_SIZE];
char message_stats[MESSAGE_SIZE];
char receive_command[MESSAGE_SIZE];
char receive_id[MESSAGE_SIZE];
char receive_data[MESSAGE_SIZE];
int data;
int id;

int size;

// =====================
// MESSAGE QUEUE (MQ) INFO
// =====================
int mq_id;

// =====================
// REQUEST COUNTERS
// =====================
int request_video;
int request_other;

// =====================
// SHARED MEMORY INFO
// =====================
Shared_data *shared_var;
Shared_report *shared_report;

Queue_organizer* video_request_queue;
Queue_organizer* other_request_queue;

int shmid;
int shmid_report;

// =====================
// PIPE FILE DESCRIPTORS
// =====================
int fd_user;
int fd_back;
int fd_backoffice;
int fd_mobile;

// =====================
// THREADING (MUTEX & CONDITION VARIABLES)
// =====================
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t go_on_sender = PTHREAD_COND_INITIALIZER;

// =====================
// PROCESS PIDS
// =====================
FILE *file;
pid_t auth_engine_pid;
pid_t monitor_pid;
pid_t monitor_back_pid;
pid_t* auth_manager_pid;

int (*unnamed_pipe)[2];

// =====================
// SEMAPHORE INFO
// =====================
char sem_name[20];

sem_t *sem_report;
sem_t *sem_queue;
sem_t *sem_log;
sem_t *sem_shared;
sem_t *sem_online;
sem_t *sem_monitor;
sem_t *sem_mobile;
sem_t** semaphores;
sem_t *sem_extra;

// =====================
// THREAD HANDLES
// =====================
pthread_t sender_pthread, receiver_pthread;

// =====================
// MOBILE PROCCESS VARIABLES
// =====================
pthread_t social_pthread, music_pthread, video_pthread;
char message_video[MESSAGE_SIZE];
char message_social[MESSAGE_SIZE];
char message_music[MESSAGE_SIZE];
int plafond = 0;
int user_request = 0;
int video_duration = 0;
int music_duration = 0;
int social_duration = 0;
int mobile_data = 0;
int message_length = 0;

void start_program(){
	server.user_number = 0;
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

void read_5gconfig_file(char *filename){
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
            write_log("Error opening 5G config file.");
            exit(1);
        }
		fclose(file);
	}else {
        write_log("Error opening 5G config file.");
	    exit(1);
	}
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
	free_queue(&other_request_queue, &video_request_queue);

	// Close MQ
	if (msgctl(mq_id, IPC_RMID, NULL) == -1) {
        perror("msgctl failed");
        exit(EXIT_FAILURE);
    }
	write_log("5G_AUTH_PLATFORM SIMULATOR CLOSING");
	// Close file writer
	fclose(file);
	destroy_semaphor();
	exit(EXIT_SUCCESS);
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
    msg.mtype = 2;
    msg.answer.total_video = shared_report->total_video;
    msg.answer.auth_video = shared_report->auth_video;
    msg.answer.total_social = shared_report->total_social;
    msg.answer.auth_social = shared_report->auth_social;
    msg.answer.total_music = shared_report->total_music;
    msg.answer.auth_music = shared_report->auth_music;

    sem_wait(sem_queue);
    if (msgsnd(mq_id, &msg, sizeof(msg.answer), IPC_NOWAIT) == -1) {
        write_log("msgsnd failed");
        exit(EXIT_FAILURE);
    }
		sem_post(sem_queue);

}
