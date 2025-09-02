package Temas;
import POOTrivia.Question;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * A class Science armazena os dados especificos das perguntas e respostas relacionadas com esta categoria
 * Esta classe contêm dois arrays um com as respostas faceis e outro com as respostas dificeis de ciencias
 */

public class Science extends Question{
    private final ArrayList<String> respostasFaceis;
    private final ArrayList<String> respostasDificeis;

    public Science(String question){
        super(question);
        respostasFaceis = new ArrayList<>();
        respostasDificeis = new ArrayList<>();
    }

    /**
     * método que retorna os pontos da pergunta, caso esta seja respondida corretamente
     * @return pontos da pergunta
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + 5;
    }

    /**
     * método que adiciona uma resposta de Science ao array com as respostas faceis
     * @param newCiencia resposta a ser adicionada
     */
    @Override
    public void addResposta(String newCiencia){
        respostasFaceis.add(newCiencia);
    }

    /**
     * método que adiciona uma resposta de Science ao array com as respostas dificeis
     * @param newCiencia resposta a ser adiciona
     */
    @Override
    public void addResposta2(String newCiencia){
        respostasDificeis.add(newCiencia);
    }

    /**
     * método que embaralha as seis respostas de Science faceis e retorna uma lista com essas
     * respostas, sendo utilizado apenas na rodada 1 e 2 do jogo
     * @return lista com as seis respostas
     */
    @Override
    public String[] respostasA(){
        String[] random = new String[6];
        Collections.shuffle(respostasFaceis);
        for(int i = 0; i < random.length; i++){
            random[i] = respostasFaceis.get(i);
        }
        return random;
    }

    /**
     * método que embaralha as seis respostas de Science dificeis e retorna uma lista com essas
     * respostas, sendo utilizado apenas quando a rodada é igual ou superior a três
     * @return lista com as seis respostas
     */
    @Override
    public String[] respostasB(){
        String[] random = new String[6];
        Collections.shuffle(respostasDificeis);
        for(int i = 0; i < random.length; i++){
            random[i] = respostasDificeis.get(i);
        }
        return random;
    }

    /**
     * método que escreve nos botôes as respostas correspondentes de acordo com a rodada em que o jogo se encontra
     * @param buttons lista com os botões
     * @param rodada rodada do jogo
     */
    @Override
    public void defineTheme(JButton[] buttons, int rodada){
        String[] respostas;
        if(rodada < 2){
            respostas = respostasA();
        }
        else respostas = respostasB();
        for(int i = 0; i < respostas.length; i++) buttons[i].setText(respostas[i]);
    }

    /**
     * método que insere à label a imagem de Science
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Science.png");
        labelImage.setIcon(image);
    }
}
