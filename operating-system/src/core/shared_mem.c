#include "../../include/functions.h"

void create_shared_memory(){
    if ((shmid = shmget(IPC_PRIVATE, server.mobile_users * sizeof(Shared_data), IPC_CREAT | 0766)) < 0) {
    	write_log("Error in shmget with IPC_CREAT");
    	exit(1);
	}

	if ((shared_var = (Shared_data *) shmat(shmid, NULL, 0)) == (Shared_data *) -1) {
    	write_log("Shmat error!");
    	exit(1);
	}

    if ((shmid_report = shmget(IPC_PRIVATE, sizeof(Shared_report), IPC_CREAT | 0766)) < 0) {
    	write_log("Error in shmget with IPC_CREAT");
    	exit(1);
	}

	if ((shared_report = (Shared_report *) shmat(shmid_report, NULL, 0)) == (Shared_report *) -1) {
    	write_log("Shmat error!");
    	exit(1);
	}
}
