#include <stdio.h>
#include <string.h>
#include "projeto.h"

int main(){   

    Sistema *filaR = cria();
    Sistema *filaP = cria();
    /* Abertura */
    printf("      ____      --------------------------------------------------------------------------------       ____     \n");
    printf("   __/  | \\__   | Bem vindo ao Manutenlava!! Reserve lavagens e manunteções de forma prática!! |    __/ |  \\__   \n");
    printf("  '--0----0--'  --------------------------------------------------------------------------------   '--0----0--'  \n\n");

    /* Definir tempo de estudo. */
    int x = 1;
    Time atual;
    while(x){
        printf("Digite a data em que deseja iniciar a aplicação:\n\nAno >>> ");
        atual.ano = checkint();
        if(atual.ano >= 0 && bissexto(atual.ano)){
            printf("Mês >>> ");
            atual.mes = checkint();
            if (atual.mes >=1 && atual.mes <= 12){
            printf("Dia >>> ");
            atual.dia = checkint();
            if(verificadia(atual.dia,atual.mes,1)) x = 0;
            else printf("\n*** Dia inválido ***\n");
            }
            else printf("\n*** Mês inválido ***\n");
        }
        else if(atual.ano >= 0 && !bissexto(atual.ano)){
            printf("Mês >>> ");
            atual.mes = checkint();
            if (atual.mes >=1 && atual.mes <= 12){
            printf("Dia >>> ");
            atual.dia = checkint();
            if(verificadia(atual.dia,atual.mes,0)) x = 0;
            else printf("\n*** Dia inválido ***\n");
            }
            else printf("\n*** Mês inválido ***\n");
        }
        else printf("\n*** Ano inválido ***\n");
    }
    

    /* Seleção das funcionalidades */
    x = 1;
    int option;
    while(x){
        menu();
        option = checkint();

        switch(option){
            case 1:
                registra(filaR,filaP,atual);
                break;
            case 2:
                retira(filaR,filaP, atual);
                break;
            case 3:
                printf("\nLista de reservas em ordem crescente: \n\n");
                imprime(filaR);
                printf("\nLista de pré-reservas em ordem crescente: \n\n");
                imprime(filaP);
                break;
            case 4:
                char nome[MAX];
                printf("\nDigite o nome pessoa que pretende aceder as reservas e pré-reservas:\n>>> ");
                fgets(nome,MAX,stdin);
                nome[strcspn(nome, "\n")] = '\0';
                ordena(filaR,nome);
                ordena(filaP,nome);
                break;
            case 5:
                printf("\nOpções disponíveis:\n\n");
                int choice = 0;
                while(choice != 3){
                    printf("1: Executar tarefa mais recente.\n");
                    printf("2: Alterar tempo atual.\n");
                    printf("3: Retornar ao menu.\n\n>>> ");
                    choice = checkint();
                    if(choice == 1){
                        if(!vazia(filaR)){
                        executa(filaR,filaP);
                        printf("\nReserva mais recentes executada.\n");
                        }else printf("\n*** Não há nenhuma reserva a ser executada no momento. ***\n");
                        choice = 3;
                    }
                    if(choice == 2){
                        int y = 1;
                        while(y){
                            printf("\nPor favor, preencha os dados da nova data em interesse para que atualizemos as listas.\n");
                            printf("Ano >>> ");
                            atual.ano = checkint();;
                            if(atual.ano >= 0 && bissexto(atual.ano)){
                                printf("Mês >>> ");
                                atual.mes = checkint();
                                if (atual.mes >=1 && atual.mes <= 12){
                                    printf("Dia >>> ");
                                    atual.dia = checkint();
                                if(verificadia(atual.dia,atual.mes,1)) y = 0;
                                else printf("Dia inválido.\n");
                                }
                                else printf("Mês inválido.\n");
                            }
                            else if(atual.ano >= 0 && !bissexto(atual.ano)){
                                printf("Mês >>> ");
                                atual.mes = checkint();
                                if (atual.mes >=1 && atual.mes <= 12){
                                    printf("Dia >>> ");
                                    atual.dia = checkint();
                                if(verificadia(atual.dia,atual.mes,0)) y = 0;
                                else printf("Dia inválido.\n");
                                }
                                else printf("Mês inválido.\n");
                            }
                            else printf("Ano inválido.\n");
                        }
                        atualizatempo(filaP, atual);
                        atualizatempo(filaR,atual);
                        printf("\nTempo atualizado com sucesso!!\n");
                        choice = 3;
                    }
                }
                break;
            case 6:
                verificafila(filaP,filaR);
                printf("\n*** Fila de espera atualizada. ***\n");
                break;
            case 7:
                carrega(filaR, "ListaR.txt");
                if(vazia(filaP)) carrega(filaP, "ListaP.txt");
                atualizatempo(filaP, atual);
                atualizatempo(filaR,atual);
                printf("\nListas carregadas com sucesso!! Marcações registradas em tempo anterior ao atual e que não possuem horários disponíveis não foram inseridas.\n");
                break;
            case 8:
                save(filaR,"data/ListaR.txt");
                save(filaP,"data/ListaP.txt");
                printf("\nListas salvas corretamente!!\n");
                break;
            case 9: 
                x = 0;
                break;
            default: printf("\nOpção inexistente. Digite novamente a opção que deseja.\n\n");
        }
    }
    destroi(filaR);
    destroi(filaP);

    printf("\n      ____     ---------------------------------------------------------       ____     \n");
    printf("   __/  | \\__  | Obrigado por utilizar o Manutenlava!!! Volte sempre!! |    __/ |  \\__   \n");
    printf("  '--0----0--' ---------------------------------------------------------   '--0----0--'  \n\n");

    return 0;
}