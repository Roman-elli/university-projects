package POOTrivia;
import javax.swing.*;
import java.io.Serializable;

/**
 * The abstract class Question stores the common information of questions and their respective methods.
 * This class contains a String question, which represents the question text, an int questionPoints, which represents the points
 * for that question, and a String correct, which represents the correct answer initialized as empty and will be set
 * when the questions file is read.
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
     * Method that returns the points of the question
     * @return points of the question
     */
    public int getQuestionPoints(){
        return questionPoints;
    }

    /**
     * Method that returns the text of the question
     * @return String with the question text
     */
    public String getQuestion(){
        return question;
    }

    /**
     * Method that stores the correct answers after reading from the file
     * @param correta correct answer
     */
    public void setCorrect(String correta){
        correct = correta;
    }

    /**
     * Method that returns the correct answer
     * @return correct answer
     */
    public String returnCorrect(){
        return correct;
    }

    /**
     * Method that returns the calculated points of each question
     * @return total points of the question
     */
    public abstract int calculatePoints();

    /**
     * Method that adds an answer of the specific category to the array of answers of that category,
     * used to store easy answers (answers presented before the third round of the game)
     * @param newResposta answer to be added
     */
    public void addResposta(String newResposta){}

    /**
     * Method that adds an answer of the specific category to the array of answers of that category,
     * used for categories that have difficult answers (answers presented from the third round of the game)
     * @param newResposta answer to be added
     */
    public void addResposta2(String newResposta){}

    /**
     * Method implemented in subclasses to return a list of easy answers, returning null in case
     * of implementation error, should always be executed by the subclasses Arts, Science, and Football
     * @return list of answers
     */
    public String[] respostasA(){
        return null;
    }

    /**
     * Method implemented in subclasses to return a list of difficult answers, returning null in case
     * of implementation error, should always be executed by the subclasses Arts, Science, and Football
     * @return list of answers
     */
    public String[] respostasB(){
        return null;
    }

    /**
     * Method that sets the text of the answer buttons according to the current round of the game
     * @param buttons list of buttons
     * @param rodada current round of the game
     */
    public void defineTheme(JButton[] buttons, int rodada){
        for(int i = 2; i < buttons.length; i++) buttons[i].setVisible(false);
        buttons[0].setText("True");
        buttons[1].setText("False");
    }

    /**
     * Method that changes the image displayed next to the question according to the category of the question
     * @param labelImage label where the image will be displayed
     */
    public abstract void changeImage(JLabel labelImage);

    /**
     * Method that stores the correct (easy) answer for the Football category, executed when reading the file
     * @param correta correct answer
     */
    public void setCorrect1(String correta){
    }

    /**
     * Method that stores the correct (difficult) answer for the Football category, executed when reading the file
     * @param correta correct answer
     */
    public void setCorrect2(String correta){
    }
}