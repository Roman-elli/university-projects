#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "functions.h"
#include "semantic.h"
#include "codegen.h"

int temporary;   // sequence of temporary registers in a function
int for_counter = 0;
int if_counter = 0;
int string_counter = 0;
extern char *category_name[];
extern struct symbol_list *global_table;
extern struct symbol_table_list *symbol_tables;
extern struct string_list *strings;
struct param_define *list_param;


void codegen_program(struct node *program) {
    if(program == NULL || program->children->next == NULL){ 
        printf("define i32 @main() {\n"
           "  ret i32 0\n"
           "}\n");
    }else{
        // Predeclaração de funções I/O
        printf("declare i32 @_read(i32)\n");
        printf("declare i32 @_write(i32)\n");
        printf("declare i32 @printf(i8*, ...)\n");

        printf("@print.int = private constant [4 x i8] c\"%%d\\0A\\00\"\n");
        printf("@print.float = private constant [7 x i8] c\"%%.08f\\0A\\00\"\n");
        printf("@print.true = private constant [6 x i8] c\"true\\0A\\00\"\n");
        printf("@print.false = private constant [7 x i8] c\"false\\0A\\00\"\n");
        printf("@print.string = private constant [4 x i8] c\"%%s\\0A\\00\"\n");

        struct string_list *temp = strings;
        while(temp != NULL){
            printf("%s", temp->string_token);
            temp = temp->next;
        }
        printf("\n");

        list_param = NULL;
    
        // Geração de funções
        struct node_list *function = program->children->next;
        while ((function = function->next) != NULL) {
            if (function->node != NULL) {
                codegen_function(function->node);
            }
        }

        // Gerar ponto de entrada
        struct symbol_list *entry = search_scope(global_table, "main");
        if(entry != NULL && entry->node->isFunction == 1)
            printf("define i32 @main() {\n"
                "  %%1 = call i32 @_main()\n"
            "  ret i32 %%1\n"
            "}\n");
    }
}

int codegen_function(struct node *function) {
    temporary = 1;
    if (strcmp(category_name[function->category], "FuncDecl") == 0) {
        // Cabeçalho e corpo da função
        struct node_list *child_header = function->children->next;
        struct node_list *child_func = function->children->next->next;
        int number_children = countchildren(child_header->node);
        
        // Nome da função
        struct node *id_header = getchild(child_header->node, 0);
        const char *func_name = id_header->token;

        // Inicializando geração do cabeçalho
        printf("define i32 @_%s(", func_name);

        // Gerar parâmetros da função
        if (strcmp(category_name[child_header->node->category], "FuncHeader") == 0) {
            if (number_children > 2) {
            int check_number_params = countchildren(getchild(child_header->node, 2));
            if (check_number_params > 0) {
                codegen_parameters(getchild(child_header->node, 2));
            }
        } else {
            int check_number_params = countchildren(getchild(child_header->node, 1));
            if (check_number_params > 0) {
                // Verifica e processa os parâmetros da função
                codegen_parameters(getchild(child_header->node, 1));
            }
        }
        }
        printf(") {\n");

        struct param_define *current = list_param;
        while (current != NULL) {
            printf("%s\n", current->define_param);  // Imprime a string do parâmetro
            current = current->next;  // Vai para o próximo nó
        }
        
        struct node_list *func = child_func->node->children;  // Obtenha os filhos do nó
        while (func != NULL) {  // Percorra a lista de filhos de 'temp->node'
            if (func->node != NULL) {  // Verifique se o nó de 'id_func' não é nulo
                codegen_expression(func->node, id_header);  // Chame a função para verificar a expressão
                }
            func = func->next;  // Avance para o próximo nó da lista de filhos
        }

        if(search_scope(global_table, id_header->token)->type == no_type){
            printf("  ret i32 0\n");
        }

        printf("}\n\n");
        
        return temporary;
    }
    return -1; // Caso não seja uma função válida
}

int codegen_natural(struct node *natural, struct node *func_header) {
    printf("  %%%d = add i32 %s, 0\n", temporary, natural->token);
    return temporary++;
}

int codegen_identifier(struct node *n, struct node *func_header) {
    switch(n->type){
        case integer_type:
            printf("  %%%d = load i32, i32* %%%s\n", temporary, n->token); 
        break;
        case float_type:
        case double_type:
            printf("  %%%d = load double, double* %%%s\n", temporary, n->token); 
        break;
        case boolean_type:
            printf("  %%%d = load i1, i1* %%%s\n", temporary, n->token); 
        default:
        break;
    }
    return temporary++;
}

int codegen_mul(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    printf("  %%%d = mul i32 %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_add(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    printf("  %%%d = add i32 %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_sub(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    
    if(expression->type == float_type){
        printf("  %%%d = sub double %%%d, %%%d\n", temporary, t1, t2); // Negar o valor (0 - valor)
    }
    else printf("  %%%d = sub i32 %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_div(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    printf("  %%%d = sdiv i32 %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_mod(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    printf("  %%%d = smod i32 %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_call(struct node *call, struct node *func_header) {
    struct node *func_name_node = getchild(call, 0);
    struct node *args_node = getchild(call, 1);

    // Gere código para os argumentos
    int arg_count = 0;
    struct node *argument;
    while ((argument = getchild(args_node, arg_count)) != NULL) {
        int arg_tmp = codegen_expression(argument, func_header);
        arg_count++;
        printf("  %%%d = call i32 @_%s(i32 %%%d)\n", temporary, func_name_node->token, arg_tmp);
    }
    return temporary++;
}

int codegen_if_then_else(struct node *expression, struct node *func_header) {
    if_counter++;
    struct node *condition = getchild(expression, 0);
    struct node *then_branch = getchild(expression, 1);
    struct node *else_branch = getchild(expression, 2);
    
    // Gerar labels dinâmicas com base no if_counter
    char then_label[50], else_label[50], end_label[50];
    sprintf(then_label, "L%dthen", if_counter);  // Exemplo: L0then
    sprintf(else_label, "L%delse", if_counter);  // Exemplo: L0else
    sprintf(end_label, "L%dend", if_counter);    // Exemplo: L0end
    // Avaliar a condição
    int cond_temp = codegen_expression(condition, func_header);

    if (condition->category == Identifier) {
        if(condition->type == boolean_type){    
            // Se for um identifier, gerar a comparação com 0
            printf("  %%%d = xor i1 %%%d, true\n", temporary, cond_temp); // XOR com true inverte o valor
            int not_temp = temporary++;  // Registrar o resultado do icmp
            printf("  br i1 %%%d, label %%%s, label %%%s\n", not_temp, then_label, else_label); // Condicional com o resultado do icmp
        } else if(condition->type == integer_type){
            // Se for um identifier, gerar a comparação com 0
            printf("  %%%d = icmp ne i32 %%%d, 0\n", temporary, cond_temp);  // Comparar com 0
            int icmp_temp = temporary++;  // Registrar o resultado do icmp
            printf("  br i1 %%%d, label %%%s, label %%%s\n", icmp_temp, then_label, else_label); // Condicional com o resultado do icmp
        } else{
            // Se for um identifier, gerar a comparação com 0
            printf("  %%%d = icmp ne double %%%d, 0\n", temporary, cond_temp);  // Comparar com 0
            int icmp_temp = temporary++;  // Registrar o resultado do icmp
            printf("  br i1 %%%d, label %%%s, label %%%s\n", icmp_temp, then_label, else_label); // Condicional com o resultado do icmp
        }
    } else {
        // Caso a condição não seja um identifier, você pode tratar de outra maneira, ou simplesmente pular essa parte
        printf("  br i1 %%%d, label %%%s, label %%%s\n", cond_temp, then_label, else_label); // Usando o valor retornado da expressão
    }

    printf("%s:\n", then_label);
    codegen_expression(then_branch, func_header);

    printf("  br label %%%s\n", end_label);

    printf("%s:\n", else_label);
    codegen_expression(else_branch, func_header);

    //printf("  store i32 %%%d, i32* %%1\n", else_temp);
    printf("  br label %%%s\n", end_label);

    printf("%s:\n", end_label);
    if(countchildren(condition) > 0){
        if(getchild(condition,0)->type == integer_type) printf("  %%%d = load i32, i32* %%%s\n", temporary, getchild(condition, 0)->token);
    } 
    else {
        printf("  %%%d = load i1, i1* %%%s\n", temporary, condition->token);
    }
    return temporary++;
}

int codegen_lt(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = icmp slt i32 %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    else{
        printf("  %%%d = fcmp olt double %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    return temporary++;
}

int codegen_and(struct node *expression, struct node *func_header) {
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = and i32 %%%d, %%%d\n", temporary, t1, t2);
    }else if(getchild(expression, 0)->type == boolean_type){
        printf("  %%%d = and i1 %%%d, %%%d\n", temporary, t1, t2);
    } else printf("  %%%d = and double %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_decimal(struct node *decimal, struct node *func_header) {
    // Converte o token para um número de ponto flutuante
    double value = atof(decimal->token);  // Converte a string para double
    printf("  %%%d = fadd double %f, 0.0\n", temporary, value);
    
    return temporary++;
}

int codegen_le(struct node *expression, struct node *func_header) {
    // Geração de código para menor ou igual
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);
    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = icmp sle i32 %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    else {
        printf("  %%%d = icmp sle double %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    return temporary++;
}

int codegen_ge(struct node *expression, struct node *func_header) {
    // Geração de código para maior ou igual
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);

    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = icmp sge i32 %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    else {
        printf("  %%%d = icmp sge double %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }

    return temporary++;
}

int codegen_gt(struct node *expression, struct node *func_header) {
    // Geração de código para maior que
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);

    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = icmp sgt i32 %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    else{
        printf("  %%%d = icmp sgt double %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }

    return temporary++;
}

int codegen_or(struct node *expression, struct node *func_header) {
    // Geração de código para OR lógico
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);

    printf("  %%%d = or i1 %%%d, %%%d\n", temporary, t1, t2);
    return temporary++;
}

int codegen_eq(struct node *expression, struct node *func_header) {
    // Geração de código para igualdade
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);


    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = icmp eq i32 %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    else{
        printf("  %%%d = icmp eq double %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }

    return temporary++;
}

int codegen_ne(struct node *expression, struct node *func_header) {
    // Geração de código para desigualdade
    int t1 = codegen_expression(getchild(expression, 0), func_header);
    int t2 = codegen_expression(getchild(expression, 1), func_header);

    if(getchild(expression, 0)->type == integer_type){
        printf("  %%%d = icmp ne i32 %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    else{
        printf("  %%%d = icmp ne double %%%d, %%%d\n", temporary, t1, t2); // slt: signed less than
    }
    return temporary++;
}

int codegen_parseargs(struct node *expression, struct node *func_header) {
    // Geração de código para parsing de argumentos
    printf("  %%%d = call i32 @parseargs(i32* %s)\n", temporary, expression->token); // Supondo função parseargs
    return temporary++;
}

int codegen_assign(struct node *expression, struct node *func_header) {
    // Geração de código para atribuição
    int value = codegen_expression(getchild(expression, 1), func_header);

    switch(expression->type){
        case float_type:
        case double_type:
            printf("  store double %%%d, double* %%%s\n", value, getchild(expression, 0)->token);
        break;
        case integer_type:
            printf("  store i32 %%%d, i32* %%%s\n", value, getchild(expression, 0)->token);
        break;
        case boolean_type:
            printf("  store i1 %%%d, i1* %%%s\n", value, getchild(expression, 0)->token);
        break;
        default:
        break;
    }
    
    return temporary;
}
int codegen_for(struct node *expression, struct node *func_header) {
    for_counter++;
    char looplabel[50], bodylabel[50], endlabel[50];
    sprintf(looplabel, "looplabel_%d", for_counter);  // Ex: looplabel_0
    sprintf(bodylabel, "bodylabel_%d", for_counter);  // Ex: bodylabel_0
    sprintf(endlabel, "endlabel_%d", for_counter);    // Ex: endlabel_0

    struct node *condition = getchild(expression, 0);  // Condição do loop
    struct node *body = getchild(expression, 1);  // Corpo do loop

    printf("  br label %%%s\n", looplabel);
    // Gera o rótulo do início do loop
    printf("%s:\n", looplabel);

    // Gera o código para avaliar a condição do loop
    int cond_temp = codegen_expression(condition, func_header);  // Avaliar a condição
   
    // Gera o salto baseado no valor da condição
    printf("  br i1 %%%d, label %%%s, label %%%s\n", cond_temp, bodylabel, endlabel);

    // Rótulo do corpo do loop
    printf("%s:\n", bodylabel);

    // Gera o código para o corpo do loop
    codegen_expression(body, func_header);  // Executar o corpo do loop

    // Gera o salto de volta ao início do loop
    printf("  br label %%%s\n", looplabel);

    // Rótulo de término do loop
    printf("%s:\n", endlabel);

    // Retorna o valor da próxima variável temporária
    return temporary;
}

int codegen_block(struct node *expression, struct node *func_header) {
    if(countchildren(expression) == 0) expression->type = no_type;
    else{
        struct node_list *child = expression->children;
        while((child = child->next) != NULL){
            while(child->node == NULL || child == NULL) child = child->next;
            codegen_expression(child->node, func_header);
            }
        }
    return -1; // Blocos geralmente não retornam valores
}


int codegen_print(struct node *expression, struct node *func_header) {
    struct node *child = getchild(expression, 0); 
    int value = codegen_expression(child, func_header);  // Código do valor a ser impresso
    int x;
    struct string_list *temp;
    switch (child->category) {

         case Minus:
            if(child->type == float_type){
                printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([7 x i8], [7 x i8]* @print.float, i32 0, i32 0), double %%%d)\n", temporary, value);
            } else printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([4 x i8], [4 x i8]* @print.int, i32 0, i32 0), i32 %%%d)\n",temporary, value);
         break;
        case Identifier:
            // Imprime booleano como "true" ou "false"
            switch(child->type){
                case integer_type:
                    printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([4 x i8], [4 x i8]* @print.int, i32 0, i32 0), i32 %%%d)\n",temporary, value);
                break;
                case double_type:
                case float_type:
                    printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([7 x i8], [7 x i8]* @print.float, i32 0, i32 0), double %%%d)\n",temporary, value);
                break;
                case boolean_type:
                    printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([5 x i8], [5 x i8]* @print.bool, i32 0, i32 0), i1 %%%d)\n", temporary, value);
                break;
                default:
                break;
            }
            break;
        case Bool:
    
        // Se for verdadeiro (1), imprime "true"
        if (value) {
            printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([5 x i8], [5 x i8]* @print.bool, i32 0, i32 0), i1 1)\n", temporary);
        }
        // Se for falso (0), imprime "false"
        else {
            printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([6 x i8], [6 x i8]* @print.bool, i32 0, i32 0), i1 0)\n", temporary);
        }
        break;
        case Natural:
            // Imprime valor inteiro (i32)
            printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([4 x i8], [4 x i8]* @print.int, i32 0, i32 0), i32 %%%d)\n",temporary, value);
            break;
        case Decimal:
        case Float32:
            printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([7 x i8], [7 x i8]* @print.float, i32 0, i32 0), double %%%d)\n", temporary, value);
            break;
        case String:
            // Imprime string (i8*)
            printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([4 x i8], [4 x i8]* @print.string, i32 0, i32 0), i32 %%%d)\n",temporary, value);
            break;
        case StrLit:
            temp = strings;
            x = 0;
            int length;
            while(x < string_counter){
                temp = temp->next;
                x++;
            }
            length = temp->length;
            printf("  %%%d = call i32 (i8*, ...) @printf(i8* getelementptr inbounds([%d x i8], [%d x i8]* @print.strlit%d, i32 0, i32 0))\n", temporary, length, length, string_counter);
            string_counter++;
            break;
        default:
            break;
    }
    return temporary++;
}


int codegen_not(struct node *expression, struct node *func_header) {
    // Geração de código para NOT lógico
    int value = codegen_expression(getchild(expression, 0), func_header);
    printf("  %%%d = xor i1 %%%d, true\n", temporary, value); // XOR com true inverte o valor
    return temporary++;
}

int codegen_plus(struct node *expression, struct node *func_header) {
    // Geração de código para NOT lógico
    int value = codegen_expression(getchild(expression, 0), func_header); // Obter o valor do filho
    if(expression->type == float_type){
        printf("  %%%d = fadd double 0.0, %%%d\n", temporary, value); // Negar o valor (0 - valor)
    }
    else printf("  %%%d = add i32 0, %%%d\n", temporary, value); // Negar o valor (0 - valor)
    return temporary++;
}

int codegen_minus(struct node *expression, struct node *func_header) {
    // Geração de código para NOT lógico
    int value = codegen_expression(getchild(expression, 0), func_header); // Obter o valor do filho
    if(expression->type == float_type){
        printf("  %%%d = fsub double 0.0, %%%d\n", temporary, value); // Negar o valor (0 - valor)
    }
    else printf("  %%%d = sub i32 0, %%%d\n", temporary, value); // Negar o valor (0 - valor)
    return temporary++;
}

int codegen_vardecl(struct node *expression, struct node *func_header) {
    // Geração de código para bloco de código
    switch(getchild(expression, 1)->type){
        case float_type:
        case double_type:
            printf("  %%%s = alloca double\n", getchild(expression, 1)->token);
        break;
        case integer_type:
            printf("  %%%s = alloca i32\n", getchild(expression, 1)->token);
        break;
        case boolean_type:
            printf("  %%%s = alloca i1\n", getchild(expression, 1)->token);
        break;
        default:
        break;
    }
    return temporary;
}


int codegen_expression(struct node *expression, struct node *func_header) {
    int tmp = -1;
    switch(expression->category) {
        case VarDecl:
            tmp = codegen_vardecl(expression, func_header);
            break;
        case Natural:
            tmp = codegen_natural(expression, func_header);
            break;
        case Decimal:
        case Float32:
            tmp = codegen_decimal(expression, func_header);
            break;
        case Print:
            tmp = codegen_print(expression, func_header);
            break;
        case Plus:
            tmp = codegen_plus(expression, func_header);
            break;
        case Minus:
            tmp = codegen_minus(expression, func_header);
            break;
        case Not:
            tmp = codegen_not(expression, func_header);
            break;
        case Block:
            tmp = codegen_block(expression, func_header);
            break;
        case Lt:
            tmp = codegen_lt(expression, func_header);
            break;
        case Le:
            tmp = codegen_le(expression, func_header);
            break;
        case Ge:
            tmp = codegen_ge(expression, func_header);
            break;
        case Gt:
            tmp = codegen_gt(expression, func_header);
            break;
        case And:
            tmp = codegen_and(expression, func_header);
            break;
        case Or:
            tmp = codegen_or(expression, func_header);
            break;
        case Eq:
            tmp = codegen_eq(expression, func_header);
            break;
        case Ne:
            tmp = codegen_ne(expression, func_header);
            break;
        case ParseArgs:
            tmp = codegen_parseargs(expression, func_header);
            break;
        case Assign:
            tmp = codegen_assign(expression, func_header);
            break;
        case Identifier:
            tmp = codegen_identifier(expression, func_header);
            break;
        case For:
            tmp = codegen_for(expression, func_header);
            break;
        case Mul:
            tmp = codegen_mul(expression, func_header);
            break;
        case Add:
            tmp = codegen_add(expression, func_header);
            break;
        case Sub:
            tmp = codegen_sub(expression, func_header);
            break;
        case Div:
            tmp = codegen_div(expression, func_header);
            break;
        case Mod:
            tmp = codegen_mod(expression, func_header);
            break;
        case Call:
            tmp = codegen_call(expression, func_header);
            break;
        case If:
            tmp = codegen_if_then_else(expression, func_header);
            break;
        case Return:
            tmp = codegen_expression(getchild(expression, 0), func_header);
            printf("  ret i32 %%%d\n", tmp);
            break;
        default:
            break;
    }
    return tmp;
}

void codegen_parameters(struct node *parameters) {
    struct node *parameter;
    int curr = 0;
    while((parameter = getchild(parameters, curr++)) != NULL) {
        if(curr > 1)
            printf(", ");
        enum type type = category_type(getchild(parameter, 0)->category);

        char test[10000];
        // Formata a string de acordo com o tipo do parâmetro
        if (type == integer_type) {
            sprintf(test, "  %%%s = alloca i32", getchild(parameter, 1)->token);  // Tipo inteiro de 32 bits
          
        } else if (type == double_type) {
            sprintf(test, "  %%%s = alloca double", getchild(parameter, 1)->token);  // Tipo double
           
        } else if (type == boolean_type) {
            sprintf(test, "  %%%s = alloca i1", getchild(parameter, 1)->token);  // Tipo boolean, representado como i1
            
        }
        
        // Adiciona a string test à lista de parâmetros
        struct param_define *new_param = (struct param_define*)malloc(sizeof(struct param_define));
        if (new_param == NULL) {
            fprintf(stderr, "Erro ao alocar memória para o novo parâmetro.\n");
            exit(1);  // Termina o programa caso não consiga alocar memória
        }

        // Aloca e copia a string formatada para o novo nó
        new_param->define_param = strdup(test);  // Cria uma cópia da string formatada
        new_param->next = NULL;

        // Se a lista de parâmetros estiver vazia, inicializa a lista
        if (list_param == NULL) {
            list_param = new_param;
        } else {
            // Caso contrário, adiciona o novo parâmetro ao final da lista
            struct param_define *last = list_param;
            while (last->next != NULL) {
                last = last->next;
            }
            last->next = new_param;
        }

    }
}

struct symbol_list *search_table (char *expression_value, char *identifier) {
    // Primeiramente, procura na tabela global
    struct symbol_table_list *symbol;
    for (symbol = symbol_tables; symbol != NULL; symbol = symbol->next) {
        if (strcmp(symbol->table->identifier, identifier) == 0) {
            return search_scope(symbol->table, expression_value);  // Encontrei o símbolo na tabela
        }
    }
    return NULL;
}
