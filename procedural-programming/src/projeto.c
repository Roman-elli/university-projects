#include "../include/projeto.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

void menu(Sistema *filaR, Sistema *filaP){
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
        printf("\nOpções disponíveis:\n");
        printf("1: Reservar lavagem ou manutenção.\n");
        printf("2: Cancelar uma reserva/Pré-reserva.\n");
        printf("3: Listar as reservas e as pré-reservas de lavagens e de manutenções ordenadas por data de forma crescente.\n");
        printf("4: Listar as reservas e as pré-reservas de um cliente ordenadas por data de forma decrescente.\n");
        printf("5: Opções para execução de tarefas.\n");
        printf("6: Atualizar fila de espera.\n");
        printf("7: Carregar listas.\n");
        printf("8: Salvar listas.\n");
        printf("9: Sair do programa.\n");
        printf("\nDigite a opção que deseja: ");     
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
                save(filaR,"ListaR.txt");
                save(filaP,"ListaP.txt");
                printf("\nListas salvas corretamente!!\n");
                break;
            case 9: 
                x = 0;
                break;
            default: printf("\nOpção inexistente. Digite novamente a opção que deseja.\n\n");
        }
    }

    printf("\n      ____     ---------------------------------------------------------       ____     \n");
    printf("   __/  | \\__  | Obrigado por utilizar o Manutenlava!!! Volte sempre!! |    __/ |  \\__   \n");
    printf("  '--0----0--' ---------------------------------------------------------   '--0----0--'  \n\n");   
}

int bissexto(int x){
        if(x % 400 == 0) return 1;
        else{
                if((x % 4 == 0) && (x % 100 != 0)) return 1;
                else return 0;
        }
}

int verificadia(int dia, int mes, int ano){ 
        /* ano == 1 (bissexto) <<>> ano == 0 (Não é bissexto) */
        switch(mes){
                case 1:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                case 2:
                        if(dia >= 1 && dia <= 29 && ano == 1) return 1;
                        if(dia >= 1 && dia <= 28 && ano == 0) return 1;
                        break;
                case 3:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                case 4:
                        if(dia >= 1 && dia <= 30) return 1;
                        break;
                case 5:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                case 6:
                        if(dia >= 1 && dia <= 30) return 1;
                        break;
                case 7:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                case 8:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                case 9:
                        if(dia >= 1 && dia <= 30) return 1;
                        break;
                case 10:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                case 11:
                        if(dia >= 1 && dia <= 30) return 1;
                        break;
                case 12:
                        if(dia >= 1 && dia <= 31) return 1;
                        break;
                default:
                break;
        }
        return 0;
}

Sistema *cria(){
        Sistema *aux = (Sistema *) malloc(sizeof(Sistema));
        if(aux != NULL){
                aux->prox = NULL;
                return aux;
        }
        else {
                perror("\n*** Erro de alocação de memória ***\n");
                return NULL;
        }             
}

void registra(Sistema *filaR, Sistema *filaP, Time atual){
        Pessoa insert;
        printf("\n [1] Reserva ---- [2] Pré-reserva\n\n>>> ");
                insert.work = checkint();
                if(insert.work == 1 || insert.work == 2){
                        printf("\n [1] Lavagem (30 MINUTOS) ---- [2] Manutenção (1 HORA)\n\n>>> ");
                        insert.func = checkint();;
                        if((insert.work == 1 || insert.work == 2) && (insert.func == 1 || insert.func == 2)){
                        printf("\nDigite seu nome: ");
                        fgets(insert.nome, MAX, stdin);
                        insert.nome[strcspn(insert.nome, "\n")] = '\0';
                        printf("\nData atual: %02d / %02d / %d *\n\nInsira os dados de sua reserva.\n\nAno: ", atual.dia,atual.mes,atual.ano);
                        insert.ano = checkint();

                        /* Caso o ano seja bissexto */
                                if(bissexto(insert.ano) && insert.ano >= atual.ano){
                                printf("Mês: ");
                                insert.mes = checkint();

                                /* Caso mes seja valido */
                                if(insert.mes >=1 && insert.mes <= 12 && (insert.ano > atual.ano || (insert.ano == atual.ano && insert.mes >= atual.mes))){
                                        printf("Dia: ");
                                        insert.dia = checkint();

                                        /* Caso o dia seja válido */
                                        if(verificadia(insert.dia,insert.mes,1) && (insert.ano > atual.ano || (insert.ano == atual.ano && insert.mes > atual.mes) || (insert.ano == atual.ano && insert.mes == atual.mes && insert.dia >= atual.dia))){
                                        
                                        /* Imprime as reservas e pré-reservas específicas do dia */
                                        if(insert.work == 1) imprimedata(filaR, insert);
                                        else imprimedata(filaP, insert);
                                        
                                        printf("\nHorario de funcionamento das 8:00 as 18:00. (Manutenções podem ser reservadas até as 17:00)\n");
                                        printf("\nHora: ");
                                        insert.hora = checkint();
                                        if(insert.hora >= 8 && insert.hora < 18){
                                                printf("\nA marcação dos minutos são feitas apenas em 0 e 30 minutos.\n\nMinutos: ");
                                                insert.min = checkint();
                                                if(insert.min != 0 && insert.min != 30) printf("*** Os minutos inseridos são invalidos. ***\n");
                                                else if (insert.func == 2 && insert.hora == 17 && insert.min == 30) printf("*** Não é possível marcar uma manutenção neste horário. ***\n"); 
                                                else if(insert.work == 1) insere(filaR, filaP,insert,1);
                                                else insere(filaP, NULL,insert,1);
                                        }
                                        else printf("\n*** A hora inserida é inválida. ***\n");
                                        }
                                        else printf("\n*** O dia inserido é inválido. ***\n");
                                }
                                else printf("\n*** O mes inserido é invalido. ***\n");  
                                }

                                /* Caso o ano não seja bissexto */
                                else if(insert.ano >= atual.ano){
                                printf("Mês: ");
                                insert.mes = checkint();

                                /* Caso mes seja valido */
                                if(insert.mes >= 1 && insert.mes <= 12 && (insert.ano > atual.ano || (insert.ano == atual.ano && insert.mes >= atual.mes))){
                                        printf("Dia: ");
                                        insert.dia = checkint();

                                        /* Caso o dia seja válido */
                                        if(verificadia(insert.dia, insert.mes,0) && (insert.ano > atual.ano || (insert.ano == atual.ano && insert.mes > atual.mes) || (insert.ano == atual.ano && insert.mes == atual.mes && insert.dia >= atual.dia))){
                                        
                                        /* Imprime as reservas e pré-reservas específicas do dia */
                                        if(insert.work == 1) imprimedata(filaR, insert);
                                        else imprimedata(filaP, insert);
                                        
                                        printf("\nHorario de funcionamento das 8:00 as 18:00.  (Manutenções podem ser reservadas até as 17:00)\n");
                                        printf("\nHora: ");
                                        insert.hora = checkint();
                                        
                                        if(insert.hora >= 8 && insert.hora < 18){
                                                printf("\nA marcação dos minutos são feitas apenas em 0 e 30 minutos.\n\nMinutos: ");
                                                insert.min = checkint();
                                                
                                                if(insert.min != 0 && insert.min != 30) printf("*** Os minutos inseridos são invalidos. ***\n");
                                                else if (insert.func == 2 && insert.hora == 17 && insert.min == 30) printf("Não é possível marcar uma manutenção neste horário.\n"); 
                                                else if(insert.work == 1) insere(filaR, filaP,insert,1);
                                                else insere(filaP, NULL,insert,1);  
                                        }
                                        else printf("\n*** A hora inserida é inválida. ***\n");
                                        }
                                        else printf("\n*** O dia inserido é inválido. ***\n");
                                }
                                else printf("\n*** O mes inserido é invalido. ***\n");              
                                }
                                else printf("\n*** O ano inserido é invalido. ***\n"); 
                        }              
                        else printf("\n*** Não existe esta função. Digite novamente a opção que deseja. ***\n");
                }else printf("\n***Não existe esta função. Digite novamente a opção que deseja. ***\n");
}

void imprime(Sistema *fila){
        if(!vazia(fila)){
                printf("%8s%15s%12s%16s\n", "Data", "Horário", "Função", "Usuario");
                for(Sistema *aux = fila->prox; aux != NULL; aux = aux->prox){
                        if(aux->usuario.func == 1){ 
                                printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s%10s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Lavagem",aux->usuario.nome);
                        }
                        if(aux->usuario.func == 2){ 
                                printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s %10s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Manutenção",aux->usuario.nome);
                     }
                }
        }
        else printf("*** Ainda não há nenhuma marcação nesta lista ***\n");
}

int vazia(Sistema *fila){
        if (fila->prox == NULL) return 1;
        else return 0;
}

void procura(Sistema *fila, Pessoa chave, Sistema **ant, Sistema **atual){
        *ant = fila; 
        *atual = fila->prox;
        while ((*atual) != NULL && 
                ((*atual)->usuario.ano < chave.ano ||
                ((*atual)->usuario.ano == chave.ano && (*atual)->usuario.mes < chave.mes) ||
                ((*atual)->usuario.ano == chave.ano && (*atual)->usuario.mes == chave.mes && (*atual)->usuario.dia < chave.dia) ||
                ((*atual)->usuario.ano == chave.ano && (*atual)->usuario.mes == chave.mes && (*atual)->usuario.dia == chave.dia && (*atual)->usuario.hora < chave.hora) ||
                ((*atual)->usuario.ano == chave.ano && (*atual)->usuario.mes == chave.mes && (*atual)->usuario.dia == chave.dia && (*atual)->usuario.hora == chave.hora && (*atual)->usuario.min < chave.min) ||
                ((*atual)->usuario.ano == chave.ano && (*atual)->usuario.mes == chave.mes && (*atual)->usuario.dia == chave.dia && (*atual)->usuario.hora == chave.hora && (*atual)->usuario.min == chave.min && (*atual)->usuario.work == 2))) {
        *ant = *atual;
        *atual = (*atual)->prox;
    }
        if ((*atual) != NULL && ((*atual)->usuario.dia != chave.dia || (*atual)->usuario.mes != chave.mes || (*atual)->usuario.ano != chave.ano || (*atual)->usuario.hora != chave.hora || (*atual)->usuario.min != chave.min)) {
                *atual = NULL; /* elemento não encontrado */
    }
}

int verificavaga(Sistema *fila, Pessoa p1){
        if(vazia(fila)) return 1;
        else{
                Sistema *aux = fila->prox;
                while(aux != NULL){
                        /* Mesma data e horario */
                        if(aux->usuario.ano == p1.ano && aux->usuario.mes == p1.mes && aux->usuario.dia == p1.dia && aux->usuario.hora == p1.hora && aux->usuario.min == p1.min && p1.work == 1) return 0;
                        /* Mesma data */
                        if(aux->usuario.ano == p1.ano && aux->usuario.mes == p1.mes && aux->usuario.dia == p1.dia && p1.work == 1){
                                /* Caso a hora seja x:00 */
                                if(p1.min == 0 && aux->usuario.hora == p1.hora-1 && aux->usuario.min == 30){
                                        if(aux->usuario.func == 2) return 0;
                                        /* Caso a anterior seja lavagem, a proxima esteja reservada e a marcação seja uma manutenção */
                                        else if(p1.func == 2 && aux->prox != NULL && aux->prox->usuario.hora == p1.hora && aux->prox->usuario.min == 30) return 0;
                                }
                                /* Caso a hora seja x:30 */
                                if(p1.min == 30 && aux->usuario.hora == p1.hora && aux->usuario.min == 0){
                                        if(aux->usuario.func == 2) return 0;
                                        /* Caso a anterior seja lavagem, a proxima esteja reservada e a marcação seja uma manutenção  */
                                        else if(p1.func == 2 && aux->prox != NULL && aux->prox->usuario.hora == p1.hora+1 && aux->prox->usuario.min == 0) return 0;
                                }
                                /* Caso seja manutenção o anterior esteja livre e o proximo esteja reservado*/
                                if((p1.min == 30 && p1.func == 2 && aux->usuario.hora == p1.hora+1 && aux->usuario.min == 0) || (p1.min == 0 && p1.func == 2 && aux->usuario.hora == p1.hora && aux->usuario.min == 30)) return 0;
                        }
                        aux = aux->prox;
                }
        }
        return 1;
}

void insere (Sistema *lista, Sistema *listaP, Pessoa p1, int x){ 
        if(verificavaga(lista,p1)){
                Sistema *no, *ant, *inutil;
                no = (Sistema *) malloc (sizeof (Sistema));
                if (no != NULL) {
                        no->usuario = p1;
                        procura (lista, p1, &ant, &inutil);
                        no->prox = ant->prox;
                        ant->prox = no; 
                        if(p1.work == 1 && x == 1)printf("\nReserva efetuada com sucesso!!\n");
                        else if(x == 1) printf("\nPré-reserva efetuada com sucesso.\n");
                }
        }
        else{
                int option = 0;
                printf("Este horário ja esta reservado. Deseja entrar em uma lista de espera para este horario?\n");
                while(!option){
                        printf("[1] Sim ---- [2] Não\n>>> ");
                        option = checkint();
                        if(option == 1){
                                p1.work = 2;
                                insere(listaP, NULL,p1,0);
                                printf("A sua pré-reserva foi feita com sucesso.\n");
                        }
                        else if(option == 2) printf("Peço desculpas o inconveniente. Caso ainda deseje reservar um serviço cheque a terceira função da aplicação e confira os horários disponíveis!\n");              
                        else{
                                printf("Opção inválida. Digite novamente a opção desejada.\n");
                                option = 0;
                        }
                }
        }
}

void imprimenome(Sistema *fila, Sistema *filaP, char *nome){
        int encontrou = 0;
        printf("As reservas de %s são:\n", nome);
        printf("\n%8s%15s%12s\n", "Data", "Horário", "Função");
        for(Sistema *aux = fila->prox; aux != NULL; aux = aux->prox){
                if(strcmp(aux->usuario.nome, nome) == 0){
                        encontrou++;
                        if(aux->usuario.func == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Lavagem");
                        else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Manutenção");     
                }
        }
        if(encontrou == 0) printf("%8s%14s%10s\n", "----", "-------", "------");       
        encontrou = 0;
        printf("\nAs pré-reservas de %s são:\n\n", nome);
        printf("%8s%15s%12s\n", "Data", "Horário", "Função");
        for(Sistema *aux = filaP->prox; aux != NULL; aux = aux->prox){
                if(strcmp(aux->usuario.nome, nome) == 0){
                        encontrou++;
                        if(aux->usuario.func == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Lavagem");
                           
                        else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Manutenção");
             }
        
        }
        if(encontrou == 0) printf("%8s%14s%10s\n", "----", "-------", "------");       
}

void imprimedata(Sistema *lista, Pessoa p1){
        printf("Reservas do dia %02d / %02d / %d:\n", p1.dia,p1.mes,p1.ano);
        Sistema *aux = lista->prox;
        int encontrou = 0;
        printf("%8s%15s%12s%12s%16s\n", "Data", "Horário", "Função", "Tipo", "Usuario");
        while((aux) != NULL){
                if(aux->usuario.dia == p1.dia && aux->usuario.mes == p1.mes && aux->usuario.ano == p1.ano){
                        if(aux->usuario.func == 1){
                                if(aux->usuario.work == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Lavagem", "Reserva", aux->usuario.nome);
                                                               
                                else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Lavagem", "Pré-reserva", aux->usuario.nome);
                        }
                        if(aux->usuario.func == 2){
                                if(aux->usuario.work == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Manutenção", "Reserva", aux->usuario.nome);
                                                                      
                                else printf("(%02d/%02d/%d)   [%02d:%02d]    %-10s    %-9s   %7s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Manutenção", "Pré-reserva", aux->usuario.nome);
                        }
                        encontrou++;
                        }
                aux = aux->prox;
                }
        if(encontrou == 0) printf("%8s%14s%10s%12s%16s\n", "----", "-------", "------", "----", "-------");       
}

void procuranome(Sistema *fila, Pessoa chave, Sistema **ant, Sistema **atual, int funcao){
        *ant = fila; 
        *atual = fila->prox;
        if(funcao == 1) while ((*atual) != NULL && (strcmp((*atual)->usuario.nome, chave.nome) != 0 
                              || (*atual)->usuario.dia != chave.dia || (*atual)->usuario.mes != chave.mes 
                              || (*atual)->usuario.ano != chave.ano || (*atual)->usuario.hora != chave.hora 
                              || (*atual)->usuario.min != chave.min)){
                *ant = *atual;
                *atual = (*atual)->prox;
                }
        if(funcao == 2) while ((*atual) != NULL && ((*atual)->usuario.dia != chave.dia 
                                || (*atual)->usuario.mes != chave.mes 
                                || (*atual)->usuario.ano != chave.ano || (*atual)->usuario.hora != chave.hora 
                                || (*atual)->usuario.min != chave.min)){
                *ant = *atual;
                *atual = (*atual)->prox;
                }

    if (*atual == NULL) {
        *ant = NULL; // elemento não encontrado
    }
}

void ordena(Sistema *lista, char *nome){
        Sistema *aux = lista->prox;
        int contador = 0;
        int encontrou = 0;
        if(!vazia(lista) && aux->usuario.work == 1) printf("\nAs reservas de %s são:\n", nome);
        else if(!vazia(lista)) printf("\nAs pré-reservas de %s são:\n", nome);
        printf("\n%8s%15s%12s\n", "Data", "Horário", "Função");
        while((aux) != NULL){
                contador++;
                aux = aux->prox;
        }
        while(contador != 0){
                Sistema *aux = lista;
                for(int i = 0; i <= contador; i++){
                        if(i == contador && strcmp(aux->usuario.nome,nome) == 0){
                                encontrou++;
                                if(aux->usuario.func == 1) printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Lavagem");
                        if(aux->usuario.func == 2) printf("(%02d/%02d/%d)   [%02d:%02d]    %-11s\n", aux->usuario.dia , aux->usuario.mes , aux->usuario.ano , aux->usuario.hora , aux->usuario.min , "Manutenção");
                            
                        }
                        aux = aux->prox;               
                }
                contador--;
        }
        if(encontrou == 0) printf("%8s%14s%10s\n", "----", "-------", "------");       
}

void retira(Sistema *listaR, Sistema *listaP, Time actual){
        Pessoa usuario;
        int erro = 0;
        printf("Preencha os dados para efetuar o cancelamento!\n");
        printf("Digite o seu nome: ");
        fgets(usuario.nome,MAX,stdin);
        usuario.nome[strcspn(usuario.nome, "\n")] = '\0';
        imprimenome(listaR, listaP, usuario.nome);
        printf("\n[1] Cancelar Reserva ---- [2] Cancelar pré-reserva\n\n>>> ");
        usuario.work = checkint();
        if(usuario.work == 1 || usuario.work == 2){
                printf("* Data atual: %02d / %02d / %d *\n", actual.dia,actual.mes,actual.ano);
                printf("Digite o ano: ");
                usuario.ano = checkint();
                if(usuario.ano >= actual.ano){
                        printf("Digite o mes : ");
                        usuario.mes = checkint();
                        if(usuario.mes >=1 && usuario.mes <= 12 && (usuario.ano > actual.ano || (usuario.ano == actual.ano && usuario.mes >= actual.mes))){
                                printf("Digite o dia : ");
                                usuario.dia = checkint();
                                if((usuario.ano > actual.ano || (usuario.ano == actual.ano && usuario.mes > actual.mes) || (usuario.ano == actual.ano && usuario.mes == actual.mes && usuario.dia >= actual.dia))){
                                        printf("Digite as horas : ");
                                        usuario.hora = checkint();
                                        if(usuario.hora >= 8 && usuario.hora <= 17){
                                                printf("Digite os minutos : ");
                                                usuario.min = checkint();
                                        }else{ printf("\nHora inválida.\n"); erro++;}
                                }else {printf("\nDia inválido.\n"); erro++;}
                        }else {printf("\nMês inválido.\n"); erro++;}
                }else {printf("\nAno inválido.\n"); erro++;}
        }else {printf("\nNão existe esta função.\n"); erro++;}

        Sistema *ant, *atual;
        if(usuario.work == 1 && erro == 0){
                /* Eliminar e checar pré-reserva! */
                procuranome (listaR, usuario, &ant, &atual,1);
                if (atual != NULL) {
                        ant->prox = atual->prox;
                        free(atual);
                        printf("A reserva de %s foi cancelada com sucesso.\n", usuario.nome);
                        /* Verifica pré-reserva e substitui */
                        verificafila(listaP,listaR);
                }
                else printf("Usuario não encontrado.\n");
        }
        else if(usuario.work == 2 && erro == 0){
                /* Eliminar pré-reserva */
                procuranome (listaP, usuario, &ant, &atual,1);
                if (atual != NULL) {
                        ant->prox = atual->prox;
                        free (atual);
                        printf("A pré-reserva de %s foi cancelada com sucesso.\n", usuario.nome);
                }
                else printf("Usuario não encontrado.\n");
        }
}

void verificafila(Sistema *listaP, Sistema *listaR){
        Sistema *aux = listaP->prox;
        Sistema *temp = listaP;
        while (aux != NULL) {
                aux->usuario.work = 1;
                if(verificavaga(listaR, aux->usuario)){
                        insere(listaR, NULL,aux->usuario,0);
                        temp->prox = aux->prox;  // Atualiza o ponteiro do elemento anterior
                        free(aux);  // Libera a memória do elemento
                        aux = temp->prox;  // Atualiza o ponteiro auxiliar
                } else {
                aux->usuario.work = 2;
                temp = aux;  // Atualiza o ponteiro temporário
                aux = aux->prox;  // Atualiza o ponteiro auxiliar
                }
        }
}

int checkint() {
    int x;
    while (scanf("%d", &x) != 1 || getchar() != '\n') {
        printf("Opção inválida. Digite novamente.\n>>> ");
        while (getchar() != '\n');
    }
    return x;
}

void atualizatempo(Sistema *lista, Time atual) {
    Sistema *aux = lista->prox;
    Sistema *temp = lista;

    while (aux != NULL) {
        if (aux->usuario.ano < atual.ano || 
            (aux->usuario.ano == atual.ano && aux->usuario.mes < atual.mes) || 
            (aux->usuario.ano == atual.ano && aux->usuario.mes == atual.mes && aux->usuario.dia < atual.dia)) {
            
            temp->prox = aux->prox;     /* Atualiza o ponteiro do elemento anterior */
            free(aux);                  /* Libera a memória do elemento   */
            aux = temp->prox;           /* Atualiza o ponteiro auxiliar   */
        } else {
            temp = aux;                 /* Atualiza o ponteiro temporário */
            aux = aux->prox;            /* Atualiza o ponteiro auxiliar   */
        }
    }
}

void atualizafila(Sistema *lista, Pessoa atual){
        Sistema *aux = lista->prox;
        Sistema *temp = lista;
        while (aux != NULL) {
                if (aux->usuario.ano < atual.ano || 
                (aux->usuario.ano == atual.ano && aux->usuario.mes < atual.mes) || 
                (aux->usuario.ano == atual.ano && aux->usuario.mes == atual.mes && aux->usuario.dia < atual.dia) || 
                (aux->usuario.ano == atual.ano && aux->usuario.mes == atual.mes && aux->usuario.dia == atual.dia && aux->usuario.hora < atual.hora) ||
                (aux->usuario.ano == atual.ano && aux->usuario.mes == atual.mes && aux->usuario.dia == atual.dia && aux->usuario.hora < atual.hora) || 
                (aux->usuario.ano == atual.ano && aux->usuario.mes == atual.mes && aux->usuario.dia == atual.dia && aux->usuario.hora == atual.hora && aux->usuario.min < atual.min) || 
                (aux->usuario.ano == atual.ano && aux->usuario.mes == atual.mes && aux->usuario.dia == atual.dia && aux->usuario.hora == atual.hora && aux->usuario.min == atual.min)){
                temp->prox = aux->prox;  /* Atualiza o ponteiro do elemento anterior */
                free(aux);               /* Libera a memória do elemento */
                aux = temp->prox;        /* Atualiza o ponteiro auxiliar */
                } else {
                temp = aux;              /* Atualiza o ponteiro temporário */
                aux = aux->prox;         /* Atualiza o ponteiro auxiliar */
                }
        }
}

void executa(Sistema *listaR, Sistema *listaP){
        Sistema *aux = listaR->prox;
        if(!vazia(listaR)){
                listaR->prox = aux->prox;
                if(!vazia(listaP)){
                        atualizafila(listaP,aux->usuario);                        
                }
                free(aux);
        }
}

void carrega(Sistema *lista, const char *ficheiro){

        char caminho[128];
        snprintf(caminho, sizeof(caminho), "data/%s", ficheiro);
        FILE *arquivo = fopen(caminho, "r");
        
        if (arquivo == NULL) {
                if(strcmp(ficheiro, "ListaR.txt") == 0) printf("** No reservations on database. **\n");
                else if(strcmp(ficheiro, "ListaP.txt") == 0) printf("** No pre-reservations on database. **\n");
                else printf("** Error opening save files. **\n");
                return;
        }

        Pessoa insert;
        /* Percorre as listas e lê os dados do arquivo */
        while (fscanf(arquivo, "%d %d %d %d %d %d %d", &insert.work, &insert.func, &insert.ano, &insert.mes, &insert.dia, &insert.hora, &insert.min) == 7) {
                fgets(insert.nome, MAX, arquivo);
                insert.nome[strcspn(insert.nome, "\n")] = '\0';
                if(strcmp(ficheiro,"ListaR.txt") == 0 && verificavaga(lista,insert)) insere(lista, NULL, insert,0);
                else if (strcmp(ficheiro,"ListaP.txt") == 0) insere(lista, NULL, insert,0);
        }
        fclose(arquivo);
}

void save(Sistema *lista, const char *ficheiro){
        /* Abre o arquivo para escrita */
        mkdir("data", 0777);  // garante que a pasta exista
        char caminho[128];
        snprintf(caminho, sizeof(caminho), "data/%s", ficheiro);

        FILE *arquivo = fopen(caminho, "w");

        if (arquivo == NULL) {
                printf("Erro ao abrir o arquivo %s\n", caminho);
                return;
        }
        
        /* Percorre a lista e escreve dados no arquivo */
        Sistema *atual = lista->prox;
        while (atual != NULL) {
                fprintf(arquivo, "%d %d %d %d %d %d %d", atual->usuario.work, atual->usuario.func, atual->usuario.ano, atual->usuario.mes, atual->usuario.dia, atual->usuario.hora, atual->usuario.min);
                fprintf(arquivo, "%s\n", atual->usuario.nome);
                atual = atual->prox;
        }
        fclose(arquivo);
}

void destroi(Sistema *fila){
        Sistema *aux;
        while (!vazia (fila)) {
                aux = fila;
                fila = fila->prox;
                free (aux);
        }
        free(fila);
}