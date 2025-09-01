package POOTrivia;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * A class FrameClass contém os métodos necessários para criar a interface gráfica do programa
 * Esta classe contêm variás variáveis, como labels, botões e painéis
 * Foi utilizado um Jpanel para o menu, um para as perguntas e outro para os resultados, sendo a mudança entre eles
 * feita por meio do setVisible. Além disso, acrescenta-se que a instancia referente ao jogo apenas é criada
 * no momento inicial do programa
 */

public class FrameClass extends JFrame{
    private final POOTrivia gameTrivia;
    private final JButton[] buttons;
    private final JLabel labelQuestion, labelResult, labelImage, labelCorrect, labelPlayer1, labelPlayer2, labelPlayer3, labelPlayerName;
    private final JButton buttonNext;
    private final JPanel panelMenu, panelQuestions, panelResult;

    public FrameClass(){
        super();
        gameTrivia = new POOTrivia();
        int largura = 1200;
        int altura = 800;
        configurarJanela(largura,altura);

        // Menu do jogo
        panelMenu = new JPanel(new BorderLayout());
        panelMenu.setBorder(new EmptyBorder(0, largura/3, altura/5, largura/3));

        JPanel panelMenuGrid = new JPanel(new GridLayout(3, 1, 0, altura / 12));

        ImageIcon logo = new ImageIcon("assets/images/Logo.png");
        JLabel labelLogo = new JLabel(logo);

        JButton buttonPlay = new JButton("Iniciar Jogo");
        buttonPlay.setFont(new Font("Century Gothic", Font.BOLD, 20));
        buttonPlay.addActionListener(new ButtonInitiateListener());

        JButton buttonPlayers = new JButton("Melhores Jogadores");
        buttonPlayers.setFont(new Font("Century Gothic", Font.BOLD, 20));
        buttonPlayers.addActionListener(new ButtonRankListener());

        JButton buttonEnd = new JButton("Sair do jogo");
        buttonEnd.setFont(new Font("Century Gothic", Font.BOLD, 20));
        buttonEnd.addActionListener(new ButtonEndListener());

        panelMenuGrid.add(buttonPlay);
        panelMenuGrid.add(buttonPlayers);
        panelMenuGrid.add(buttonEnd);

        panelMenu.add(labelLogo, BorderLayout.NORTH);
        panelMenu.add(panelMenuGrid, BorderLayout.CENTER);

        // Painel de questões
        panelQuestions = new JPanel(new BorderLayout());

        JPanel panelQuestionsGrid = new JPanel(new GridLayout(3, 3, 50, 50));
        panelQuestionsGrid.setBorder(new EmptyBorder(altura/6, largura/6, altura/6, largura/6));

        JPanel panelQuestionsFlow = new JPanel(new FlowLayout());

        labelResult = new JLabel();
        labelResult.setFont(new Font("Century Gothic", Font.BOLD, 20));

        labelQuestion = new JLabel();
        labelQuestion.setFont(new Font("Century Gothic", Font.BOLD, 17));

        labelImage = new JLabel();
        labelCorrect = new JLabel();

        JButton button1 = new JButton();
        button1.setFont(new Font("Century Gothic", Font.BOLD, 15));
        button1.addActionListener(new ButtonListen());

        JButton button2 = new JButton();
        button2.setFont(new Font("Century Gothic", Font.BOLD, 15));
        button2.addActionListener(new ButtonListen());

        JButton button3 = new JButton();
        button3.setFont(new Font("Century Gothic", Font.BOLD, 15));
        button3.addActionListener(new ButtonListen());

        JButton button4 = new JButton();
        button4.setFont(new Font("Century Gothic", Font.BOLD, 15));
        button4.addActionListener(new ButtonListen());

        JButton button5 = new JButton();
        button5.setFont(new Font("Century Gothic", Font.BOLD, 15));
        button5.addActionListener(new ButtonListen());

        JButton button6 = new JButton();
        button6.setFont(new Font("Century Gothic", Font.BOLD, 15));
        button6.addActionListener(new ButtonListen());

        buttons = new JButton[]{button1, button2, button3, button4, button5, button6};

        buttonNext = new JButton();
        buttonNext.setFont(new Font("Century Gothic", Font.BOLD, 17));
        buttonNext.addActionListener(new ButtonNext());

        panelQuestionsFlow.add(labelQuestion);
        panelQuestionsFlow.add(labelImage);
        panelQuestions.add(panelQuestionsFlow, BorderLayout.NORTH);

        panelQuestionsGrid.add(button1);
        panelQuestionsGrid.add(button2);
        panelQuestionsGrid.add(button3);
        panelQuestionsGrid.add(button4);
        panelQuestionsGrid.add(button5);
        panelQuestionsGrid.add(button6);
        panelQuestionsGrid.add(labelCorrect);
        panelQuestionsGrid.add(labelResult);
        panelQuestionsGrid.add(buttonNext);
        panelQuestions.add(panelQuestionsGrid, BorderLayout.CENTER);

        // Panel jogadores
        panelResult = new JPanel(new BorderLayout());

        JPanel panelResultGrid = new JPanel(new GridLayout(4, 1));
        panelResultGrid.setBorder(new EmptyBorder(altura/10, largura/10, 0, 0));

        JPanel panelFlow1 = new JPanel(new FlowLayout());
        JPanel panelFlow2 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel panelFlow3 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel panelFlow4 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel panelFlow5 = new JPanel(new FlowLayout());

        ImageIcon goldImage = new ImageIcon("assets/images/Ouro.png");
        JLabel labelImage1 = new JLabel(goldImage);

        labelPlayer1 = new JLabel("1º lugar");
        labelPlayer1.setFont(new Font("Century Gothic", Font.BOLD, 18));

        ImageIcon silverImage = new ImageIcon("assets/images/Prata.png");
        JLabel labelImage2 = new JLabel(silverImage);

        labelPlayer2 = new JLabel("2º lugar");
        labelPlayer2.setFont(new Font("Century Gothic", Font.BOLD, 18));

        ImageIcon bronzeImage = new ImageIcon("assets/images/Bronze.png");
        JLabel labelImage3 = new JLabel(bronzeImage);

        labelPlayer3 = new JLabel("3º lugar");
        labelPlayer3.setFont(new Font("Century Gothic", Font.BOLD, 18));

        ImageIcon penguimIcon = new ImageIcon("assets/images/Pinguim.png");
        JLabel labelPinguim = new JLabel(penguimIcon);

        labelPlayerName = new JLabel();
        labelPlayerName.setFont(new Font("Century Gothic", Font.BOLD, 20));

        JButton buttonReturn = new JButton("Voltar ao menu");
        buttonReturn.setFont(new Font("Century Gothic", Font.BOLD, 20));
        Dimension dimension = new Dimension(200,80);
        buttonReturn.setPreferredSize(dimension);
        buttonReturn.addActionListener(new ButtonReturnListener());

        panelResultGrid.add(panelFlow2);
        panelResultGrid.add(panelFlow3);
        panelResultGrid.add(panelFlow4);
        panelResultGrid.add(panelFlow5);
        panelResult.add(panelResultGrid, BorderLayout.CENTER);

        panelFlow2.add(labelImage1);
        panelFlow2.add(labelPlayer1);
        panelFlow3.add(labelImage2);
        panelFlow3.add(labelPlayer2);
        panelFlow4.add(labelImage3);
        panelFlow4.add(labelPlayer3);
        panelFlow5.add(buttonReturn);

        panelFlow1.add(labelPlayerName);
        panelResult.add(panelFlow1, BorderLayout.NORTH);
        panelResult.add(labelPinguim, BorderLayout.EAST);

        FrameClass.this.add(panelMenu);
        setVisible(true);
    }

    /**
     * método que cofigura o tamanho da janela do jogo
     * @param largura largura do frame
     * @param altura altura do frame
     */
    private void configurarJanela(int largura, int altura) {
        setTitle("POOTrivia");
        setSize(largura, altura);
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {
            /**
             * método que cria uma caixa de pergunta, para saber se o utilizador deseja realmente fechar o programa
             * @param e evento a ser processado
             */
            @Override
            public void windowClosing(java.awt.event.WindowEvent e) {
                realizarSaida();
            }
        });
    }

    /**
     * método que ajusta o panel das perguntas para uma nova pergunta e o atualiza de acordo com as informações pertencentes a pergunta
     * que foi enviada por parametro
     * @param playQuestion pergunta
     */
    private void nextQuestion(Pergunta playQuestion) {
        for(JButton i: buttons) {
            i.setEnabled(true);
            i.setVisible(true);
        }
        buttonNext.setVisible(false);
        labelCorrect.setVisible(false);
        labelResult.setText("");
        labelQuestion.setText(playQuestion.getQuestion());

        playQuestion.changeImage(labelImage);
        playQuestion.defineTema(buttons, gameTrivia.getRound());
    }

    /**
     * a classe ButtonInitiateListener lida com as situações após o utilizador apertar o botão de iniciar jogo
     */
    private class ButtonInitiateListener implements ActionListener {
        /**
         * método que ao detetar uma interação do jogador com o botão de iniciar o jogo, executa o método reset, faz a
         * troca dos panel e ajusta o panel de perguntas para a primeira pergunta do jogo
         * @param e evento a ser processado
         */
        @Override
        public void actionPerformed(ActionEvent e) {
            gameTrivia.reset();
            panelMenu.setVisible(false);
            panelQuestions.setVisible(true);
            FrameClass.this.add(panelQuestions);
            buttonNext.setText("Próxima pergunta");
            nextQuestion(gameTrivia.newQuestion());
        }
    }

    /**
     * a classe ButtonNext lida com as situações após ser apertado o botão de próxima pergunta
     */
    private class ButtonNext implements ActionListener {

        /**
         * método que, assim que é detetado a interação do usuário com o buttonNext, atualiza o painel de perguntas em cada rodada
         * e armazena as informações referentes ao jogador quando chega a última rodada do jogo, em seguida, o metodo que cria o
         * ficheiro do jogador é executado e, por fim, é feita a passagem para o painel de resultados
         * @param e evento a ser processado
         */
        @Override
        public void actionPerformed(ActionEvent e){
            if(gameTrivia.getRound() < 5) nextQuestion(gameTrivia.newQuestion());
            else {
                String nome = JOptionPane.showInputDialog(null, "Digite seu nome:", "Nome do jogador", JOptionPane.PLAIN_MESSAGE);
                if (nome != null && !nome.isEmpty()) {
                    if(nome.length() < 40) {
                        gameTrivia.getPlayer().setPlayerName(nome);
                        gameTrivia.addPlayer(gameTrivia.getPlayer());
                        gameTrivia.writePlayer(nome);
                        panelQuestions.setVisible(false);
                        panelResult.setVisible(true);
                        labelPlayerName.setText("Sua pontuação foi " + gameTrivia.getPlayer().getPoints() + "!!! Obrigado por jogar POOTrivia " + nome + "!!!");
                        gameTrivia.getWinner(labelPlayer1, labelPlayer2, labelPlayer3);
                        FrameClass.this.add(panelResult);
                    }
                    else{
                        JOptionPane.showMessageDialog(null, "Por favor, digite um nome com menor dimensão(máximo 50 caracteres).", "Erro", JOptionPane.ERROR_MESSAGE);
                    }
                }
                if(nome != null && nome.isEmpty()){
                    JOptionPane.showMessageDialog(null, "Por favor, digite um nome válido.", "Erro", JOptionPane.ERROR_MESSAGE);
                }
            }
        }
    }

    /**
     * a classe ButtonListen executa as interações dos botões de resposta
     */
    private class ButtonListen implements ActionListener {
        /**
         * método que após um botão de resposta ter sido carregado, torna impossivel carregar em outro botão que não seja
         * o da próxima pergunta, compara a resposta que o utilizador respondeu com a correta e, por fim, adiciona as respostas corretas e as erradas ao
         * array de perguntas certas e erradas do jogador
         * @param e evento a ser processado
         */
        @Override
        public void actionPerformed(ActionEvent e){
            JButton button = (JButton) e.getSource();
            for(JButton i: buttons) i.setEnabled(false);
            String resposta = button.getText();
            String correta = gameTrivia.newQuestion().returnCorrect();
            Jogador player = gameTrivia.getPlayer();
            labelCorrect.setVisible(true);
            buttonNext.setVisible(true);
            ImageIcon image;
            if (resposta.equals(correta)) {
                image = new ImageIcon("assets/images/Correto.png");
                labelResult.setText("Ganhou " + gameTrivia.newQuestion().calculatePoints() + " pontos");
                player.addRight(gameTrivia.newQuestion());
            } else {
                image = new ImageIcon("assets/images/Errado.png");
                player.addWrong(gameTrivia.newQuestion());
            }

            labelCorrect.setIcon(image);
            gameTrivia.nextRound();
            if(gameTrivia.getRound() == 5) buttonNext.setText("Terminar jogo");
        }
    }

    /**
     * a classe ButtonReturnListener lida com a interação do jogador com o botão de retornar ao menu
     */
    private class ButtonReturnListener implements ActionListener {
        /**
         * método que retorna ao menu
         * @param e evento a ser processado
         */
        @Override
        public void actionPerformed(ActionEvent e){
            panelResult.setVisible(false);
            panelMenu.setVisible(true);
            FrameClass.this.add(panelMenu);
        }
    }

    /**
     * a classe ButtonRankListener lida com a interação do jogador com o botão de Melhores jogadores
     */
    private class ButtonRankListener implements ActionListener {
        /**
         * método que torna visivel o painel de Resultados, requisitando da classe principal do jogo os melhores
         * jogadores por meio do método getWinner
         * @param e evento a ser processado
         */
        @Override
        public void actionPerformed(ActionEvent e){
            panelMenu.setVisible(false);
            panelResult.setVisible(true);
            labelPlayerName.setText("Rank dos melhores jogadores!!!");
            gameTrivia.getWinner(labelPlayer1, labelPlayer2, labelPlayer3);
            FrameClass.this.add(panelResult);
        }
    }

    /**
     * a classe ButtonEndListener lida com a saída do jogo através do botão de Terminar jogo
     */
    private class ButtonEndListener implements ActionListener {
        /**
         * método que realiza a saída do jogo
         * @param e evento a ser processado
         */
        @Override
        public void actionPerformed(ActionEvent e){
            realizarSaida();
        }
    }

    /**
     * método utilizada para realizar a saída do jogo, tanto por meio do botão terminar jogo, como por meio do x no ecrâ
     */
    private void realizarSaida(){
        if(JOptionPane.showConfirmDialog(null, "Tem a certeza que pretende sair?", "Sair", JOptionPane.YES_NO_OPTION) == 0) {
            System.exit(0);
        }
    }
}