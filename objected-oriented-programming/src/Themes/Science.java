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
    private final ArrayList<String> easyAnswerList;
    private final ArrayList<String> hardAnswerList;

    public Science(String question){
        super(question);
        easyAnswerList = new ArrayList<>();
        hardAnswerList = new ArrayList<>();
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
     * @param newScienceAnswer answer to be added
     */
    @Override
    public void addEasyAnswer(String newScienceAnswer){
        easyAnswerList.add(newScienceAnswer);
    }

    /**
     * Method that adds a Science answer to the array of difficult answers
     * @param newScienceAnswer answer to be added
     */
    @Override
    public void addHardAnswer(String newScienceAnswer){
        hardAnswerList.add(newScienceAnswer);
    }

    /**
     * Method that shuffles the six easy Science answers and returns a list of them,
     * used only in rounds 1 and 2 of the game
     * @return list with six answers
     */
    @Override
    public String[] easyAnswersManage(){
        String[] random = new String[6];
        Collections.shuffle(easyAnswerList);
        for(int i = 0; i < random.length; i++){
            random[i] = easyAnswerList.get(i);
        }
        return random;
    }

    /**
     * Method that shuffles the six difficult Science answers and returns a list of them,
     * used only when the round is equal or greater than three
     * @return list with six answers
     */
    @Override
    public String[] hardAnswersManage(){
        String[] random = new String[6];
        Collections.shuffle(hardAnswerList);
        for(int i = 0; i < random.length; i++){
            random[i] = hardAnswerList.get(i);
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
            answerList = easyAnswersManage();
        }
        else answerList = hardAnswersManage();
        for(int i = 0; i < answerList.length; i++) buttons[i].setText(answerList[i]);
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