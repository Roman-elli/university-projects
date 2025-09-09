#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../include/functions.h"
#include "../../include/semantic.h"

int semantic_errors = 0;
int param_check = 0;
int strlit_counter = 0;
int length_string;
struct string_list *strings;
struct symbol_list *global_table;

struct symbol_table_list *symbol_tables;
struct error_list *list_error;
struct symbol_check_list *check_list;

extern char *category_name[];
char parametros[MAX_LENGHT];

int check_program(struct node *program) {
    if(program == NULL || program->children->next == NULL) return 0;
    global_table = (struct symbol_list *)malloc(sizeof(struct symbol_list));
    global_table->next = NULL;

    symbol_tables = NULL;

    check_list = NULL;

    list_error = NULL;

    strings = NULL;

    struct node_list *child = program->children->next;
    
    while ((child = child->next) != NULL){
        while(child->node == NULL) child = child->next; 
        check_function(child->node);
    }
    check_all();
    return semantic_errors;
}

void check_function(struct node *function) {
    if (strcmp(category_name[function->category], "FuncDecl") == 0) {
        struct node_list *child_header = function->children->next;
        struct node_list *child_func = function->children->next->next;
        int number_children = countchildren(child_header->node);
        int already_defined = 0;

        struct node *id_header = getchild(child_header->node, 0);

        if (strcmp(category_name[child_header->node->category], "FuncHeader") == 0) {
            if (search_symbol(id_header->token) == NULL) {
                getchild(child_header->node, 0)->isFunction = 1;
                if (number_children > 2) {
                    enum type type = category_type(getchild(child_header->node, 1)->category);
                    
                    insert_symbol(global_table, id_header->token, type, getchild(child_header->node, 0),0);
                } else {
                    insert_symbol(global_table, id_header->token, no_type, getchild(child_header->node, 0), 0);
                }
            } else {
                printf("Line %d, column %d: Symbol %s already defined\n",id_header->token_line, id_header->token_column, id_header->token);
                already_defined = 1;
                semantic_errors++;
            }
        }

        if(already_defined != 1){
            struct symbol_list *scope = (struct symbol_list *)malloc(sizeof(struct symbol_list));
            scope->next = NULL;
            scope->identifier = id_header->token;
            if(number_children > 2){
                scope->type = category_type(getchild(child_header->node, 1)->category);
            } else scope->type = no_type;
        
            parametros[0] = '\0';

            if (number_children > 2) {
                int check_number_params = countchildren(getchild(child_header->node, 2));
                if (check_number_params > 0 && already_defined == 0) {
                    check_parameters(getchild(child_header->node, 2), scope);
                }
            } else {
                int check_number_params = countchildren(getchild(child_header->node, 1));
                if (check_number_params > 0 && already_defined == 0) {
                    check_parameters(getchild(child_header->node, 1), scope);
                }
            }
            
            struct symbol_list *func_symbol = search_symbol(id_header->token);
            if (func_symbol != NULL) {
                func_symbol->params = strdup(parametros);
                scope->params = strdup(parametros);
            }
    
            struct symbol_check_list *new_check = (struct symbol_check_list *)malloc(sizeof(struct symbol_check_list));
            new_check->node = child_func->node;
            new_check->table = scope;
            new_check->next = NULL;

            if (check_list == NULL && already_defined == 0) {
                check_list = new_check;
            } else if(already_defined == 0){
                struct symbol_check_list *temp = check_list;
                while (temp->next != NULL) {
                    temp = temp->next;
                }
                temp->next = new_check;
            }
            
            add_scope_to_table(scope);
        }
    } else if(strcmp(category_name[function->category], "VarDecl") == 0){
        struct node *id_Var = getchild(function, 1);
        if (search_scope(global_table, id_Var->token) == NULL) {
                enum type type = category_type(getchild(function, 0)->category);
                id_Var->type = type;
                insert_symbol(global_table, id_Var->token, type, id_Var, 2);
                
            } else {
                printf("Line %d, column %d: Symbol %s already defined\n", id_Var->token_line, id_Var->token_column, id_Var->token);
                semantic_errors++;
            }
    }
}

void check_all() {
    struct symbol_check_list *temp = check_list;
    while (temp != NULL) {
        if (temp->node != NULL) {
            struct node_list *id_func = temp->node->children;
            while (id_func != NULL) {
                if (id_func->node != NULL) {
                    check_expression(id_func->node, temp->table);
                }
                id_func = id_func->next;
            }
            if (search_scope(temp->table, "return") == NULL) {
                insert_symbol_first(temp->table, "return", temp->table->type, newnode(Return, NULL), 0);
            }
            check_used(temp->table);
        }
        temp = temp->next;
    }
}

void check_parameters(struct node *parameters, struct symbol_list *scope) {
    struct node_list *parameter = parameters->children->next;
    struct parameter_list *tokens = NULL;  // Lista de tokens dos parâmetros

    parametros[0] = '\0';

    while (parameter != NULL) {
        enum type type = category_type(getchild(parameter->node, 0)->category);
        
        getchild(parameter->node, 1)->type = type;
        
        insert_symbol(scope, getchild(parameter->node, 1)->token, type, getchild(parameter->node, 1), 1);
        
        char type_str[15000];
        strcpy(type_str, type_name(type));

        struct parameter_list *current_token = tokens;
        while (current_token != NULL) {
            if(strcmp(current_token->token, getchild(parameter->node, 1)->token) == 0){
                printf("Line %d, column %d: Symbol %s already defined\n", getchild(parameter->node, 1)->token_line, getchild(parameter->node, 1)->token_column, current_token->token);
                semantic_errors++;
                break;
            }
            current_token = current_token->next;
        }

        if (parametros[0] != '\0') {
            strcat(parametros, ",");
        }
        strcat(parametros, type_str);
    
        struct parameter_list *new_token = (struct parameter_list *)malloc(sizeof(struct parameter_list));
        new_token->token = strdup(getchild(parameter->node, 1)->token);
        new_token->next = tokens;
        tokens = new_token;

        parameter = parameter->next;
    }

    while (tokens != NULL) {
        struct parameter_list *temp = tokens;
        tokens = tokens->next;
        free(temp->token);
        free(temp);
    }
}

void check_expression(struct node *semantic_category, struct symbol_list *scope) {
    char *operator;
    switch(semantic_category->category) {
        case Return:
            if(countchildren(semantic_category) == 0){
                insert_symbol_first(scope, "return", scope->type, semantic_category, 0);
                enum type type_funcao = search_scope(global_table, scope->identifier)->type;
                if(type_funcao != no_type){
                    printf("Line %d, column %d: Incompatible type void in return statement\n", semantic_category->token_line, semantic_category->token_column);
                    semantic_errors++;
                }
            }
            else {
                check_expression(getchild(semantic_category, 0),scope);
                enum type type = getchild(semantic_category,0)->type;
                enum type type_funcao = search_scope(global_table, scope->identifier)->type;
                if(type != type_funcao){
                    printf("Line %d, column %d: Incompatible type %s in return statement\n", semantic_category->token_line, getchild(semantic_category,0)->token_column, type_name(type));
                    semantic_errors++;
                }
                insert_symbol_first(scope, "return", type_funcao, semantic_category, 0);
            }
            break;
        case VarDecl:
            if (search_scope(scope, getchild(semantic_category, 1)->token) == NULL) {
                    getchild(semantic_category, 1)->type_param = 0;
                    enum type type = category_type(getchild(semantic_category, 0)->category);
                    getchild(semantic_category, 1)->type = type;
                    insert_symbol(scope, getchild(semantic_category, 1)->token, type, getchild(semantic_category, 1), 0);
                    getchild(semantic_category, 1)->used = 1;
                } else {
                    printf("Line %d, column %d: Symbol %s already defined\n",getchild(semantic_category, 1)->token_line, getchild(semantic_category, 1)->token_column, getchild(semantic_category, 1)->token);
                    semantic_errors++;
                }
            break;
        case Identifier:   
            if(search_scope(scope, semantic_category->token) == NULL && search_scope(global_table, semantic_category->token) == NULL) {
                printf("Line %d, column %d: Cannot find symbol %s\n", semantic_category->token_line, semantic_category->token_column, semantic_category->token);
                semantic_category->type = undefined;
                semantic_category->used = 0;
                semantic_category->print_type = 1;
                semantic_errors++;
            } else if(search_scope(scope, semantic_category->token) != NULL){
                semantic_category->type = search_scope(scope, semantic_category->token)->node->type;
                semantic_category->print_type = 1;
                semantic_category->used = 0;
                search_scope(scope, semantic_category->token)->node->used = 0;
            } else if(search_scope(global_table, semantic_category->token) != NULL){
                if(search_scope(global_table, semantic_category->token)->node->isFunction == 1){
                    semantic_category->type = undefined;
                    semantic_category->print_type = 1;
                    search_scope(global_table, semantic_category->token)->node->type = undefined;
                    printf("Line %d, column %d: Cannot find symbol %s\n", semantic_category->token_line, semantic_category->token_column, semantic_category->token);
                }
                else semantic_category->type = search_scope(global_table, semantic_category->token)->node->type;
                semantic_category->print_type = 1;
                semantic_category->used = 0;
                search_scope(global_table, semantic_category->token)->node->used = 0;
            }
            break;
        case For:
            check_expression(getchild(semantic_category,0), scope);
            if(countchildren(semantic_category) > 1) check_expression(getchild(semantic_category,1), scope);
            if(getchild(semantic_category, 0)->type != boolean_type && getchild(semantic_category, 0)->category != Block){
                printf("Line %d, column %d: Incompatible type %s in for statement\n", semantic_category->token_line, getchild(semantic_category, 0)->token_column, type_name(getchild(semantic_category, 0)->type));
                semantic_errors++;
            }
  
            break;
        case Natural:
            semantic_category->print_type = 1;
            semantic_category->type = integer_type;
            semantic_category->used = 0;
            break;
        case Decimal:
            semantic_category->print_type = 1;
            semantic_category->type = float_type;
            semantic_category->used = 0;
            break;
        case StrLit:
            semantic_category->print_type = 1;
            semantic_category->type = string_type;
            semantic_category->used = 0;
            length_string = 0;
            char *sanitized_str = sanitize_string(semantic_category->token);
            length_string += strlen(sanitized_str) + 2;

            char *string_declaration = (char *)malloc(strlen(sanitized_str) + 500);
            sprintf(string_declaration, "@print.strlit%d = private constant [%d x i8] c\"%s\\0A\\00\"\n", strlit_counter, length_string, sanitized_str);
            strlit_counter++;
            if(strlen(semantic_category->token) == 0) strlit_counter = 0;
            if (strings == NULL) {
                strings = (struct string_list *)malloc(sizeof(struct string_list));
                strings->length = length_string;
                strings->string_token = (char *)malloc(strlen(string_declaration) + 1);
                
                strcpy(strings->string_token, string_declaration);
                strings->next = NULL;
            } else {
                struct string_list *temp = strings;
                while (temp->next != NULL) {
                    temp = temp->next;
                }

                struct string_list *new_node = (struct string_list *)malloc(sizeof(struct string_list));
                new_node->length = length_string;

                new_node->string_token = (char *)malloc(strlen(string_declaration) + 1);

                strcpy(new_node->string_token, string_declaration);
                new_node->next = NULL;

                temp->next = new_node;
            }
            free(string_declaration);
            break;
        case String:
            semantic_category->type = string_type;
            semantic_category->used = 0;
            break;
        case Float32:
            semantic_category->print_type = 1;
            semantic_category->type = float_type;
            semantic_category->used = 0;
            break;
        case Print:
            check_expression(getchild(semantic_category,0), scope);
            if(getchild(semantic_category, 0)->type == undefined){
                printf("Line %d, column %d: Incompatible type %s in fmt.Println statement\n", semantic_category->token_line, getchild(semantic_category, 0)->token_column, type_name(getchild(semantic_category, 0)->type));
                semantic_category->type = boolean_type;
                semantic_errors++;
            }
            break;
        case Plus:
            check_expression(getchild(semantic_category,0), scope);
            semantic_category->print_type = 1;
            semantic_category->type = getchild(semantic_category,0)->type;
            if(getchild(semantic_category, 0)->type == undefined){
                printf("Line %d, column %d: Operator + cannot be applied to type %s\n", semantic_category->token_line, semantic_category->token_column, type_name(getchild(semantic_category, 0)->type));
                
                semantic_errors++;
            }
            break;
        case Minus:
            check_expression(getchild(semantic_category,0), scope);
            semantic_category->print_type = 1;
            semantic_category->type = getchild(semantic_category,0)->type;
            if(getchild(semantic_category, 0)->type == undefined){
                printf("Line %d, column %d: Operator - cannot be applied to type %s\n", semantic_category->token_line, semantic_category->token_column, type_name(getchild(semantic_category, 0)->type));
                
                semantic_errors++;
            }
            break;
        case Not:
            check_expression(getchild(semantic_category,0), scope);
            if(getchild(semantic_category, 0)->type != boolean_type){
                printf("Line %d, column %d: Operator ! cannot be applied to type %s\n", semantic_category->token_line, semantic_category->token_column, type_name(getchild(semantic_category, 0)->type));
                semantic_category->type = boolean_type;
                semantic_errors++;
            }
            else semantic_category->type = getchild(semantic_category,0)->type;
            semantic_category->print_type = 1;
            break;
        case Call:
        if (search_scope(global_table, getchild(semantic_category, 0)->token) != NULL) {
            if (search_scope(global_table, getchild(semantic_category, 0)->token)->type != no_type) {
                semantic_category->print_type = 1;
                semantic_category->type = search_scope(global_table, getchild(semantic_category, 0)->token)->type;
            }

            getchild(semantic_category, 0)->print_type = 2;

            if (countchildren(semantic_category) > 1) {
                int x = 1;
                struct node* argument;
                while (getchild(semantic_category, x) != NULL) {
                    argument = getchild(semantic_category, x);
                    check_expression(argument, scope);

                    char type_str[15000];
                    if (argument->type == void_type) argument->type = no_type;

                    strcpy(type_str, type_name(argument->type));

                    if (strlen(getchild(semantic_category, 0)->param_list) + strlen(type_str) + 1 < sizeof(getchild(semantic_category, 0)->param_list)) {
                        if (getchild(semantic_category, 0)->param_list[0] != '\0') {
                            strcat(getchild(semantic_category, 0)->param_list, ",");
                        }

                        strcat(getchild(semantic_category, 0)->param_list, type_str);
                    } 
                    x++;
                }
            }
            if (strcmp(search_scope(global_table, getchild(semantic_category, 0)->token)->params, getchild(semantic_category, 0)->param_list) != 0) {
                printf("Line %d, column %d: Cannot find symbol %s(%s)\n", semantic_category->token_line, semantic_category->token_column, getchild(semantic_category, 0)->token, getchild(semantic_category, 0)->param_list);
                semantic_category->type = undefined;
                semantic_category->print_type = 1;
                getchild(semantic_category, 0)->type = undefined;
                getchild(semantic_category, 0)->print_type = 1;
                semantic_errors++;
            }
        }else {
            getchild(semantic_category, 0)->print_type = 2;
            if (countchildren(semantic_category) > 1) {
                int x = 1;
                struct node* argument;
                while (getchild(semantic_category, x) != NULL) {
                    argument = getchild(semantic_category, x);
                    check_expression(argument, scope);

                    char type_str[15000];
                    if (argument->type == void_type) argument->type = no_type;

                    strcpy(type_str, type_name(argument->type));

                    if (strlen(getchild(semantic_category, 0)->param_list) + strlen(type_str) + 1 < sizeof(getchild(semantic_category, 0)->param_list)) {
                        if (getchild(semantic_category, 0)->param_list[0] != '\0') {
                            strcat(getchild(semantic_category, 0)->param_list, ",");
                        }

                        strcat(getchild(semantic_category, 0)->param_list, type_str);
                    }
                    x++;
                }
            }
            printf("Line %d, column %d: Cannot find symbol %s(%s)\n", semantic_category->token_line, semantic_category->token_column, getchild(semantic_category, 0)->token, getchild(semantic_category, 0)->param_list);
            getchild(semantic_category, 0)->type = undefined;
            getchild(semantic_category, 0)->print_type = 1;
            semantic_category->type = undefined;
            semantic_category->print_type = 1;
            semantic_errors++;
        }
        break;
        case Block:
            if(countchildren(semantic_category) == 0) semantic_category->type = no_type;
            else{
                struct node_list *block_child = semantic_category->children;
                    while((block_child = block_child->next) != NULL){
                        while(block_child->node == NULL || block_child == NULL) block_child = block_child->next; 
                        check_expression(block_child->node, scope);
                    }
            }
            break;
        case If:
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);
            check_expression(getchild(semantic_category, 2), scope);
            if(getchild(semantic_category, 0)->type != boolean_type){
                printf("Line %d, column %d: Incompatible type %s in if statement\n", getchild(semantic_category, 0)->token_line, getchild(semantic_category, 0)->token_column, type_name(getchild(semantic_category, 0)->type));
                
                semantic_errors++;
            }
            break;
        case Lt:
        case Le:
        case Ge:
        case Gt:
            switch(semantic_category->category){
                case Lt: operator = "<";
                    break;
                case Le: operator = "<=";
                    break;
                case Gt: operator = ">";
                    break;
                case Ge: operator = ">=";
                    break;
                default: break;
            }
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);

                       
            if(getchild(semantic_category, 0)->type == boolean_type || getchild(semantic_category, 1)->type == boolean_type || getchild(semantic_category, 0)->type == undefined || getchild(semantic_category, 1)->type == undefined || (getchild(semantic_category, 0)->type == integer_type && getchild(semantic_category, 1)->type == float_type) || (getchild(semantic_category, 0)->type == float_type && getchild(semantic_category, 1)->type == integer_type)){
                printf("Line %d, column %d: Operator %s cannot be applied to types %s, %s\n", semantic_category->token_line, semantic_category->token_column, operator, type_name(getchild(semantic_category, 0)->type), type_name(getchild(semantic_category, 1)->type));
                semantic_errors++;
            }
            semantic_category->type = boolean_type; 
            semantic_category->print_type = 1;

            break;
        case And:
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);
            if (getchild(semantic_category, 0)->type != boolean_type || getchild(semantic_category, 1)->type != boolean_type){
                printf("Line %d, column %d: Operator && cannot be applied to types %s, %s\n",semantic_category->token_line, semantic_category->token_column, type_name(getchild(semantic_category, 0)->type), type_name(getchild(semantic_category, 1)->type));
                semantic_errors++;
            }
            semantic_category->type = boolean_type; 
            semantic_category->print_type = 1;
   
        break;
        case Or:
        case Eq:
        case Ne:
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);
            semantic_category->type = boolean_type; 
            semantic_category->print_type = 1;
        break;
        case ParseArgs:
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);
            if((getchild(semantic_category, 0)->type || getchild(semantic_category, 1)->type) != integer_type){
                printf("Line %d, column %d: Operator strconv.Atoi cannot be applied to types %s, %s\n",semantic_category->token_line, semantic_category->token_column, type_name(getchild(semantic_category, 0)->type), type_name(getchild(semantic_category, 1)->type));
                semantic_category->type = undefined;
                semantic_errors++;
            }
            semantic_category->type = getchild(semantic_category, 1)->type; 
            semantic_category->print_type = 1;
            break;
        case Assign:
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);
            
            if((getchild(semantic_category, 0)->type != getchild(semantic_category, 1)->type) || getchild(semantic_category, 0)->type == undefined || getchild(semantic_category, 1)->type == undefined){
                printf("Line %d, column %d: Operator = cannot be applied to types %s, %s\n",semantic_category->token_line, semantic_category->token_column, type_name(getchild(semantic_category, 0)->type), type_name(getchild(semantic_category, 1)->type));
                semantic_errors++;
            } 
            if(getchild(semantic_category, 0)->category == Identifier && search_scope(scope, getchild(semantic_category,0)->token) != NULL) search_scope(scope, getchild(semantic_category,0)->token)->node->used = 0;
            if(getchild(semantic_category, 1)->category == Identifier && search_scope(scope, getchild(semantic_category,1)->token) != NULL) search_scope(scope, getchild(semantic_category,1)->token)->node->used = 0;
            
            semantic_category->type = getchild(semantic_category, 0)->type; 
            semantic_category->print_type = 1;
        break;
        case Add:
        case Sub:
        case Mul:
        case Div:
        case Mod:
            switch(semantic_category->category){
                case Add: operator = "+";
                    break;
                case Sub: operator = "-";
                    break;
                case Mul: operator = "*";
                    break;
                case Div: operator = "/";
                    break;
                case Mod: operator = "%";
                    break;
                default: break;
            }
            check_expression(getchild(semantic_category, 0), scope);
            check_expression(getchild(semantic_category, 1), scope);            

            if  ( (getchild(semantic_category, 0)->type != getchild(semantic_category, 1)->type) || 
                (getchild(semantic_category, 0)->type == boolean_type) || (getchild(semantic_category, 1)->type == boolean_type) || 
                ( (getchild(semantic_category, 0)->type == undefined) || (getchild(semantic_category, 1)->type == undefined))){                
                    printf("Line %d, column %d: Operator %s cannot be applied to types %s, %s\n",semantic_category->token_line, semantic_category->token_column, operator, type_name(getchild(semantic_category, 0)->type), type_name(getchild(semantic_category, 1)->type));
                    semantic_category->type = undefined;
                    semantic_category->print_type = 1;
                    semantic_errors++;
            }
            else{
                semantic_category->type = getchild(semantic_category, 0)->type; 
                semantic_category->print_type = 1;
            }
            break;
        default:
            break;
    }
}

char* sanitize_string(const char *input) {
    size_t length = strlen(input);
    char *output = malloc(length * 4 + 1); 
    char *ptr = output;
    int bar_print = 0;

    for (size_t i = 1; i < length-1; i++) {
        switch (input[i]) {
            case 'n':
                if(bar_print == 1){
                *ptr++ = '0';
                *ptr++ = 'A';
                bar_print = 0;
                length_string-=2;
                } else *ptr++ = input[i];
                break;
            case 'r':
                if(bar_print == 1){
                    *ptr++ = '0';
                    *ptr++ = 'D';
                    length_string-=2;
                    bar_print = 0;
                } else *ptr++ = input[i];
                break;
            case 't':
                if(bar_print == 1){
                *ptr++ = '0';
                *ptr++ = '9';
                length_string-=2;
                bar_print = 0;
                } else *ptr++ = input[i];
                break;
            case 'b':
                if(bar_print == 1){
                *ptr++ = '0';
                *ptr++ = '8';
                bar_print = 0;
                length_string-=2;
                } else *ptr++ = input[i];
                break;
            case 'f':
                if(bar_print == 1){
                *ptr++ = '0';
                *ptr++ = 'C';
                bar_print = 0;
                length_string-=2;
                } else *ptr++ = input[i];
                break;
            case '\\':
                *ptr++ = '\\';
                if(input[i+1] == '\\' && bar_print == 1) length_string--;
                if(input[i+1] == '\\' && input[i+2] == '\\' && bar_print == 1) length_string++;
                if(bar_print != 1) bar_print = 1;
                break;
            case '\"':
                if(bar_print == 1){
                *ptr++ = '2';
                *ptr++ = '2';
                bar_print = 0;
                length_string -= 2;
                } else *ptr++ = input[i];
                break;

            case '%':
                *ptr++ = '%';
                *ptr++ = '%';
            break;
            case '\0':
                if(bar_print == 1){
                *ptr++ = '0';
                *ptr++ = '0';
                bar_print = 0;
                } else *ptr++ = input[i];
                break;
            default:
                *ptr++ = input[i];
                if (bar_print == 1) length_string--;
                bar_print = 0;
                break;
        }
    }
    if(bar_print == 1){
        length_string--;
        bar_print = 0;
    }

    *ptr = '\0';
    return output;
}

void check_used(struct symbol_list *table) {
    struct symbol_list *symbol = table;

    while (symbol != NULL) {
        if (symbol->node != NULL) {
            if (symbol->node->used == 1) {
                printf("Line %d, column %d: Symbol %s declared but never used\n", symbol->node->token_line, symbol->node->token_column, symbol->node->token);
                semantic_errors++;
            }
        }

        symbol = symbol->next;
    }
}

struct symbol_list *insert_symbol(struct symbol_list *table, char *identifier, enum type type, struct node *node, int param_type) {
    struct symbol_list *new = (struct symbol_list *)malloc(sizeof(struct symbol_list));
    new->identifier = strdup(identifier);
    new->type = type;
    new->node = node;
    new->node->type_param = param_type;
    new->params = strdup("");
    new->next = NULL;
    
    struct symbol_list *symbol = table;
    while (symbol != NULL) {
        if (symbol->next == NULL) {
            symbol->next = new;
            break;
        } else if (strcmp(symbol->next->identifier, identifier) == 0) {
            free(new);
            return NULL;
        }
        symbol = symbol->next;
    }
    return new;
}

struct symbol_list *insert_symbol_first(struct symbol_list *table, char *identifier, enum type type, struct node *node, int param_type) {
    struct symbol_list *new = (struct symbol_list *)malloc(sizeof(struct symbol_list));
    new->identifier = strdup(identifier);
    new->type = type;
    new->node = node;
    new->node->type_param = param_type;
    new->params = strdup("");
    new->next = NULL;

    struct symbol_list *symbol = table;
    while (symbol != NULL) {
        if (strcmp(symbol->identifier, identifier) == 0) {
            free(new);
            return NULL;
        }
        symbol = symbol->next;
    }
    
    new->next = table->next;
    table->next = new;
    
    return new;
}

struct symbol_list *search_scope(struct symbol_list *scope, char *identifier) {
    struct symbol_list *symbol;
    for (symbol = scope->next; symbol != NULL; symbol = symbol->next) {
        if (strcmp(symbol->identifier, identifier) == 0) {
            return symbol;
        }
    }
    return NULL;
}

struct symbol_list *search_symbol(char *identifier) {
    struct symbol_list *symbol;
    for (symbol = global_table->next; symbol != NULL; symbol = symbol->next) {
        if (strcmp(symbol->identifier, identifier) == 0) {
            return symbol;
        }
    }

    struct symbol_table_list *current_scope = symbol_tables;
    while (current_scope != NULL) {
        for (symbol = current_scope->table; symbol != NULL; symbol = symbol->next) {
            if (strcmp(symbol->identifier, identifier) == 0) {
                return symbol;
            }
        }
        current_scope = current_scope->next;
    }

    return NULL;
}

void add_scope_to_table(struct symbol_list *scope) {
    struct symbol_table_list *new_scope = (struct symbol_table_list *)malloc(sizeof(struct symbol_table_list));
    new_scope->table = scope;
    new_scope->next = NULL;

    if (symbol_tables == NULL) {
        symbol_tables = new_scope;
    } else {
        struct symbol_table_list *current = symbol_tables;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_scope;
    }
}

void show_all_symbol_tables() {
    struct symbol_table_list *current_table = symbol_tables;
    
    printf("===== Global Symbol Table =====\n");
    show_symbol_table(global_table,1);
    
    while (current_table != NULL) {
        printf("===== Function %s(%s) Symbol Table =====\n", current_table->table->identifier, current_table->table->params);
        show_symbol_table(current_table->table,2);
        current_table = current_table->next;
    }
}

void show_symbol_table(struct symbol_list *table, int global_table) {
    struct symbol_list *symbol;
    if(global_table == 1){
        for (symbol = table->next; symbol != NULL; symbol = symbol->next) {
            if(symbol->node->type_param == 2) printf("%s\t\t%s\n", symbol->identifier, type_name(symbol->type));
            else printf("%s\t(%s)\t%s\n", symbol->identifier, symbol->params, type_name(symbol->type));
        }
    }else{
        for (symbol = table->next; symbol != NULL; symbol = symbol->next) {
            if(symbol->node->type_param == 1){
                printf("%s\t%s\t%s\tparam\n", symbol->identifier, symbol->params, type_name(symbol->type));
            }else printf("%s\t%s\t%s\n", symbol->identifier, symbol->params, type_name(symbol->type));
        }
    }
    printf("\n");
}
