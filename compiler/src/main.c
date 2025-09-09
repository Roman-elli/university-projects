#include "../include/functions.h"
#include "../include/semantic.h"
#include "../include/codegen.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../build/parser.tab.h"

// Local variables
int error_counter = 0;
int flagError = 1;
int showTree = 1;
int semantic = 1;
int valid_program = 0;
extern int semantic_errors;

// Extern variables
extern struct node *program;

int main(int argc, char **argv) {
    yydebug = 0;
    if(argc>1){
        for(int i = 1; i < argc; i++){
            if(strcmp(argv[i],"-l")==0) flagError=0; 
            else if(strcmp(argv[i],"-t")==0) showTree = 0;
            else if (strcmp(argv[i], "-s")==0) semantic = 0;
        }
    }
    
    yyparse();

    if(valid_program == 1){
        if(showTree == 0 && error_counter == 0) show(program, 0);
        semantic_errors += check_program(program); 

        if(semantic == 0) {
            show_all_symbol_tables();
            show_all(program, 0);
        }
    }
    if(semantic_errors == 0) codegen_program(program);
    freeTree(program);
    return 0;
}

extern int yywrap() {
    return 1;
}