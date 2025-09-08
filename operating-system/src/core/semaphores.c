#include "../../include/functions.h"

void create_semaphor() {
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

void destroy_semaphor(){
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
