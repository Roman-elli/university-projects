%{

#include "functions.h"
#include "semantic.h"
#include "codegen.h"

#include "parser.tab.h"

#include <stdlib.h>
#include <stdio.h>

#define YY_USER_ACTION { previuscolumn = column; column += yyleng; yylloc.first_line = line; yylloc.first_column = previuscolumn; }
#define MAX_LENGTH 10000
#define PASS_TOKEN() yylval.lexeme = strdup(yytext);

int line = 1;
int column = 1;
int fator, validString;
char stringLit[MAX_LENGTH];
int lastToken = 0;
int commentColumnStart, commentLineStart;
int stringColumnStart, stringtLineStart;

extern int flagError;

int previuscolumn = 0;
int previusline = 0;

%}

digit               [0-9]
letter              [A-Za-z_]
whitespace          " "|\t
escape              \\f|\\r\\n|\\n|\\r|\\t|\\\\|\\\"
reserved            break|case|chan|const|continue|default|defer|fallthrough|go|goto|import|interface|map|range|select|struct|switch|type|\-\-|\+\+

%X                  COMMENT

%X                  STRINGS

%%
";"                          { if(flagError == 0) printf("SEMICOLON\n"); lastToken = 0; return SEMICOLON; }
","                          { if(flagError == 0) printf("COMMA\n"); lastToken = 0; return COMMA; }
"_"                          { if(flagError == 0) printf("BLANKID\n"); lastToken = 0; return BLANKID; }
"="                          { if(flagError == 0) printf("ASSIGN\n"); lastToken = 0; return ASSIGN; }
"*"                          { if(flagError == 0) printf("STAR\n"); lastToken = 0; return STAR; }
"/"                          { if(flagError == 0) printf("DIV\n"); lastToken = 0; return DIV; }
"-"                          { if(flagError == 0) printf("MINUS\n"); lastToken = 0; return MINUS;}
"+"                          { if(flagError == 0) printf("PLUS\n"); lastToken = 0; return PLUS;}
"=="                        { if(flagError == 0) printf("EQ\n"); lastToken = 0; return EQ; }
">="                        { if(flagError == 0) printf("GE\n"); lastToken = 0; return GE; }
">"                          { if(flagError == 0) printf("GT\n" ); lastToken = 0; return GT; }
"{"                          { if(flagError == 0) printf("LBRACE\n" ); lastToken = 0; return LBRACE; }
"<="                        { if(flagError == 0) printf("LE\n" ); lastToken = 0; return LE; }
"("                          { if(flagError == 0) printf("LPAR\n" ); lastToken = 0; return LPAR; }
"["                          { if(flagError == 0) printf("LSQ\n" ); lastToken = 0; return LSQ; }
"<"                          { if(flagError == 0) printf("LT\n" ); lastToken = 0; return LT; }
"%"                          { if(flagError == 0) printf("MOD\n" ); lastToken = 0; return MOD; }
"!="                        { if(flagError == 0) printf("NE\n" ); lastToken = 0; return NE; }
"!"                          { if(flagError == 0) printf("NOT\n" ); lastToken = 0; return NOT; }
"&&"                        { if(flagError == 0) printf("AND\n" ); lastToken = 0; return AND; }
"||"                        { if(flagError == 0) printf("OR\n" ); lastToken = 0; return OR; }
"}"                          { if(flagError == 0) printf("RBRACE\n" ); lastToken = 1; return RBRACE; }
")"                          { if(flagError == 0) printf("RPAR\n" ); lastToken = 1; return RPAR; }
"]"                          { if(flagError == 0) printf("RSQ\n" ); lastToken = 1; return RSQ;}   
package                     { if(flagError == 0) printf("PACKAGE\n" ); lastToken = 0; return PACKAGE; }
return                      { if(flagError == 0) printf("RETURN\n" ); lastToken = 1; return RETURN; }
else                        { if(flagError == 0) printf("ELSE\n" ); lastToken = 0; return ELSE; }
for                         { if(flagError == 0) printf("FOR\n" ); lastToken = 0; return FOR; }
if                          { if(flagError == 0) printf("IF\n" ); lastToken = 0; return IF; }
var                         { if(flagError == 0) printf("VAR\n" ); lastToken = 0; return VAR; }
int                         { if(flagError == 0) printf("INT\n" ); lastToken = 0; return INT; }
float32                     { if(flagError == 0) printf("FLOAT32\n" ); lastToken = 0; return FLOAT32; }
bool                        { if(flagError == 0) printf("BOOL\n" ); lastToken = 0; return BOOL; }
string                      { if(flagError == 0) printf("STRING\n" ); lastToken = 0; return STRING; }
fmt.Println                 { if(flagError == 0) printf("PRINT\n" ); lastToken = 0; return PRINT; }
strconv.Atoi                { if(flagError == 0) printf("PARSEINT\n"); lastToken = 0; return PARSEINT; }
func                        { if(flagError == 0) printf("FUNC\n"); lastToken = 0; return FUNC; }
os.Args                     { if(flagError == 0) printf("CMDARGS\n"); lastToken = 0; return CMDARGS; }

\n|\r|\r\n                         { 
    column = 1; previusline = line; line++;
    if(lastToken){ 
        lastToken = 0;
        if(flagError == 0)printf("SEMICOLON\n");
        return SEMICOLON;  
    } 
}
{whitespace}                                               { ; }

"0"[0-7]+                                                   { if(flagError == 0) printf("NATURAL(%s)\n", yytext); lastToken = 1; PASS_TOKEN(); return NATURAL; }
"0"[0-9]*[8-9]+[0-9]*                                      { printf("Line %d, column %d: invalid octal constant (%s)\n", line, column-yyleng, yytext); lastToken = 1; }
("0x"|"0X")([0-9]|[a-fA-F])+                               { if(flagError == 0) printf("NATURAL(%s)\n", yytext); lastToken = 1; PASS_TOKEN(); return NATURAL;}
{digit}+                                                    { if(flagError == 0) printf("NATURAL(%s)\n", yytext); lastToken = 1; PASS_TOKEN(); return NATURAL;}

{digit}*"."({digit}+|{digit}*[eE][+-]?{digit}+)            { if(flagError == 0) printf("DECIMAL(%s)\n", yytext); lastToken = 1; PASS_TOKEN(); return DECIMAL;}
{digit}+"."{digit}*([eE][+-]?{digit}+)?                    { if(flagError == 0) printf("DECIMAL(%s)\n", yytext); lastToken = 1; PASS_TOKEN(); return DECIMAL;}
{digit}+[eE][+-]?{digit}+                                  { if(flagError == 0) printf("DECIMAL(%s)\n", yytext); lastToken = 1; PASS_TOKEN(); return DECIMAL;}

{reserved}                                                 { if(flagError == 0) printf("RESERVED(%s)\n", yytext); lastToken = 0; return RESERVED; }

{letter}+({digit}|{letter})*                               { 
    if(flagError == 0) printf("IDENTIFIER(%s)\n", yytext); 
    lastToken = 1;
    PASS_TOKEN();
    return IDENTIFIER;
}


\"                  { BEGIN(STRINGS); fator = 0; memset(stringLit, 0, sizeof(stringLit)); stringtLineStart = line; stringColumnStart = column; validString = 1; }
<STRINGS>\"          { 
    stringLit[fator] = '\0';  
    if(validString){ 
        if(flagError == 0) printf("STRLIT(\"%s\")\n", stringLit); 
        char temp_string[MAX_LENGTH+3];
        sprintf(temp_string, "\"%s\"", stringLit);
        lastToken = 1;
        yylval.lexeme = strdup(temp_string);
        memset(temp_string, 0, sizeof(temp_string));
        BEGIN(INITIAL);
        return STRLIT;
    }
    BEGIN(INITIAL);
}

<STRINGS>{escape}                { 
    if (fator < MAX_LENGTH - 2) {
        stringLit[fator++] = yytext[0]; 
        stringLit[fator++] = yytext[1]; 
    }    

}
<STRINGS>\n|\r|\r\n              { 
    printf("Line %d, column %d: unterminated string literal\n", stringtLineStart, stringColumnStart-1);
    previusline = line;
    line++;
    column = 1;
    validString = 0;
    lastToken = 0;
    BEGIN(INITIAL);
}

<STRINGS><<EOF>>                 { 
    printf("Line %d, column %d: unterminated string literal\n", stringtLineStart, stringColumnStart-1);
    BEGIN(INITIAL);
    yyterminate();
}

<STRINGS>\\.|\\                  { 
    printf("Line %d, column %d: invalid escape sequence (%s)\n", line, column - yyleng, yytext);
    validString = 0; 
}

<STRINGS>.                       { if (fator < MAX_LENGTH - 1) stringLit[fator++] = yytext[0]; }

"/*"                            { BEGIN(COMMENT); commentLineStart = line; commentColumnStart = column;}
<COMMENT>"*/"                   { BEGIN(INITIAL); }
<COMMENT>(\n|\r|\r\n)           { column = 1; previusline = line; line++;}
<COMMENT>.                      { ; }
<COMMENT><<EOF>>                { 
    printf("Line %d, column %d: unterminated comment\n", commentLineStart, commentColumnStart-2);
    BEGIN(INITIAL);
    yyterminate();
}

"//".*(\n|\r|\r\n)                          { 
    column = 1; previusline = line; line++; 
    if (lastToken) {
        lastToken = 0;
        if(flagError == 0) printf("SEMICOLON\n");
        return SEMICOLON;
    }
}
"//".*                                      {}


<<EOF>>         {
    if(lastToken){ 
        lastToken = 0;
        if(flagError == 0) printf("SEMICOLON\n");
        return SEMICOLON;  
    }
    yyterminate();
}

.                               { 
     printf("Line %d, column %d: illegal character (%s)\n", line, column-yyleng, yytext); 
}

%%