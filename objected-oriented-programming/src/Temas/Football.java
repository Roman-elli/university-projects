package Temas;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * A class Football armazena os dados especificos das perguntas e respostas relacionados com esta categoria
 * Esta classe contêm dois arrays um com as respostas dos jogadores(faceis) e outro com as respostas das camisas(dificeis),
 * e uma string correct1 que armazena a resposta correta dos jogadores e uma string correct2 que armazena a resposta
 * correta das camisas
 */
public class Football extends Sports{
    private final ArrayList<String> respostasJogador;
    private final ArrayList<String> respostasCamisa;
    private String correct1, correct2;

    public Football(String question){
        super(question);
        respostasJogador = new ArrayList<>();
        respostasCamisa = new ArrayList<>();
        correct1 = "";
        correct2 = "";
    }

    /**
     * método que retorna os pontos da pergunta, caso esta seja respondida corretamente
     * @return pontos da pergunta
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + super.getMajoracao() + 1;
    }

    /**
     * método que adiciona uma resposta de Football ao array com as respostas dos jogadores
     * @param newFutebol resposta a ser adicionada
     */
    @Override
    public void addResposta(String newFutebol){
        respostasJogador.add(newFutebol);
    }

    /**
     * método que adiciona uma resposta de Football ao array com as respostas das camisas
     * @param newFutebol resposta a ser adicionada
     */
    @Override
    public void addResposta2(String newFutebol){
        respostasCamisa.add(newFutebol);
    }

    /**
     * método que embaralha as seis respostas de Football relativas aos jogadores, define a correct1 como resposta principal e retorna uma lista com as
     * respostas dos jogadores(fáceis), sendo utilizado apenas na rodada 1 e 2 do jogo
     * @return lista com as seis respostas fáceis
     */
    @Override
    public String[] respostasA(){
        String[] random = new String[6];
        setCorrect(correct1);
        Collections.shuffle(respostasJogador);
        for(int i = 0; i < random.length; i++){
            random[i] = respostasJogador.get(i);
        }
        return random;
    }

    /**
     * método que embaralha as seis respostas de Football relativas as camisas, define a correct2 como resposta principal e retorna uma lista com as
     * respostas das camisas(difíceis), sendo utilizado quando a rodada é igual ou superior a três
     * @return lista com as seis respostas difíceis
     */
    @Override
    public String[] respostasB(){
        String[] random = new String[6];
        setCorrect(correct2);
        Collections.shuffle(respostasCamisa);
        for(int i = 0; i < random.length; i++){
            random[i] = respostasCamisa.get(i);
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
        else{
            respostas = respostasB();
        }
        for(int i = 0; i < respostas.length; i++) buttons[i].setText(respostas[i]);
    }

    /**
     * método que insere à label a imagem de Football
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Football.png");
        labelImage.setIcon(image);
    }

    /**
     * método que armazena a resposta correta relativamente aos jogadores(facil), executada na leitura do ficheiro de perguntas
     * @param correta resposta correta
     */
    @Override
    public void setCorrect1(String correta){
        correct1 = correta;
    }

    /**
     * método que armazena a resposta correta relativamente as camisas(dificil), executada na leitura do ficheiro de perguntas
     * @param correta resposta correta
     */
    @Override
    public void setCorrect2(String correta){
        correct2 = correta;
    }
}
