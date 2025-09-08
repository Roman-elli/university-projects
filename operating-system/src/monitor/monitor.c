#include "../../include/functions.h"

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
            if (usage_ratio >= 1 && shared_var[i].mq_hundred == 0) {
								shared_var[i].mq_hundred++;
								snprintf(message_monitor, sizeof(message_monitor), "ALERT 100%% (USER %d) TRIGGERED", i);
								write_log(message_monitor);
                msg.answer = 100;
            } else if (usage_ratio >= 0.9 && shared_var[i].mq_ninety == 0) {
								shared_var[i].mq_ninety++;
								snprintf(message_monitor, sizeof(message_monitor), "ALERT 90%% (USER %d) TRIGGERED", i);
								write_log(message_monitor);
                msg.answer = 90;
            } else if (usage_ratio >= 0.8 && shared_var[i].mq_eighty == 0) {
								shared_var[i].mq_eighty++;
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

