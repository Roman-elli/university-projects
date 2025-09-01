package POOTrivia;
import Temas.*;
import javax.swing.*;
import java.io.*;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.time.LocalDateTime;

/**
 * A class POOTrivia é onde se encontram os principais métodos do programa.
 * Esta classe contêm um array do tipo Pergunta, onde serão armazenadas as perguntas do jogo que são embaralhadas por meio de um shuffle
 * sempre que o jogo começa, um array do tipo Jogador, onde serão armazenados os jogadores, um int numeroRespostas,
 * onde está o número de respostas de cada pergunta e um int rodada, que representa em que rodada do jogo estamos e a
 * variável jogadorAtivo do tipo Jogador, que representa o jogador atual
 */
public class POOTrivia {
    private final ArrayList<Pergunta> gameQuestions;
    private final ArrayList<Jogador> players;
    private final int numeroRespostas;
    private int rodada;
    private Jogador jogadorAtivo;
    public POOTrivia(){
        gameQuestions = new ArrayList<>();
        players = new ArrayList<>();
        numeroRespostas = 6;
        rodada = 0;
        readFile();
        Collections.shuffle(gameQuestions);
        jogadorAtivo = new Jogador();
        readPlayers();
    }

    /**
     * método que lê o ficheiro das perguntas, analisando se este ficheiro existe e, caso exista, efetua a leitura armazenando
     * cada pergunta com as respetivas respostas na sua respetiva categoria. Em seguida, a primeira resposta(resposta correta)
     * de cada pergunta é armazenada por meio do metodo setCorrect, o qual é utilizado apenas quando a categoria é Artes, Ciencias ou Futebol (utilizando
     * neste também setCorrect2, pois para cada pergunta desta modalidade existe dois tipos de resposta) e nas categorias de Natação e Ski
     * é utilizado o método turnTrue que ira tornar as strings de respostas inicializadas anteriormente em "falso" como "verdadeiro"
     */
    public void readFile(){
        File f = new File("assets/game-questions/Perguntas.txt");
        if(f.exists() && f.isFile()) {
            try {
                FileReader fr = new FileReader(f);
                BufferedReader br = new BufferedReader(fr);
                Pergunta novaPergunta;
                String line, leitura;
                while((line = br.readLine()) != null){
                    switch (line){
                        case "Artes":
                            novaPergunta = new Artes(br.readLine());
                            addQuestion(novaPergunta);
                            for(int i = 0; i < numeroRespostas; i++){
                                leitura = br.readLine();
                                if(i == 0) novaPergunta.setCorrect(leitura);
                                novaPergunta.addResposta(leitura);
                            }
                            break;
                        case "Ciências":
                            novaPergunta = new Ciencias(br.readLine());
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
                        case "Ski":
                            novaPergunta = new Ski(br.readLine());
                            addQuestion(novaPergunta);
                            novaPergunta.setCorrect(br.readLine());
                            break;
                        case "Natação":
                            novaPergunta = new Natacao(br.readLine());
                            addQuestion(novaPergunta);
                            novaPergunta.setCorrect(br.readLine());
                            break;
                        case "Futebol":
                            novaPergunta = new Futebol(br.readLine());
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
                            System.out.println("Tema não existe.");
                        }
                        br.readLine();
                    }
                br.close();
            } catch (FileNotFoundException ex) {
                System.out.println("Erro a abrir ficheiro de texto.");
            } catch (IOException ex) {
                System.out.println("Erro a ler ficheiro de texto.");
            }
        } else {
            System.out.println("Ficheiro não existe.");
        }
    }

    /**
     * método que avança a rodada do jogo
     */
    public void nextRound(){
        rodada++;
    }

    /**
     * método que retorna em que rodada do jogo nos encontramos
     * @return rodada atual
     */
    public int getRound(){
        return rodada;
    }

    /**
     * método que adiciona as perguntas ao array de perguntas
     * @param novaPergunta pergunta a ser adiciona
     */
    public void addQuestion(Pergunta novaPergunta){
        gameQuestions.add(novaPergunta);
    }

    /**
     * método que retorna a questão que será apresentada em cada rodada
     * @return questão que será apresentada em cada rodada
     */
    public Pergunta newQuestion(){
        return gameQuestions.get(rodada);
    }

    /**
     * método que adiciona o jogador no array de jogadores
     * @param novoJogador jogador a ser adicionado
     */
    public void addPlayer(Jogador novoJogador){
        players.add(novoJogador);
    }

    /**
     * método que pega o nome do jogador, armazenando as suas iniciais atravês de um split, a data e a hora do momento em que o jogador
     * está jogando o jogo, sendo utilizado um format para que o formato pretendido para o nome do ficheiro seja gerado e retornado
     * @param nomeJogador nome do jogador
     * @return nome do ficheiro pretendido
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
        return "pootrivia_jogo_" + formatter.format(agora) + "_" + newName + ".dat";
    }

    /**
     * método que cria um ficheiro de objetos com o nome pretendido armazenando  um objeto do tipo jogador
     * @param nomeJogador nome do jogador utilizado para o título do ficheiro
     */
    public void writePlayer(String nomeJogador){
        String nomeFicheiro = "data/save-game/" + converteTitle(nomeJogador);
        File f = new File(nomeFicheiro);
        try (FileOutputStream fos = new FileOutputStream(f);
             ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeObject(jogadorAtivo);
        } catch (FileNotFoundException ex) {
            System.out.println("Erro ao criar ficheiro.");
        } catch (IOException ex) {
            System.out.println("Erro ao escrever para o ficheiro.");
        }
    }

    /**
     * método que ordena a lista de jogadores(players) de acordo com os seus pontos totais
     */
    public void ordenaPlayers(){
        Collections.sort(players);
    }


    public void ensureSaveFolderExists() {
        File pasta = new File("data/save-game");
        if (!pasta.exists()) {
            boolean criado = pasta.mkdirs(); // cria todas as pastas necessárias
            if (criado) {
                System.out.println("Pasta data/save-game criada com sucesso!");
            } else {
                System.out.println("Falha ao criar a pasta data/save-game.");
            }
        }
    }
    /**
     * método que lê o ficheiro de objetos dos jogadores, aramazenando os jogadores na lista de jogadores
     */
    public void readPlayers() {
        ensureSaveFolderExists();
        
        File pasta = new File("data/save-game");

        if (pasta.isDirectory()) {
            File[] arquivos = pasta.listFiles();

            if (arquivos != null) {
                for (File arquivo : arquivos) {
                    try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(arquivo))) {
                        Jogador novoJogador = (Jogador) ois.readObject();
                        addPlayer(novoJogador);

                    } catch (IOException | ClassNotFoundException ex) {
                        System.out.println("Erro ao ler o arquivo: " + arquivo.getName());
                    }
                }
            }
        } else {
            System.out.println("O caminho fornecido não é um diretório.");
        }
    }

    /**
     * método que retorna o jogador atual do jogo
     * @return jogador atual
     */
    public Jogador getPlayer(){
        return jogadorAtivo;
    }

    /**
     * método que coloca nas posições do ranking os três melhores jogadores sendo sempre verificada a existência dos jogadores na lista
     * @param player1 JLabel primeiro lugar
     * @param player2 JLabel segundo lugar
     * @param player3 JLabel terceiro lugar
     */
    public void getWinner(JLabel player1, JLabel player2, JLabel player3){
        ordenaPlayers();
        if(!players.isEmpty())player1.setText(players.get(0).toString());
        if(players.size() > 1) player2.setText(players.get(1).toString());
        if(players.size() > 2) player3.setText(players.get(2).toString());
    }

    /**
     * método que reseta o jogo, quando o jogador decide jogar novamente gerando um novo jogador, definindo a rodada a 0
     * e embaralhando novamente a lista de perguntas para que no próximo jogo sejam geradas novas perguntas ao jogador
     */
    public void reset(){
        if(rodada != 0){
            Collections.shuffle(gameQuestions);
            jogadorAtivo = new Jogador();
            rodada = 0;
        }
    }
}