package POOTrivia;
import javax.swing.*;
import java.io.Serializable;

/**
 * A class abstract Question é onde serão armazenadas as informações comuns das perguntas e seus repetivos métodos
 * Está classe contêm uma String question, que representa uma pergunta, o int questionPoints, que representa os pontos
 * dessa pergunta e uma String correct, que representa a resposta correta inicializada como vazio pois será alterada
 * assim que a leitura do ficheiro de perguntas for executada
 */
public abstract class Question implements Serializable {
    private final String question;
    private final int questionPoints;
    private String correct;
    public Question(String question){
        this.question = question;
        questionPoints = 5;
        correct = "";
    }

    /**
     * método que retorna os pontos da pergunta
     * @return pontos da pergunta
     */
    public int getQuestionPoints(){
        return questionPoints;
    }

    /**
     * método que retorna o enunciado da pergunta
     * @return String com o enunciado da pergunta
     */
    public String getQuestion(){
        return question;
    }

    /**
     * método que armazena as respostas corretas após ler do ficheiro
     * @param correta resposta correta
     */
    public void setCorrect(String correta){
        correct = correta;
    }

    /**
     * método que retorna a resposta correta
     * @return resposta correta
     */
    public String returnCorrect(){
        return correct;
    }

    /**
     * método que devolve os pontos calculados de cada pergunta
     * @return pontos totais de cada pergunta
     */
    public abstract int calculatePoints();

    /**
     * método que adiciona uma resposta da categoria específica ao array com as respostas dessa categoria, usada para
     * armazenar respostas faceis (respostas apresentadas antes da terceira rodada do jogo)
     * @param newResposta resposta a ser adicionada
     */
    public void addResposta(String newResposta){}

    /**
     * método que adiciona uma resposta de uma categoria específica ao array com as respostas dessa categoria, usada para
     * categorias que possuem respostas dificeis (respostas apresentadas a partir da terceira rodada do jogo)
     * @param newResposta resposta a ser adicionada
     */
    public void addResposta2(String newResposta){}

    /**
     * método implementado nas subclasses para retornar uma lista com as respostas faceis, retornando null caso
     * haja um erro de implementação, pois deve sempre ser executada pela subclasse Arts, Science e Football
     * @return lista com as respostas
     */
    public String[] respostasA(){
        return null;
    }

    /**
     * método implementado nas subclasses para retornar uma lista com as respostas dificeis, retornando null caso
     * haja um erro de implementação, pois deve sempre ser executada pela subclasse Arts, Science e Football
     * @return lista com as respostas
     */
    public String[] respostasB(){
        return null;
    }

    /**
     * método que define o texto dos botões de resposta, de acordo com a rodada em que o jogo se encontra
     * @param buttons lista com os botões
     * @param rodada rodada do jogo
     */
    public void defineTheme(JButton[] buttons, int rodada){
        for(int i = 2; i < buttons.length; i++) buttons[i].setVisible(false);
        buttons[0].setText("True");
        buttons[1].setText("False");
    }

    /**
     * método que troca a imagem que é apresentada ao lado da pergunta, de acordo com a categoria da pergunta
     * @param labelImage label onde será apresentada a imagem
     */
    public abstract void changeImage(JLabel labelImage);

    /**
     * método que armazena a resposta correta (facil) da categoria futebol, executada na leitura do ficheiro
     * @param correta resposta correta
     */
    public void setCorrect1(String correta){
    }

    /**
     * método que armazena a resposta correta (difícil) da categoria futebol, executada na leitura do ficheiro
     * @param correta resposta correta
     */
    public void setCorrect2(String correta){
    }
}
