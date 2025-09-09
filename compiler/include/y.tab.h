/* A Bison parser, made by GNU Bison 3.5.1.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2020 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    OR = 258,
    AND = 259,
    EQ = 260,
    LE = 261,
    GE = 262,
    PACKAGE = 263,
    VAR = 264,
    INT = 265,
    FLOAT32 = 266,
    BOOL = 267,
    STRING = 268,
    FUNC = 269,
    NE = 270,
    RETURN = 271,
    FOR = 272,
    PRINT = 273,
    PARSEINT = 274,
    CMDARGS = 275,
    IF = 276,
    ELSE = 277,
    SEMICOLON = 278,
    COMMA = 279,
    BLANKID = 280,
    ASSIGN = 281,
    STAR = 282,
    DIV = 283,
    MINUS = 284,
    PLUS = 285,
    GT = 286,
    LBRACE = 287,
    LPAR = 288,
    LSQ = 289,
    LT = 290,
    MOD = 291,
    NOT = 292,
    RBRACE = 293,
    RPAR = 294,
    RSQ = 295,
    RESERVED = 296,
    IDENTIFIER = 297,
    NATURAL = 298,
    DECIMAL = 299,
    STRLIT = 300,
    UNARY = 301
  };
#endif
/* Tokens.  */
#define OR 258
#define AND 259
#define EQ 260
#define LE 261
#define GE 262
#define PACKAGE 263
#define VAR 264
#define INT 265
#define FLOAT32 266
#define BOOL 267
#define STRING 268
#define FUNC 269
#define NE 270
#define RETURN 271
#define FOR 272
#define PRINT 273
#define PARSEINT 274
#define CMDARGS 275
#define IF 276
#define ELSE 277
#define SEMICOLON 278
#define COMMA 279
#define BLANKID 280
#define ASSIGN 281
#define STAR 282
#define DIV 283
#define MINUS 284
#define PLUS 285
#define GT 286
#define LBRACE 287
#define LPAR 288
#define LSQ 289
#define LT 290
#define MOD 291
#define NOT 292
#define RBRACE 293
#define RPAR 294
#define RSQ 295
#define RESERVED 296
#define IDENTIFIER 297
#define NATURAL 298
#define DECIMAL 299
#define STRLIT 300
#define UNARY 301

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 28 "gocompiler.y"

    char *lexeme;
    struct node *node;

#line 154 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


extern YYSTYPE yylval;
extern YYLTYPE yylloc;
int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
