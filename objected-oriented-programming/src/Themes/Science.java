package Themes;
import POOTrivia.Question;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * The Science class stores the specific data of questions and answers related to this category.
 * This class contains two arrays: one with easy Science answers and another with difficult Science answers.
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
     * Method that returns the points of the question if it is answered correctly
     * @return points of the question
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + 5;
    }

    /**
     * Method that adds a Science answer to the array of easy answers
     * @param newCiencia answer to be added
     */
    @Override
    public void addResposta(String newCiencia){
        respostasFaceis.add(newCiencia);
    }

    /**
     * Method that adds a Science answer to the array of difficult answers
     * @param newCiencia answer to be added
     */
    @Override
    public void addResposta2(String newCiencia){
        respostasDificeis.add(newCiencia);
    }

    /**
     * Method that shuffles the six easy Science answers and returns a list of them,
     * used only in rounds 1 and 2 of the game
     * @return list with six answers
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
     * Method that shuffles the six difficult Science answers and returns a list of them,
     * used only when the round is equal or greater than three
     * @return list with six answers
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
        else respostas = respostasB();
        for(int i = 0; i < respostas.length; i++) buttons[i].setText(respostas[i]);
    }

    /**
     * Method that sets the Science image on the label
     * @param labelImage label where the image will be displayed
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Science.png");
        labelImage.setIcon(image);
    }
}