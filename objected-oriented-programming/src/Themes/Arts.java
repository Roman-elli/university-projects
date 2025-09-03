package Themes;
import POOTrivia.Question;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * The Arts class stores the specific data of questions and answers related to this category.
 * This class contains an array with the art answers.
 */
public class Arts extends Question{
    private final ArrayList<String> respostasArtes;
    public Arts(String question){
        super(question);
        respostasArtes = new ArrayList<>();
    }

    /**
     * Method that calculates the points of a question if it is answered correctly or if necessary
     * @return points of the question
     */
    public int calculatePoints(){
        return super.getQuestionPoints() * 10;
    }

    /**
     * Method that adds an art answer to the array of answers
     * @param newArt answer to be added
     */
    @Override
    public void addResposta(String newArt){
        respostasArtes.add(newArt);
    }

    /**
     * Method that shuffles three art answers including the correct one, returning the list with these three answers,
     * used only in rounds 1 and 2 of the game
     * @return list with three answers
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
     * Method that shuffles six art answers, returning a list with these answers, used only
     * when the round is equal to or greater than three
     * @return list with six answers
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
     * Method that sets the button text with the corresponding answers according to the current round
     * @param buttons list of buttons
     * @param rodada current round of the game
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
     * Method that sets the art image on the label
     * @param labelImage label where the image will be displayed
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Arts.png");
        labelImage.setIcon(image);
    }
}