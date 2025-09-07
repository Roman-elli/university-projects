//Beatriz Alexandra Azeitona Mourato nº2022224891
//Thales Barbuto Romanelli Lopes nº2022169928

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

#define MESSAGE_SIZE 1024
#define DEBUG
#define USER_PIPE	"USER_PIPE"
#define BACK_PIPE "BACK_PIPE"
#define QUEUE_KEY 12345

// MQ info
int mq_id;

typedef struct
{
  long mtype;
  int answer;   // 0 > plafond terminado  1 > accepted
} mq_user;



// SERVER_INFO
typedef struct{
	int mobile_users;
	int queue_pos;
	int auth_servers_max;
	int auth_proc_time;
	int max_video_wait;
	int max_others_wait;
	int numero_usuario;
} Servidor;

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
typedef struct{
	int user_id;
	int data_total;
	int used_data;
	int on;
  int mq_oitenta;
  int mq_noventa;
  int mq_cem;
}Shared_data;
Shared_data *shared_var;
int shmid;


typedef struct{
	int total_video;
	int auth_video;
	int total_social;
	int auth_social;
	int total_music;
	int auth_music;
}Shared_report;
Shared_report *shared_report;
int shmid_report;

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


int request_video;
int request_other;
int size;

FILE *arquivo;

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
pid_t auth_engine_pid;
pid_t monitor_pid;
pid_t monitor_back_pid;

pthread_t sender_pthread, receiver_pthread;

void start_program();
void cria_semaforo();
void reset();
void sigint_monitorback_handler(int signum);
void data_stats();
void destroi_semaforo();
void sigint_system_handler(int signum);
void sigint_monitor_handler(int signum);
void sigint_auth_handler(int signum);
void sigint_request_handler(int signum);
void erro(char *s);
void read_file(char *filename);
void authorization();
void auth_engine(int engine_id);
void monitor_engine();
void message_queue();
void create_shared_memory();
void write_log();
void end_program();
Queue_organizer* insert_queue(int user_id, char *type, int data);
void *sender_work(void *arg);
void *receiver_work(void *arg);
int check_user(int id);
int check_offline();
void free_queue(Queue_organizer **head_other, Queue_organizer **head_video);
int valida_numero(const char *argv);
