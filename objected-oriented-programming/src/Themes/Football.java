package Themes;
import javax.swing.*;
import java.util.ArrayList;
import java.util.Collections;

/**
 * The Football class stores the specific data of questions and answers related to this category.
 * This class contains two arrays: one with player answers (easy) and another with jersey answers (difficult),
 * and a string easyAnswer that stores the correct player answer and a string hardAnswer that stores the correct
 * jersey answer.
 */
public class Football extends Sports{
    private final ArrayList<String> easyAnswerList;
    private final ArrayList<String> hardAnswerList;
    private String easyAnswer, hardAnswer;

    public Football(String question){
        super(question);
        easyAnswerList = new ArrayList<>();
        hardAnswerList = new ArrayList<>();
        easyAnswer = "";
        hardAnswer = "";
    }

    /**
     * Method that returns the points of the question if it is answered correctly
     * @return points of the question
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + super.getScoreWeight() + 1;
    }

    /**
     * Method that adds a Football answer to the array of player answers
     * @param newFootballAnswer answer to be added
     */
    @Override
    public void addEasyAnswer(String newFootballAnswer){
        easyAnswerList.add(newFootballAnswer);
    }

    /**
     * Method that adds a Football answer to the array of jersey answers
     * @param newFootballAnswer answer to be added
     */
    @Override
    public void addHardAnswer(String newFootballAnswer){
        hardAnswerList.add(newFootballAnswer);
    }

    /**
     * Method that shuffles the six Football player answers, sets easyAnswer as the main answer, 
     * and returns a list of player answers (easy), used only in rounds 1 and 2 of the game
     * @return list with six easy answers
     */
    @Override
    public String[] easyAnswersManage(){
        String[] random = new String[6];
        setCorrect(easyAnswer);
        Collections.shuffle(easyAnswerList);
        for(int i = 0; i < random.length; i++){
            random[i] = easyAnswerList.get(i);
        }
        return random;
    }

    /**
     * Method that shuffles the six Football jersey answers, sets hardAnswer as the main answer, 
     * and returns a list of jersey answers (difficult), used when the round is equal or greater than three
     * @return list with six difficult answers
     */
    @Override
    public String[] hardAnswersManage(){
        String[] random = new String[6];
        setCorrect(hardAnswer);
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
        else{
            answerList = hardAnswersManage();
        }
        for(int i = 0; i < answerList.length; i++) buttons[i].setText(answerList[i]);
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
     * @param rightAnswer correct answer
     */
    @Override
    public void setCorrect1(String rightAnswer){
        easyAnswer = rightAnswer;
    }

    /**
     * Method that stores the correct answer for jerseys (difficult), executed when reading the questions file
     * @param rightAnswer correct answer
     */
    @Override
    public void setCorrect2(String rightAnswer){
        hardAnswer = rightAnswer;
    }
}