#include "../../include/functions.h"

int check_user(int id){
	for(int i = 0; i < server.mobile_users; i++)
		if(shared_var[i].user_id == id) return i;
	return -1;
}

int check_offline(){
	for(int i = 0; i < server.mobile_users; i++)
		if(shared_var[i].on == 0) return i;
	return -1;
}

Queue_organizer* insert_queue(int user_id, char *type, int data) {
    Queue_organizer *new_node = (Queue_organizer *)malloc(sizeof(Queue_organizer));
    if (new_node == NULL) {
        perror("Failed to allocate memory for new other node");
        exit(EXIT_FAILURE);
    }
    new_node->user_id = user_id;
    strcpy(new_node->type, type);
    new_node->data = data;
    new_node->time = time(NULL);
    new_node->next = NULL;
    return new_node;
}
