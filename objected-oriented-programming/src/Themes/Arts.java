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
    private final ArrayList<String> artAnswerList;
    public Arts(String question){
        super(question);
        artAnswerList = new ArrayList<>();
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
    public void addEasyAnswer(String newArt){
        artAnswerList.add(newArt);
    }

    /**
     * Method that shuffles three art answers including the correct one, returning the list with these three answers,
     * used only in rounds 1 and 2 of the game
     * @return list with three answers
     */
    @Override
    public String[] easyAnswersManage(){
        String[] random = new String[3];
        int randomChoice = (int)(Math.random() * 3);
        random[randomChoice] = returnCorrect();
        Collections.shuffle(artAnswerList);
        String test;
        for(int i = 0; i < random.length; i++){
            if(i != randomChoice){
                 test = artAnswerList.get(i);
                 if(!test.equals(random[randomChoice])){
                     random[i] = test;
                 }
                 else{
                     random[i] = artAnswerList.getLast();
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
    public String[] hardAnswersManage(){
        String[] random = new String[6];
        Collections.shuffle(artAnswerList);
        for(int i = 0; i < random.length; i++){
            random[i] = artAnswerList.get(i);
        }
        return random;
    }

    /**
     * Method that sets the button text with the corresponding answers according to the current round
     * @param buttons list of buttons
     * @param round current round of the game
     */
    @Override
    public void defineTheme(JButton[] buttons, int round){
        String[] answerList;
        if(round < 2){
            for(int i = 3; i < buttons.length; i++) buttons[i].setVisible(false);
            answerList = easyAnswersManage();
        }
        else answerList = hardAnswersManage();

        for(int i = 0; i < answerList.length; i++) buttons[i].setText(answerList[i]);
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