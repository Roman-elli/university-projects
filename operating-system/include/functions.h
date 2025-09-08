#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <sys/msg.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <semaphore.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <time.h>
#include <pthread.h>
#include <signal.h>
#include <errno.h>
#include <sys/select.h>
#include <asm-generic/signal-defs.h>

#define MESSAGE_SIZE 1024
#define DEBUG
#define USER_PIPE "USER_PIPE"
#define BACK_PIPE "BACK_PIPE"
#define QUEUE_KEY 12345

// =====================
// SERVER INFORMATION
// =====================
typedef struct{
	int mobile_users;
	int queue_pos;
	int auth_servers_max;
	int auth_proc_time;
	int max_video_wait;
	int max_others_wait;
	int user_number;
} Servidor;

// =====================
// SHARED MEMORY INFORMATION
// =====================
typedef struct{
	int user_id;
	int data_total;
	int used_data;
	int on;
	int mq_eighty;
	int mq_ninety;
	int mq_hundred;
}Shared_data;

typedef struct{
	int total_video;
	int auth_video;
	int total_social;
	int auth_social;
	int total_music;
	int auth_music;
}Shared_report;

// =====================
// MESSAGE QUEUE STRUCTURES
// =====================
typedef struct
{
  long mtype;
  int answer;
} mq_user;

typedef struct
{
  long mtype;
  Shared_report answer;
} mq_back;

// =====================
// QUEUE ORGANIZER STRUCTURE
// =====================
typedef struct Queue_organizer {
    int user_id;
    char type[30];
    int data;
    time_t time;
    struct Queue_organizer *next;
} Queue_organizer;

// =====================
// GLOBAL VARIABLES
// =====================
extern Servidor server;
extern FILE *file;
extern pid_t auth_engine_pid;
extern pid_t monitor_pid;
extern char message[MESSAGE_SIZE];
extern int id;
extern pthread_mutex_t mutex;
extern int number_int_validation(const char *argv);
extern char sem_name[20];

// =====================
// MESSAGE QUEUE INFO
// =====================
extern int mq_id;

// =====================
// SHARED MEMORY IDS
// =====================
extern int shmid;
extern int shmid_report;

// =====================
// SHARED MEMORY POINTERS
// =====================
extern Shared_data *shared_var;
extern Shared_report *shared_report;

// =====================
// SEMAPHORES
// =====================
extern sem_t *sem_report;
extern sem_t *sem_queue;
extern sem_t *sem_log;
extern sem_t *sem_shared;
extern sem_t *sem_online;
extern sem_t *sem_monitor;
extern sem_t *sem_mobile;
extern sem_t** semaphores;
extern sem_t *sem_extra;

// =====================
// PROCESS PIDS
// =====================
extern FILE *file;
extern pid_t auth_engine_pid;
extern pid_t monitor_pid;
extern pid_t monitor_back_pid;
extern pid_t* auth_manager_pid;

extern int (*unnamed_pipe)[2];

// =====================
// REQUEST VARIABLES
// =====================
extern int request_video;
extern int request_other;

extern Queue_organizer* video_request_queue;
extern Queue_organizer* other_request_queue;

// =====================
// THREADS
// =====================
extern pthread_t sender_pthread, receiver_pthread;

extern pthread_cond_t go_on_sender;

// =====================
// MESSAGE BUFFERS
// =====================
extern char message[MESSAGE_SIZE];
extern char message_stats[MESSAGE_SIZE];
extern char receive_command[MESSAGE_SIZE];
extern char receive_id[MESSAGE_SIZE];
extern char receive_data[MESSAGE_SIZE];
extern int data;
extern int id;

// =====================
// PIPE FILE DESCRIPTORS
// =====================
extern int fd_user;
extern int fd_back;
extern int fd_backoffice;
extern int fd_mobile;

// =====================
// MOBILE PROCESS VARIABLES
// =====================
extern pthread_t social_pthread, music_pthread, video_pthread;
extern char message_video[MESSAGE_SIZE];
extern char message_social[MESSAGE_SIZE];
extern char message_music[MESSAGE_SIZE];
extern int plafond;
extern int user_request;
extern int video_duration;
extern int music_duration;
extern int social_duration;
extern int mobile_data;
extern int message_length;

// =====================
// FUNCTIONS DECLARATIONS
// =====================

// PROGRAM CONTROL FUNCTIONS
void start_program();
void end_program();
void reset();
void data_stats();

// SEMAPHORE AND SHARED MEMORY FUNCTIONS
void create_semaphor();
void create_shared_memory();
void destroy_semaphor();

// SIGNAL HANDLERS
void sigint_monitorback_handler(int signum);
void sigint_system_handler(int signum);
void sigint_monitor_handler(int signum);
void sigint_auth_handler(int signum);
void sigint_request_handler(int signum);
void sigint_backoffice_handler(int signum); // back handler
void sigint_mobile_handler(int signum); // mobile handler

// ERROR HANDLING
void error(char *s);

// AUTHORIZATION AND MONITORING
void authorization();
void auth_engine(int engine_id);
void monitor_engine();

// QUEUE AND MESSAGE FUNCTIONS
void free_queue(Queue_organizer **head_other, Queue_organizer **head_video);
void message_queue();
void *mq_backoffice_analyser(void *arg);
void mq_mobile_analyser();

// MOBILE HANDLERS
void *music_handler(void *arg);
void *social_handler(void *arg);
void *video_handler(void *arg);

// LOG AND CONFIG FUNCTIONS
void write_log(char* message);
void read_5gconfig_file(char *filename);
void read_mobile_config_file(char* filename);

// QUEUE MANAGEMENT
Queue_organizer* insert_queue(int user_id, char *type, int data);

// SENDER AND RECEIVER THREADS
void *sender_work(void *arg);
void *receiver_work(void *arg);

// USER CHECKS AND VALIDATION
int check_user(int id);
int check_offline();
int number_int_validation(const char *argv);

#endif
