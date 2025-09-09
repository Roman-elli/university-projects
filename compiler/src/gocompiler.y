
/* Beatriz Alexandra Azeitona Mourato - 2022224891 */
/* Thales Barbuto Romanelli Lopes - 2022169928 */

/* START definitions section -- C code delimited by %{ ... %} and token declarations */

%{

#include "functions.h"
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int yylex(void);

struct node *program = NULL;

extern int line, column, previusline, previuscolumn, stringtLineStart, stringColumnStart, yyleng;
extern char *yytext;
void yyerror (char *s);

int erros = 0;
extern int valid_program;
extern char *category_name[];

%}
%union{
    char *lexeme;
    struct node *node;
}

%locations
%{
#define LOCATE(node, line, column) { node->token_line = line; node->token_column = column; }
%}


%debug

%token OR AND EQ LE GE PACKAGE VAR INT FLOAT32 BOOL STRING FUNC NE RETURN FOR PRINT PARSEINT CMDARGS IF ELSE SEMICOLON COMMA BLANKID ASSIGN STAR DIV MINUS PLUS GT LBRACE LPAR LSQ LT MOD NOT RBRACE RPAR RSQ RESERVED  
%token<lexeme> IDENTIFIER NATURAL DECIMAL STRLIT 
%type<node> Program Declarations VarDeclaration VarSpecs Type FuncDeclaration Parameters VarsAndStatements Statement OpcionalStatement Expr ParseArgs FuncInvocation FuncInvocations 

 
%left OR 
%left AND
%left EQ LE GE NE LT GT  
%left PLUS MINUS            
%left STAR DIV MOD          

%right UNARY   /* operador unário '!' tem maior precedência */

/* START grammar rules section -- BNF grammar */

%%
Program: PACKAGE IDENTIFIER SEMICOLON Declarations {
            $$ = program = newnode(Program, NULL);
            valid_program = 1;
            delete($$, $4);
        }
        | /* empty file */ { valid_program = 0; }
;

Declarations: Declarations VarDeclaration SEMICOLON { 
            if ($1 == NULL) $$ = newnode(Delete, NULL); 
            else $$ = $1;
            delete($$, $2);
        }
        
        | Declarations FuncDeclaration SEMICOLON { 
            if ($1 == NULL) $$ = newnode(Delete, NULL); 
            else $$ = $1; 

            if ($2 != NULL) addchild($$, $2);
        }

        |   /* vazio */ { $$ = NULL; valid_program = 0; } 
;

VarDeclaration: VAR IDENTIFIER VarSpecs Type {
            $$ = newnode(Delete, NULL);
            struct node * testing = newnode(VarDecl, NULL);
            addchild($$, testing);
            addchild(testing, $4);  
            addchild(testing, newnode(Identifier, $2));
            LOCATE(getchild(testing, 1), @2.first_line, @2.first_column);

            if($3 != NULL){
                struct node_list *child = $3->children->next;  
                while (child != NULL) {
                    struct node *varDecl = newnode(VarDecl, NULL);  
                    addchild(varDecl, $4);  
                    addchild(varDecl, newnode(Identifier, child->node->token));
                    LOCATE(getchild(varDecl, 1), child->node->token_line, child->node->token_column);  
                    addchild($$, varDecl);  
                    child = child->next;
                }
            }
        }

        | VAR LPAR IDENTIFIER VarSpecs Type SEMICOLON RPAR {
            $$ = newnode(Delete, NULL);
            struct node * testing = newnode(VarDecl, NULL);
            addchild($$, testing);
            addchild(testing, $5);  
            addchild(testing, newnode(Identifier, $3));  
            LOCATE(getchild(testing, 1), @3.first_line, @3.first_column);

            if($4 != NULL){
                struct node_list *child = $4->children->next;  
                while (child != NULL) {
                    struct node *varDecl = newnode(VarDecl, NULL);  
                    addchild(varDecl, $5); 
                    addchild(varDecl, newnode(Identifier, child->node->token));
                    LOCATE(getchild(varDecl, 1), child->node->token_line, child->node->token_column);  
                    addchild($$, varDecl);  
                    child = child->next;
                }
            }
        }
;

VarSpecs: VarSpecs COMMA IDENTIFIER { 
            if ($1 != NULL) {
                $$ = $1;  
                int x = countchildren($$);
                addchild($$, newnode(Identifier, $3));                
                LOCATE(getchild($$, x), @3.first_line, @3.first_column);  
            } else {
                $$ = newnode(VarDecl, NULL);  
                addchild($$, newnode(Identifier, $3));
                LOCATE(getchild($$, 0), @3.first_line, @3.first_column);
            }
        }
        |   /* vazio */ { $$ = NULL; } 
;

FuncDeclaration: FUNC IDENTIFIER LPAR Parameters RPAR Type LBRACE VarsAndStatements RBRACE { 
            $$ = newnode(FuncDecl, NULL);
            
            struct node *Header = newnode(FuncHeader, NULL);
            addchild(Header, newnode(Identifier, $2));
            LOCATE(getchild(Header, 0), @2.first_line, @2.first_column);
            addchild(Header, $6);

            addchild(Header, $4);

            addchild($$, Header);    
            addchild($$, $8); 
        }
        | FUNC IDENTIFIER LPAR Parameters RPAR LBRACE VarsAndStatements RBRACE { 
            $$ = newnode(FuncDecl, NULL);
            struct node *Header = newnode(FuncHeader, NULL);
            addchild(Header, newnode(Identifier, $2));
            LOCATE(getchild(Header, 0), @2.first_line, @2.first_column);
            addchild(Header, $4);
                
            addchild($$, Header);    
            addchild($$, $7); 
        }

        | FUNC IDENTIFIER LPAR RPAR Type LBRACE VarsAndStatements RBRACE { 
            $$ = newnode(FuncDecl, NULL);
            
            struct node *Header = newnode(FuncHeader, NULL);
            addchild(Header, newnode(Identifier, $2));
            LOCATE(getchild(Header, 0), @2.first_line, @2.first_column);
            addchild(Header, $5);

            struct node *Params = newnode(FuncParams, NULL);
            addchild(Header, Params);

            addchild($$, Header);    
            addchild($$, $7); 
        }

        | FUNC IDENTIFIER LPAR RPAR LBRACE VarsAndStatements RBRACE { 
            $$ = newnode(FuncDecl, NULL);
            
            struct node *Header = newnode(FuncHeader, NULL);
            addchild(Header, newnode(Identifier, $2));
            LOCATE(getchild(Header, 0), @2.first_line, @2.first_column);
            struct node *Params = newnode(FuncParams, NULL);
            addchild(Header, Params);

            addchild($$, Header);    
            addchild($$, $6);
        }
;

Type: INT             { $$ = newnode(Int, NULL); }
        | FLOAT32     { $$ = newnode(Float32, NULL); }
        | BOOL        { $$ = newnode(Bool, NULL); }
        | STRING      { $$ = newnode(String, NULL); }
;


Parameters: IDENTIFIER Type  { 
            $$ = newnode(FuncParams, NULL);
            struct node *Decl = newnode(ParamDecl, NULL);
            addchild($$, Decl);
            addchild(Decl, $2); 
            addchild(Decl, newnode(Identifier, $1));
            LOCATE(getchild(Decl, 1), @1.first_line, @1.first_column);
        }
                
        | Parameters COMMA IDENTIFIER Type { 
            $$ = $1; 
            struct node *Decl = newnode(ParamDecl, NULL);
            addchild($$, Decl);
            addchild(Decl, $4); 
            addchild(Decl, newnode(Identifier, $3));
            LOCATE(getchild(Decl, 1), @3.first_line, @3.first_column);
        }           
;

VarsAndStatements: VarsAndStatements SEMICOLON { $$ = $1; }

        | VarsAndStatements VarDeclaration SEMICOLON {
            $$ = $1;
            delete($$, $2); 
        }

        | VarsAndStatements Statement SEMICOLON {
            $$ = $1;
            delete($$, $2); 
        }

        |   { $$ = newnode(FuncBody, NULL); }
    ;

Statement:
        IF Expr LBRACE OpcionalStatement RBRACE {
            $$ = newnode(If, NULL);
            delete($$, $2);
            
            if($4 != NULL) addchild($$, $4); 
            addchild($$, newnode(Block, NULL)); 
        }

        | IF Expr LBRACE OpcionalStatement RBRACE ELSE LBRACE OpcionalStatement RBRACE {
            $$ = newnode(If, NULL);
            delete($$, $2);
            
            if($4 != NULL) addchild($$, $4); 
            else addchild($$, newnode(Block, NULL)); 

            if($8 != NULL) addchild($$, $8); 
            else addchild($$, newnode(Block, NULL)); 
        }

        | FOR Expr LBRACE OpcionalStatement RBRACE {
            $$ = newnode(For, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            delete($$, $2);
            
            if ($4 == NULL) $4 = newnode(Block, NULL);
            else addchild($$, $4); 
        }

        | FOR LBRACE OpcionalStatement RBRACE {
            $$ = newnode(For, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            
            if ($3 == NULL) $3 = newnode(Block, NULL);
            else addchild($$, $3); 
        }

        | RETURN Expr {
            $$ = newnode(Return, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            delete($$, $2); 
        }
        
        | RETURN {
            $$ = newnode(Return, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
        }

        | IDENTIFIER ASSIGN Expr {
            $$ = newnode(Assign, NULL);
            addchild($$, newnode(Identifier, $1));
            LOCATE($$, @2.first_line, @2.first_column);
            LOCATE(getchild($$, 0), @1.first_line, @1.first_column);
            delete($$, $3);
        }

        | LBRACE OpcionalStatement RBRACE { 
            if($2->children->next == NULL) $$ = NULL;
            else if($2->children->next->next == NULL)
                $$ = $2->children->next->node;
            else {
                struct node_list *child = $2->children->next;  
                int has_valid_child = 0;
                
                while (child != NULL) {
                    if (child->node != NULL) {
                        has_valid_child = 1;
                        break;
                    }
                    child = child->next;
                }

                if (has_valid_child) $$ = $2;  
                else $$ = NULL;      
            } 
        }

        | FuncInvocation {
            $$ = newnode(Delete, NULL);
            addchild($$, $1); 
        }

        | ParseArgs {
            $$ = newnode(Delete, NULL);
            addchild($$, $1);
        }

        | PRINT LPAR Expr RPAR {
            $$ = newnode(Print, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            delete($$, $3); 
        }

        | PRINT LPAR STRLIT RPAR {
            $$ = newnode(Print, NULL);
            addchild($$, newnode(StrLit, $3));
            LOCATE($$, @1.first_line, @1.first_column);
            LOCATE(getchild($$,0), @3.first_line, @3.first_column);
        }

        | error { $$ = NULL; }
;

OpcionalStatement: OpcionalStatement Statement SEMICOLON  { 
            $$ = $1;
            delete($$, $2); 
        }

        |   { $$ = newnode(Block, NULL); }
;

ParseArgs: IDENTIFIER COMMA BLANKID ASSIGN PARSEINT LPAR CMDARGS LSQ Expr RSQ RPAR { 
            $$ = newnode(ParseArgs, NULL);
            addchild($$, newnode(Identifier, $1));
            LOCATE($$, @5.first_line, @5.first_column);
            LOCATE(getchild($$, 0), @1.first_line, @1.first_column);
            delete($$, $9);
        }

        | IDENTIFIER COMMA BLANKID ASSIGN PARSEINT LPAR CMDARGS LSQ error RSQ RPAR { $$ = NULL; }
;

FuncInvocation: IDENTIFIER LPAR  Expr FuncInvocations RPAR { 
            $$ = newnode(Call, NULL);
            addchild($$, newnode(Identifier, $1));
            LOCATE($$, @1.first_line, @1.first_column);
            LOCATE(getchild($$, 0), @1.first_line, @1.first_column);
            delete($$, $3); 
            delete($$, $4); 
        }

        | IDENTIFIER LPAR RPAR {
            $$ = newnode(Call, NULL);
            addchild($$, newnode(Identifier, $1));
            LOCATE($$, @1.first_line, @1.first_column);
            LOCATE(getchild($$, 0), @1.first_line, @1.first_column);
        }

        | IDENTIFIER LPAR error RPAR { $$ = NULL; }
;

FuncInvocations: FuncInvocations COMMA Expr { 
                $$ = $1;
                delete($$, $3); }

        |  { $$ = newnode(Delete, NULL); }   
;

Expr: Expr OR Expr { 
            $$ = newnode(Or, NULL);
            LOCATE($$, @2.first_line, @2.first_column); 
            delete($$, $1);
            delete($$, $3); 
        }

        | Expr AND Expr { 
            $$ = newnode(And, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr LT Expr { 
            $$ = newnode(Lt, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr GT Expr { 
            $$ = newnode(Gt, NULL);
            LOCATE($$, @2.first_line, @2.first_column); 
            delete($$, $1);
            delete($$, $3);
        }

        | Expr EQ Expr {
            $$ = newnode(Eq, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr NE Expr {
            $$ = newnode(Ne, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr LE Expr {
            $$ = newnode(Le, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr GE Expr {
            $$ = newnode(Ge, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr PLUS Expr {
            $$ = newnode(Add, NULL);
            LOCATE($$, @2.first_line, @2.first_column); 
            delete($$, $1);
            delete($$, $3);
        }

        | Expr MINUS Expr {
            $$ = newnode(Sub, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        } 

        | Expr STAR Expr {
            $$ = newnode(Mul, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr DIV Expr { 
            $$ = newnode(Div, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | Expr MOD Expr { 
            $$ = newnode(Mod, NULL); 
            LOCATE($$, @2.first_line, @2.first_column);
            delete($$, $1);
            delete($$, $3);
        }

        | NOT Expr %prec UNARY { 
            $$ = newnode(Not, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            delete($$, $2);
        }

        | MINUS Expr %prec UNARY { 
            $$ = newnode(Minus, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            delete($$, $2);
        }

        | PLUS Expr %prec UNARY { 
            $$ = newnode(Plus, NULL);
            LOCATE($$, @1.first_line, @1.first_column);
            delete($$, $2);
        }

        | NATURAL { 
            $$ = newnode(Natural, $1);
            LOCATE($$, @1.first_line, @1.first_column);

         }

        | DECIMAL { 
            $$ = newnode(Decimal, $1);
            LOCATE($$, @1.first_line, @1.first_column);

        }

        | IDENTIFIER { 
            $$ = newnode(Identifier, $1);
            LOCATE($$, @1.first_line, @1.first_column); 
            }

        | FuncInvocation { 
            $$ = newnode(Delete, NULL);
            addchild($$, $1);
        }

        | LPAR Expr RPAR { $$ = $2; }

        | LPAR error RPAR { $$ = NULL; } 
;

%%

/* START subroutines section */

void yyerror(char *s) {
    erros = 1;
    if (strcmp(yytext, "\n") == 0) {
        printf("Line %d, column %d: %s: %s\n", previusline, previuscolumn, s, yytext);
    }
    else if(yytext[0] == '"'){
        printf("Line %d, column %d: %s: %s\n", stringtLineStart, stringColumnStart - 1, s, yylval.lexeme);
        yylval.lexeme[0] = '\0';
    }
   else if(yytext[0] == '\0'){
        printf("Line %d, column %d: %s: %s\n", line, column, s, yytext);
    }
    else printf("Line %d, column %d: %s: %s\n", line, column - yyleng, s, yytext);
}