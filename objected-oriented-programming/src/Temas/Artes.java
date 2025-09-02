package Temas;
import POOTrivia.Pergunta;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * A class Arte armazena os dados especificos das perguntas e respostas relacionados com esta categoria
 * Esta classe contêm um array com as respostas de arte
 */
public class Artes extends Pergunta{
    private final ArrayList<String> respostasArtes;
    public Artes(String question){
        super(question);
        respostasArtes = new ArrayList<>();
    }

    /**
     * método que calcula os pontos de uma pergunta caso esta seja respondida corretamente ou caso seja necessário
     * @return pontos da pergunta
     */
    public int calculatePoints(){
        return super.getQuestionPoints() * 10;
    }

    /**
     * método que adiciona uma resposta de artes ao array com as respostas
     * @param newArt resposta a ser adicionada
     */
    @Override
    public void addResposta(String newArt){
        respostasArtes.add(newArt);
    }

    /**
     * método que embaralha três respostas de artes incluindo a correta, devolvendo a lista com essas três respostas,
     * sendo apenas utilizado na rodada 1 e 2 do jogo
     * @return lista com tres respostas
     */
    @Override
    public String[] respostasA(){
        String[] random = new String[3];
        int respostaRandom = (int)(Math.random() * 3);
        random[respostaRandom] = returnCorrect();
        Collections.shuffle(respostasArtes);
        String test;
        for(int i = 0; i < random.length; i++){
            if(i != respostaRandom){
                 test = respostasArtes.get(i);
                 if(!test.equals(random[respostaRandom])){
                     random[i] = test;
                 }
                 else{
                     random[i] = respostasArtes.getLast();
                 }
            }
        }
        return random;
    }

    /**
     * método que embaralha as seis respostas de artes, retornando uma lista com essas respostas, sendo utilizado apenas
     * quando a rodada é igual ou superior a três
     * @return lista com as seis respostas
     */
    @Override
    public String[] respostasB(){
        String[] random = new String[6];
        Collections.shuffle(respostasArtes);
        for(int i = 0; i < random.length; i++){
            random[i] = respostasArtes.get(i);
        }
        return random;
    }

    /**
     * método que escreve nos botôes as respostas correspondentes de acordo com a rodada
     * @param buttons lista com os botões
     * @param rodada rodada do jogo
     */
    @Override
    public void defineTheme(JButton[] buttons, int rodada){
        String[] respostas;
        if(rodada < 2){
            for(int i = 3; i < buttons.length; i++) buttons[i].setVisible(false);
            respostas = respostasA();
        }
        else respostas = respostasB();

        for(int i = 0; i < respostas.length; i++) buttons[i].setText(respostas[i]);
    }

    /**
     * método que insere à label a imagem de artes
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Artes.png");
        labelImage.setIcon(image);
    }
}
