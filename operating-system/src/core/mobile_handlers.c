#include "../../include/functions.h"

void *social_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (user_request > 0) {
            user_request--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (user_request == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_social, 0, sizeof(message_social));

        snprintf(message_social, sizeof(message_social), "%d#SOCIAL#%d\n", id, mobile_data);

        sem_wait(sem_mobile);

        if (write(fd_mobile, message_social, strlen(message_social)) < 0) {
            perror("Failed to write on mobile pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(social_duration);
    }
    pthread_exit(NULL);
}

void *music_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (user_request > 0) {
            user_request--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (user_request == 0) {
                kill(getpid(), SIGINT);
                break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_music, 0, sizeof(message_music));
        snprintf(message_music, sizeof(message_music), "%d#MUSIC#%d\n", id, mobile_data);

        sem_wait(sem_mobile);
        if (write(fd_mobile, message_music, strlen(message_music)) < 0) {
            perror("Failed to write on mobile pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(music_duration);
    }
    pthread_exit(NULL);
}

void *video_handler(void *arg) {
    while (1) {
        pthread_mutex_lock(&mutex);
        if (user_request > 0) {
            user_request--;
        } else {
            pthread_mutex_unlock(&mutex);
            if (user_request == 0) {
              kill(getpid(), SIGINT);
              break;
            }
            break;
        }
        pthread_mutex_unlock(&mutex);
        memset(message_video, 0, sizeof(message_video));
        snprintf(message_video, sizeof(message_video), "%d#VIDEO#%d\n", id, mobile_data);

        sem_wait(sem_mobile);
        if (write(fd_mobile, message_video, strlen(message_video)) < 0) {
            perror("Failed to write on mobile pipe.");
            break;
        }
        sem_post(sem_mobile);

        usleep(video_duration);
    }
    pthread_exit(NULL);
}
