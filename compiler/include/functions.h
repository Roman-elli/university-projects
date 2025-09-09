#ifndef FUNCTIONS_H
#define FUNCTIONS_H

enum category {
    Program, FuncHeader, Identifier, Var, Int, Float32, Bool, String, Func, 
    VarDecl, ParamDecl, FuncParams, Type, FuncDecl, FuncBody, ParseArgs, Expr, Add, Sub, Mul, Div, Mod, Not, Minus, Plus, Or, And, Eq, Ne, Lt, If,
    Gt, Le, Ge, Natural, Decimal, StrLit, Else, For, Return, Print, Assign, Block, Call , Delete
};

#define names { "Program", "FuncHeader", "Identifier", "Var", "Int", "Float32", "Bool", "String", "Func", \
                "VarDecl", "ParamDecl", "FuncParams", "Type", "FuncDecl", \
                "FuncBody", "ParseArgs", "Expr", "Add", "Sub", "Mul", "Div", "Mod", "Not", "Minus", "Plus", "Or", "And", \
                "Eq", "Ne", "Lt", "If","Gt", "Le", "Ge", "Natural", "Decimal", "StrLit", "Else", "For", "Return", "Print", \
                "Assign", "Block", "Call", "Delete"}

// Enum para os tipos
enum type {integer_type, double_type, boolean_type, float_type, string_type, no_type, void_type, undefined};

// Macro to return the type name as a string
#define type_name(type) (type == integer_type ? "int" : type == double_type ? "double" : type == boolean_type ? "bool" : type == float_type ? "float32" : \
                         type == string_type ? "string" : type == no_type ? "none" : undefined ? "undef" : "")

// Macro to map category values to type values
#define category_type(category) (category == Int || category == Natural ? integer_type : \
                                 category == Bool ? boolean_type : \
                                 category == Float32 ? float_type :  category == String ? string_type : \
                                 no_type)
struct node {
    enum category category;
    char *token;
    char param_list[15000];
    int type_param;
    int token_line, token_column;
    enum type type;
    int print_type;
    struct node_list *children;
    int freeNode;
    int used;
    int isFunction;
};

struct node_list {
    struct node *node;
    struct node_list *next;
};


struct node *newnode(enum category category, char *token);
void addchild(struct node *parent, struct node *child);
void show(struct node *root, int depth);
void show_all(struct node *node, int depth);
void delete(struct node *parent, struct node *child);
void libertaArvore(struct node * node);

struct node *getchild(struct node *parent, int position);
int countchildren(struct node *node);
#endif
