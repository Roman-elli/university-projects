#ifndef _CODEGEN_H
#define _CODEGEN_H

#include "functions.h"

void codegen_program(struct node *program);
void codegen_parameters(struct node *parameters);
int codegen_expression(struct node *expression, struct node *func_header);
int codegen_function(struct node *function);
int codegen_print(struct node *expression, struct node *func_header);

struct param_define {
    char* define_param;
    struct param_define *next;
};

struct symbol_list *search_table (char *expression_value, char *identifier);
#endif