#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "functions.h"

char *category_name[] = names;

struct node *newnode(enum category category, char *token) {
    struct node *new = malloc(sizeof(struct node));
    new->category = category;
    new->token = token;
    new->type = void_type;
    new->used = 0;
    new->isFunction = 0;
    new->param_list[0] = '\0';
    new->print_type = 0;
    new->children = malloc(sizeof(struct node_list));
    new->children->node = NULL;
    new->children->next = NULL;
    return new;
}

void addchild(struct node *parent, struct node *child) {
    struct node_list *new = malloc(sizeof(struct node_list));
    new->node = child;
    new->next = NULL;
    struct node_list *children = parent->children;
    while(children->next != NULL)
        children = children->next;
    children->next = new;
}

void show(struct node *node, int depth) {
    if (node == NULL) return; 

    for (int i = 0; i < depth; i++) printf("..");

    if (node->token == NULL) 
        printf("%s\n", category_name[node->category]);
    else 
        printf("%s(%s)\n", category_name[node->category], node->token);

    struct node_list *child = node->children;
    while (child != NULL) {
        show(child->node, depth + 1);
        child = child->next; 
    }
}


void show_all(struct node *node, int depth) {
    if (node == NULL) return; 

    for (int i = 0; i < depth; i++) printf("..");

    if (node->token == NULL){
        if(node->print_type == 1) printf("%s - %s\n", category_name[node->category], type_name(node->type));
        else if(node->print_type == 2) printf("%s - (%s)\n", category_name[node->category], node->param_list);
        else printf("%s\n", category_name[node->category]);
    }
    else {
        if(node->print_type == 1) printf("%s(%s) - %s\n", category_name[node->category], node->token, type_name(node->type));
        else if(node->print_type == 2) printf("%s(%s) - (%s)\n", category_name[node->category], node->token, node->param_list);
        else printf("%s(%s)\n", category_name[node->category], node->token);
    }
    struct node_list *child = node->children;
    while (child != NULL) {
        show_all(child->node, depth + 1);
        child = child->next; 
    }
}


void delete (struct node *parent, struct node *child){
    if (child != NULL) {
        if (strcmp(category_name[child->category], "Delete") == 0) {
            struct node_list *delete_children = child->children;
            while (delete_children != NULL) {
                addchild(parent, delete_children->node);  // Adiciona cada filho de 'Delete' ao Program
                delete_children = delete_children->next;  // Avança para o próximo filho
            }
            free(child->children);
            free(child);
        } else if (child != NULL) {
            addchild(parent, child);
        }
    }
}

void libertaArvore(struct node *node) {
    if (node == NULL || node->freeNode) return;  // Caso base: Se o nó for NULL, nada precisa ser liberado
    
    node->freeNode = 1;

    // Itera sobre os filhos e libera-os recursivamente
    struct node_list *child = node->children;  // Ponteiro para a lista de filhos
    while (child != NULL) {
        libertaArvore(child->node);  // Chama recursivamente para liberar cada filho
        child = child->next;  // Avança para o próximo filho na lista
    }

    free(node->children);  // Libera a memória associada à lista de filhos
    free(node);  // Libera a memória associada ao próprio nó
}

// get a pointer to a specific child, numbered 0, 1, 2, ...
struct node *getchild(struct node *parent, int position) {
    // Verifica se o parent ou o parent->children são NULL
    if (parent == NULL || parent->children == NULL) {
        return NULL; // Se não houver filhos, retorna NULL
    }

    struct node_list *children = parent->children;
    int current_position = 0;

    // Percorre a lista de filhos
    while (children != NULL) {
        // Ignora filhos que não sejam válidos (node == NULL)
        if (children->node != NULL) {
            // Verifica a posição desejada
            if (current_position == position) {
                return children->node;  // Retorna o filho na posição indicada
            }
            current_position++;
        }
        // Avança para o próximo filho
        children = children->next;
    }

    // Se não encontrar o filho na posição dada, retorna NULL
    return NULL;
}
// count the children of a node
int countchildren(struct node *node) {
    int i = 0;
    while(getchild(node, i) != NULL)
        i++;
    return i;
}
