package Themes;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * The Football class stores the specific data of questions and answers related to this category.
 * This class contains two arrays: one with player answers (easy) and another with jersey answers (difficult),
 * and a string correct1 that stores the correct player answer and a string correct2 that stores the correct
 * jersey answer.
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
     * Method that returns the points of the question if it is answered correctly
     * @return points of the question
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + super.getMajoracao() + 1;
    }

    /**
     * Method that adds a Football answer to the array of player answers
     * @param newFutebol answer to be added
     */
    @Override
    public void addResposta(String newFutebol){
        respostasJogador.add(newFutebol);
    }

    /**
     * Method that adds a Football answer to the array of jersey answers
     * @param newFutebol answer to be added
     */
    @Override
    public void addResposta2(String newFutebol){
        respostasCamisa.add(newFutebol);
    }

    /**
     * Method that shuffles the six Football player answers, sets correct1 as the main answer, 
     * and returns a list of player answers (easy), used only in rounds 1 and 2 of the game
     * @return list with six easy answers
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
     * Method that shuffles the six Football jersey answers, sets correct2 as the main answer, 
     * and returns a list of jersey answers (difficult), used when the round is equal or greater than three
     * @return list with six difficult answers
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
     * Method that sets the button text with the corresponding answers according to the current round
     * @param buttons list of buttons
     * @param rodada current round of the game
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
     * Method that sets the Football image on the label
     * @param labelImage label where the image will be displayed
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Football.png");
        labelImage.setIcon(image);
    }

    /**
     * Method that stores the correct answer for players (easy), executed when reading the questions file
     * @param correta correct answer
     */
    @Override
    public void setCorrect1(String correta){
        correct1 = correta;
    }

    /**
     * Method that stores the correct answer for jerseys (difficult), executed when reading the questions file
     * @param correta correct answer
     */
    @Override
    public void setCorrect2(String correta){
        correct2 = correta;
    }
}