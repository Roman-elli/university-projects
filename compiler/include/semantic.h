#ifndef SEMANTIC_H
#define SEMANTIC_H

#include "functions.h"

#define MAX_LENGHT 15000
struct symbol_list {
	char *identifier;
	char *params;  
	enum type type;
	struct node *node;
	struct symbol_list *next;
};

struct symbol_table_list {
    struct symbol_list *table;
    struct symbol_table_list *next;
};

struct symbol_check_list{
	struct symbol_list *table;
	struct node *node;
	struct symbol_check_list *next;
};

struct parameter_list {
    char *token;
    struct parameter_list *next;
};

struct string_list {
	char *string_token;
	int length;
	struct string_list *next;
};


void check_all();
char* sanitize_string(const char *input);
int check_program(struct node *program);
void check_function(struct node *function);
void check_parameters(struct node *parameters, struct symbol_list *scope);
void check_expression(struct node *expression, struct symbol_list *scope);
void check_used(struct symbol_list *table);
void add_scope_to_table(struct symbol_list *scope);

struct symbol_list *insert_symbol(struct symbol_list *symbol_table, char *identifier, enum type type, struct node *node, int param_type);
struct symbol_list *insert_symbol_first(struct symbol_list *table, char *identifier, enum type type, struct node *node, int param_type);
struct symbol_list *search_symbol(char *identifier);
struct symbol_list *search_scope(struct symbol_list *scope, char *identifier);

void show_symbol_table(struct symbol_list *table, int global_table);
void show_all_symbol_tables();
#endif
