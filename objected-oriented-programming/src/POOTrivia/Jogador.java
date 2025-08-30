package POOTrivia;
import java.io.Serializable;
import java.util.ArrayList;

/**
 * a class Jogador é onde serão armazenados as informações dos Jogadores.
 * Esta classe contêm uma string playerName, que representa o nome do jogador, uma String data, que representa a data e
 * hora do jogo, dois arrays do tipo Pergunta onde em um serão adicionadas as respostas que o jogador acertou e no
 * outro as respostas que o jogador errou
 */
public class Jogador implements Serializable, Comparable<Jogador> {
    private String playerName, data;
    private final ArrayList<Pergunta> rightQuestions;
    private final ArrayList<Pergunta> wrongQuestions;
    public Jogador(){
        playerName = "Novo Jogador";
        rightQuestions = new ArrayList<>();
        wrongQuestions = new ArrayList<>();
        data = "";
    }

    /**
     * método que adiciona as perguntas acertadas pelo jogador ao array de rigthQuestions
     * @param novaPergunta pergunta nova a ser adicionada
     */
    public void addRight(Pergunta novaPergunta){
        rightQuestions.add(novaPergunta);
    }

    /**
     * método que adiciona as perguntas erradas pelo jogador ao array de wrongQuestions
     * @param novaPergunta pergunta nova a ser adicionada
     */
    public void addWrong(Pergunta novaPergunta){
        wrongQuestions.add(novaPergunta);
    }

    /**
     * metódo que retorna os pontos totais que o jogador fez no jogo
     * @return pontos totais feitos no jogo
     */
    public int getPoints(){
        int calculo = 0;
        for(Pergunta i: rightQuestions){
            calculo += i.calculatePoints();
        }
        return calculo;
    }

    /**
     * método que armazena a data salva no momento final do jogo
     * @param data String com a data do jogo a ser armazenada
     */
    public void setData(String data){
        this.data = data;
    }

    /**
     * método que compara os pontos de cada jogador, retornando a informação necessária para que a lista de
     * jogadores seja ordenada de forma decrescente (o jogador com maior pontuação em primeiro lugar)
     * @param e objeto a ser comparado
     * @return inteiro representando a comparação entre os dois Jogadores analisados
     */
    public int compareTo(Jogador e) {
        return Integer.compare(e.getPoints(), getPoints());
    }

    /**
     * método que retorna uma string que contem a informação da data em que o jogador jogou o jogo, seus pontos totais e nome
     * @return string com os pontos totais e o nome do jogador
     */
    public String toString(){
        return data + " (" + getPoints() + " pontos) " + playerName;
    }

    /**
     * método que armazena o nome do jogador
     * @param nome nome do jogador
     */
    public void setPlayerName(String nome){
        playerName = nome;
    }
}