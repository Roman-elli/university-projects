package POOTrivia;
import Themes.*;
import javax.swing.*;
import java.io.*;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.time.LocalDateTime;

/**
 * The POOTrivia class contains the main methods of the program.
 * This class contains an array of type Question, where the game questions are stored and shuffled
 * whenever the game starts, an array of type Player, where the players are stored, an int numeroRespostas,
 * which is the number of answers for each question, an int rodada, which represents the current round of the game, and
 * the variable jogadorAtivo of type Player, which represents the current player.
 */
public class POOTrivia {
    private final ArrayList<Question> gameQuestions;
    private final ArrayList<Player> players;
    private final int numeroRespostas;
    private int rodada;
    private Player jogadorAtivo;
    public POOTrivia(){
        gameQuestions = new ArrayList<>();
        players = new ArrayList<>();
        numeroRespostas = 6;
        rodada = 0;
        readFile();
        Collections.shuffle(gameQuestions);
        jogadorAtivo = new Player();
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
                Question novaPergunta;
                String line, leitura;
                while((line = br.readLine()) != null){
                    switch (line){
                        case "Arts":
                            novaPergunta = new Arts(br.readLine());
                            addQuestion(novaPergunta);
                            for(int i = 0; i < numeroRespostas; i++){
                                leitura = br.readLine();
                                if(i == 0) novaPergunta.setCorrect(leitura);
                                novaPergunta.addResposta(leitura);
                            }
                            break;
                        case "Science":
                            novaPergunta = new Science(br.readLine());
                            addQuestion(novaPergunta);
                            for(int i = 0; i < numeroRespostas; i++){
                                leitura = br.readLine();
                                if(i == 0) novaPergunta.setCorrect(leitura);
                                novaPergunta.addResposta(leitura);
                            }
                            br.readLine();
                            for(int i = 0; i < numeroRespostas; i++){
                                leitura = br.readLine();
                                if(i == 0) novaPergunta.setCorrect(leitura);
                                novaPergunta.addResposta2(leitura);
                            }
                            break;
                        case "Skiing":
                            novaPergunta = new Skiing(br.readLine());
                            addQuestion(novaPergunta);
                            novaPergunta.setCorrect(br.readLine());
                            break;
                        case "Swimming":
                            novaPergunta = new Swimming(br.readLine());
                            addQuestion(novaPergunta);
                            novaPergunta.setCorrect(br.readLine());
                            break;
                        case "Football":
                            novaPergunta = new Football(br.readLine());
                            addQuestion(novaPergunta);
                            for(int i = 0; i < numeroRespostas; i++){
                                leitura = br.readLine();
                                if(i == 0) novaPergunta.setCorrect1(leitura);
                                novaPergunta.addResposta(leitura);
                            }
                            br.readLine();
                            for(int i = 0; i < numeroRespostas; i++){
                                leitura = br.readLine();
                                if(i == 0) novaPergunta.setCorrect2(leitura);
                                novaPergunta.addResposta2(leitura);
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
        rodada++;
    }

    /**
     * Method that returns the current round of the game
     * @return current round
     */
    public int getRound(){
        return rodada;
    }

    /**
     * Method that adds a question to the array of questions
     * @param novaPergunta question to be added
     */
    public void addQuestion(Question novaPergunta){
        gameQuestions.add(novaPergunta);
    }

    /**
     * Method that returns the question that will be presented in each round
     * @return question to be presented in the current round
     */
    public Question newQuestion(){
        return gameQuestions.get(rodada);
    }

    /**
     * Method that adds a player to the array of players
     * @param novoJogador player to be added
     */
    public void addPlayer(Player novoJogador){
        players.add(novoJogador);
    }

    /**
     * Method that gets the player's name, storing their initials through a split, the date and time when the player
     * is playing the game, using a formatter to generate the desired file name format and returning it
     * @param nomeJogador player’s name
     * @return desired file name
     */
    public String converteTitle(String nomeJogador) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMddHHmm");
        DateTimeFormatter formatter2 = DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm");
        LocalDateTime agora = LocalDateTime.now();
        jogadorAtivo.setData(formatter2.format(agora));

        String[] splitName = nomeJogador.split(" ");
        StringBuilder newName = new StringBuilder();
        for (String i : splitName) {
            newName.append(i.charAt(0));
        }
        return "pootrivia_game_" + formatter.format(agora) + "_" + newName + ".dat";
    }

    /**
     * Method that creates an object file with the desired name, storing a Player object
     * @param nomeJogador player’s name used for the file title
     */
    public void writePlayer(String nomeJogador){
        String nomeFicheiro = "data/save-game/" + converteTitle(nomeJogador);
        File f = new File(nomeFicheiro);
        try (FileOutputStream fos = new FileOutputStream(f);
             ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeObject(jogadorAtivo);
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
        File pasta = new File("data/save-game");
        if (!pasta.exists()) {
            boolean criado = pasta.mkdirs(); // creates all necessary folders
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
        
        File pasta = new File("data/save-game");

        if (pasta.isDirectory()) {
            File[] arquivos = pasta.listFiles();

            if (arquivos != null) {
                for (File arquivo : arquivos) {
                    try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(arquivo))) {
                        Player novoJogador = (Player) ois.readObject();
                        addPlayer(novoJogador);

                    } catch (IOException | ClassNotFoundException ex) {
                        System.out.println("Error reading file: " + arquivo.getName());
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
        return jogadorAtivo;
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
        if(rodada != 0){
            Collections.shuffle(gameQuestions);
            jogadorAtivo = new Player();
            rodada = 0;
        }
    }
}