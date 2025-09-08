#include "../include/functions.h"

int main(int argc, char *argv[]){
	if(argc != 2){
		printf("5g_auth_platform <config-file>\n");
		exit(-1);
	}
	read_file(argv[1]);

	create_semaphor();

    if (mkdir("data", 0755) == -1 && errno != EEXIST) {
        perror("Error creating data folder");
        exit(1);
    }
    if (mkdir("data/log", 0755) == -1 && errno != EEXIST) {
        perror("Error creating log folder");
        exit(1);
    }

	file = fopen("data/log/log.txt", "a");
	if (!file) {
		perror("Error opening log.txt");
		exit(1);
	}

	write_log("5G_AUTH_PLATFORM SIMULATOR STARTING");
	message_queue();
	create_shared_memory();
	start_program();
	write_log("PROCESS SYSTEM_MANAGER CREATED");


	auth_engine_pid = fork();
	if(auth_engine_pid == 0){
		signal(SIGINT, sigint_auth_handler);
		write_log("PROCESS AUTHORIZATION_REQUEST_MANAGER CREATED");
		authorization();
		exit(0);
	}
	else if(auth_engine_pid == -1){
		write_log("PROCESS AUTHORIZATION_REQUEST_MANAGER CREATION FAILED");
		exit(1);
	}

	monitor_pid = fork();
	if(monitor_pid == 0){
		signal(SIGINT, sigint_monitor_handler);
		write_log("PROCESS MONITOR_ENGINE CREATED");
		monitor_engine();
		exit(0);
	}
	else if(auth_engine_pid == -1){
		write_log("PROCESS MONITOR_ENGINE CREATION FAILED");
		exit(1);
	}

	signal(SIGINT, sigint_system_handler);
	end_program();
	exit(0);
}
