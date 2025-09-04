package core;
import themes.*;
import javax.swing.*;
import java.io.*;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.time.LocalDateTime;

/**
 * The pootrivia class contains the main methods of the program.
 * This class contains an array of type Question, where the game questions are stored and shuffled
 * whenever the game starts, an array of type Player, where the players are stored, an int answerCounter,
 * which is the number of answers for each question, an int round, which represents the current round of the game, and
 * the variable activePlayer of type Player, which represents the current player.
 */
public class GameEngine {
    private final ArrayList<Question> gameQuestions;
    private final ArrayList<Player> players;
    private final int answerCounter;
    private int round;
    private Player activePlayer;
    
    public GameEngine(){
        gameQuestions = new ArrayList<>();
        players = new ArrayList<>();
        answerCounter = CoreConfig.GAME_ANSWER_COUNTER;
        round = 0;
        readFile();
        Collections.shuffle(gameQuestions);
        activePlayer = new Player();
        readPlayers();
    }

    /**
     * Method that reads the questions file, checking if the file exists and, if it does, reads and stores
     * each question with its respective answers in its respective category. Then, the first answer (correct answer)
     * of each question is stored using the setCorrect method, which is used only when the category is Arts, Science, or Football (also using
     * setCorrect2, because for each question of this type there are two types of answers) and in the Swimming and Skiing categories
     * the method turnTrue is used, which will change the previously initialized answer strings from "false" to "true".
     */
    public void readFile(){
        File f = new File("assets/game-questions/questions.txt");
        if(f.exists() && f.isFile()) {
            try {
                FileReader fr = new FileReader(f);
                BufferedReader br = new BufferedReader(fr);
                Question newQuestion;
                String line, temp_read;
                while((line = br.readLine()) != null){
                    switch (line){
                        case "Arts":
                            newQuestion = new Arts(br.readLine());
                            addQuestion(newQuestion);
                            for(int i = 0; i < answerCounter; i++){
                                temp_read = br.readLine();
                                if(i == 0) newQuestion.setCorrect(temp_read);
                                newQuestion.addEasyAnswer(temp_read);
                            }
                            break;
                        case "Science":
                            newQuestion = new Science(br.readLine());
                            addQuestion(newQuestion);
                            for(int i = 0; i < answerCounter; i++){
                                temp_read = br.readLine();
                                if(i == 0) newQuestion.setCorrect(temp_read);
                                newQuestion.addEasyAnswer(temp_read);
                            }
                            br.readLine();
                            for(int i = 0; i < answerCounter; i++){
                                temp_read = br.readLine();
                                if(i == 0) newQuestion.setCorrect(temp_read);
                                newQuestion.addHardAnswer(temp_read);
                            }
                            break;
                        case "Skiing":
                            newQuestion = new Skiing(br.readLine());
                            addQuestion(newQuestion);
                            newQuestion.setCorrect(br.readLine());
                            break;
                        case "Swimming":
                            newQuestion = new Swimming(br.readLine());
                            addQuestion(newQuestion);
                            newQuestion.setCorrect(br.readLine());
                            break;
                        case "Football":
                            newQuestion = new Football(br.readLine());
                            addQuestion(newQuestion);
                            for(int i = 0; i < answerCounter; i++){
                                temp_read = br.readLine();
                                if(i == 0) newQuestion.setCorrect1(temp_read);
                                newQuestion.addEasyAnswer(temp_read);
                            }
                            br.readLine();
                            for(int i = 0; i < answerCounter; i++){
                                temp_read = br.readLine();
                                if(i == 0) newQuestion.setCorrect2(temp_read);
                                newQuestion.addHardAnswer(temp_read);
                            }
                            break;
                        default:
                            System.out.println("Theme does not exist.");
                        }
                        br.readLine();
                    }
                br.close();
            } catch (FileNotFoundException ex) {
                System.out.println("Error opening text file.");
            } catch (IOException ex) {
                System.out.println("Error reading text file.");
            }
        } else {
            System.out.println("File does not exist.");
        }
    }

    /**
     * Method that advances the game round
     */
    public void nextRound(){
        round++;
    }

    /**
     * Method that returns the current round of the game
     * @return current round
     */
    public int getRound(){
        return round;
    }

    /**
     * Method that adds a question to the array of questions
     * @param newQuestion question to be added
     */
    public void addQuestion(Question newQuestion){
        gameQuestions.add(newQuestion);
    }

    /**
     * Method that returns the question that will be presented in each round
     * @return question to be presented in the current round
     */
    public Question newQuestion(){
        return gameQuestions.get(round);
    }

    /**
     * Method that adds a player to the array of players
     * @param newPlayer player to be added
     */
    public void addPlayer(Player newPlayer){
        players.add(newPlayer);
    }

    /**
     * Method that gets the player's name, storing their initials through a split, the date and time when the player
     * is playing the game, using a formatter to generate the desired file name format and returning it
     * @param playerName player’s name
     * @return desired file name
     */
    public String converteTitle(String playerName) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMddHHmm");
        DateTimeFormatter formatter2 = DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm");
        LocalDateTime actualTime = LocalDateTime.now();
        activePlayer.setData(formatter2.format(actualTime));

        String[] splitName = playerName.split(" ");
        StringBuilder newName = new StringBuilder();
        for (String i : splitName) {
            newName.append(i.charAt(0));
        }
        return "pootrivia_game_" + formatter.format(actualTime) + "_" + newName + ".dat";
    }

    /**
     * Method that creates an object file with the desired name, storing a Player object
     * @param playerName player’s name used for the file title
     */
    public void writePlayer(String playerName){
        String fileName = CoreConfig.SAVE_GAME_PATH + converteTitle(playerName);
        File f = new File(fileName);
        try (FileOutputStream fos = new FileOutputStream(f);
             ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeObject(activePlayer);
        } catch (FileNotFoundException ex) {
            System.out.println("Error creating file.");
        } catch (IOException ex) {
            System.out.println("Error writing to file.");
        }
    }

    /**
     * Method that sorts the list of players according to their total points
     */
    public void ordenaPlayers(){
        Collections.sort(players);
    }


    public void ensureSaveFolderExists() {
        File dataFolder = new File(CoreConfig.SAVE_GAME_PATH);
        if (!dataFolder.exists()) {
            boolean criado = dataFolder.mkdirs(); // creates all necessary folders
            if (criado) {
                System.out.println("Folder data/save-game created successfully!");
            } else {
                System.out.println("Failed to create folder data/save-game.");
            }
        }
    }
    
    /**
     * Method that reads the player objects file, storing the players in the players list
     */
    public void readPlayers() {
        ensureSaveFolderExists();
        
        File dataFolder = new File("data/save-game");

        if (dataFolder.isDirectory()) {
            File[] fileList = dataFolder.listFiles();

            if (fileList != null) {
                for (File fileUnit : fileList) {
                    try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(fileUnit))) {
                        Player newPlayer = (Player) ois.readObject();
                        addPlayer(newPlayer);

                    } catch (IOException | ClassNotFoundException ex) {
                        System.out.println("Error reading file: " + fileUnit.getName());
                    }
                }
            }
        } else {
            System.out.println("The provided path is not a directory.");
        }
    }

    /**
     * Method that returns the current player of the game
     * @return current player
     */
    public Player getPlayer(){
        return activePlayer;
    }

    /**
     * Method that places the top three players in the ranking positions, always checking for the existence of players in the list
     * @param player1 JLabel first place
     * @param player2 JLabel second place
     * @param player3 JLabel third place
     */
    public void getWinner(JLabel player1, JLabel player2, JLabel player3){
        ordenaPlayers();
        if(!players.isEmpty())player1.setText(players.get(0).toString());
        if(players.size() > 1) player2.setText(players.get(1).toString());
        if(players.size() > 2) player3.setText(players.get(2).toString());
    }

    /**
     * Method that resets the game when the player decides to play again, generating a new player, setting the round to 0
     * and shuffling the list of questions again so that new questions are generated for the next game
     */
    public void reset(){
        if(round != 0){
            Collections.shuffle(gameQuestions);
            activePlayer = new Player();
            round = 0;
        }
    }
}