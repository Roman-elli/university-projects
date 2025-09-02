package POOTrivia;
import java.io.Serializable;
import java.util.ArrayList;

/**
 * The Player class is where the information of the players will be stored.
 * This class contains a string playerName, which represents the player's name, a String date, which represents the date and
 * time of the game, and two arrays of type Question: one will store the questions the player answered correctly,
 * and the other will store the questions the player answered incorrectly.
 */
public class Player implements Serializable, Comparable<Player> {
    private String playerName, data;
    private final ArrayList<Question> rightQuestions;
    private final ArrayList<Question> wrongQuestions;
    public Player(){
        playerName = "New Player";
        rightQuestions = new ArrayList<>();
        wrongQuestions = new ArrayList<>();
        data = "";
    }

    /**
     * Method that adds the questions the player answered correctly to the rightQuestions array
     * @param newQuestion the new question to be added
     */
    public void addRight(Question novaPergunta){
        rightQuestions.add(novaPergunta);
    }

    /**
     * Method that adds the questions the player answered incorrectly to the wrongQuestions array
     * @param newQuestion the new question to be added
     */
    public void addWrong(Question novaPergunta){
        wrongQuestions.add(novaPergunta);
    }

    /**
     * Method that returns the total points the player scored in the game
     * @return total points scored in the game
     */
    public int getPoints(){
        int points = 0;
        for(Question i: rightQuestions){
            points += i.calculatePoints();
        }
        return points;
    }

    /**
     * Method that stores the date recorded at the end of the game
     * @param date String containing the date of the game to be stored
     */
    public void setData(String data){
        this.data = data;
    }

    /**
     * Method that compares the points of each player, returning the necessary information 
     * so that the list of players can be sorted in descending order (the player with the highest score first)
     * @param e object to be compared
     * @return integer representing the comparison between the two analyzed players
     */
    public int compareTo(Player e) {
        return Integer.compare(e.getPoints(), getPoints());
    }

    /**
     * Method that returns a string containing the information of the date the player played the game, 
     * their total points, and name
     * @return string with the player's total points and name
     */
    public String toString(){
        return data + " (" + getPoints() + " points) " + playerName;
    }

    /**
    * Method that stores the player's name
    * @param name the player's name
    */
    public void setPlayerName(String nome){
        playerName = nome;
    }
}