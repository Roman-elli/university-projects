#include "../../include/functions.h"

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
				close(unnamed_pipe[i][0]);
				close(unnamed_pipe[i][1]);
				waitpid(auth_manager_pid[i], NULL, 0);
		}

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

void sigint_backoffice_handler(int signum) {
    printf("\nReceived SIGINT signal. Exiting...\n");
    close(fd_backoffice);
    exit(EXIT_SUCCESS);
}

void sigint_mobile_handler(int signum) {
    #ifdef DEBUG
    printf("\nNumber of user_requests exhausted...\n");
    #endif
    close(fd_mobile);
    pthread_mutex_unlock(&mutex);
    pthread_mutex_destroy(&mutex);
    exit(EXIT_SUCCESS);
}