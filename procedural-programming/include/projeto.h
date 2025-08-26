#ifndef PROJETO_H
#define PROJETO_H
#define MAX 50

/* Estrutura de armazenamento de dados de cada usuário
 .work == 1 (reserva) <<>> .work == 2 (pré-reserva)
 .func == 1 (Lavagem) <<>> .work == 2 (Manutenção) */

typedef struct {
    char nome[MAX];
    int hora,min,dia,mes,ano, work, func;  
}Pessoa;

/* Estrutura para armazenamento da data atual */
typedef struct{
    int dia,mes,ano;
}Time;

/* Estrutura que armazena cada estrutura de usuario (Pessoa) e o ponteiro que aponta para o próximo da lista */
typedef struct noFila{
    Pessoa usuario;
    struct noFila *prox;    
}Sistema;   

void menu(Sistema *filaR, Sistema *filaP);                                        /* impressão do menu */
int bissexto(int x);                                /* Verificação de ano bissexto */
int verificadia(int dia, int mes, int ano);         /* Verifica se o dia inserido é válido */
Sistema *cria();                                    /* Inicializa as listas */
int vazia(Sistema *fila);                           /* Verifica se a lista esta vazia */
void destroi(Sistema *fila);                        /* Liberta toda a memória alocada em uma lista específica */
int verificavaga(Sistema *lista, Pessoa p1);        /* Verifica se um horário específico está disponível para reserva */
void procura(Sistema *fila, Pessoa chave, Sistema **ant, Sistema **atual);                      /* Procura um elemento específico da lista levando em conta a data e horário */
void procuranome(Sistema *fila, Pessoa chave, Sistema **ant, Sistema **atual, int funcao);      /* Procura um elemento específico da lista levando em conta o nome de uma pessoa */
void insere(Sistema *lista,Sistema *listaP, Pessoa p1, int x);      /* Insere um elemento na lista caso seja possível */
void imprime(Sistema *fila);                                        /* Imprime a lista em ordem temporal */
void imprimenome(Sistema *fila, Sistema *filaP, char *nome);        /* Imprime as reservas e pré-reservas de uma pessoa específica */
void imprimedata(Sistema *fila, Pessoa insert);                     /* Imprime a lista de reservas e pré-reservas de um determinado dia */
void registra(Sistema *filaR, Sistema *filaP, Time atual);          /* Registra todos os dados necessários para que se faça uma reserva ou uma pré-reserva */
void ordena(Sistema *lista, char *nome);                            /* Imprime de as reservas e pré-reservas de um cliente específico em ordem de data de forma descrescente*/
int checkint();                                                     /* Checa o que o usuário escreve e verifica se há algum caracter inválido */
void retira(Sistema *listaR, Sistema *listaP, Time actual);         /* Retira um elemento da lista de acordo com as informações dadas */
void carrega(Sistema *listaR, const char *ficheiro);                /* Coleta todas as informações salvas em um ficheiro específico e as insere em sua respetiva lista */
void save(Sistema *lista, const char *ficheiro);                    /* Salva todos os dados das listas em seus respetivos ficheiros */
void atualizatempo(Sistema *lista, Time atual);                     /* Atualiza as listas para as novas definições de tempo atual */
void atualizafila(Sistema *lista, Pessoa atual);                    /* Após a execução de uma reserva, verifica todas as pré-reservas anteriores a ordem executada e as retira */
void verificafila(Sistema *listaP, Sistema *listaR);                /* Atualiza a fila de pré-reservas após a remoção de um usuário das reservas */
void executa(Sistema *listaR, Sistema *listaP);                     /* Executa a ordem mais antiga das reservas */

#endif