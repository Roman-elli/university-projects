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

typedef struct
{
  long mtype;
  int answer;
} mq_user;

// SERVER_INFO
typedef struct{
	int mobile_users;
	int queue_pos;
	int auth_servers_max;
	int auth_proc_time;
	int max_video_wait;
	int max_others_wait;
	int user_number;
} Servidor;

// SHARED_MEMORY_INFO
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


typedef struct
{
  long mtype;
  Shared_report answer;
} mq_back;

typedef struct Queue_organizer {
    int user_id;
    char type[30];
    int data;
    time_t time;
    struct Queue_organizer *next;
} Queue_organizer;

// Global variables
extern FILE *file;
extern pid_t auth_engine_pid;
extern pid_t monitor_pid;
extern char message[MESSAGE_SIZE];
extern int id;
extern pthread_mutex_t mutex;
extern int number_int_validation(const char *argv);
extern sem_t *sem_mobile;


// Functions declarations
void start_program();
void create_semaphor();
void reset();
void sigint_monitorback_handler(int signum);
void data_stats();
void destroy_semaphor();
void sigint_system_handler(int signum);
void sigint_monitor_handler(int signum);
void sigint_auth_handler(int signum);
void sigint_request_handler(int signum);
void error(char *s);
void read_file(char *filename);
void authorization();
void auth_engine(int engine_id);
void monitor_engine();
void message_queue();
void create_shared_memory();
void write_log(char* message);
void end_program();
Queue_organizer* insert_queue(int user_id, char *type, int data);
void *sender_work(void *arg);
void *receiver_work(void *arg);
int check_user(int id);
int check_offline();
void free_queue(Queue_organizer **head_other, Queue_organizer **head_video);
int number_int_validation(const char *argv);

#endif