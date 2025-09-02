package POOTrivia;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * The FrameClass contains the necessary methods to create the program's graphical interface.
 * This class includes several variables such as labels, buttons, and panels.
 * A JPanel was used for the menu, one for the questions, and another for the results, with the transition between them
 * handled through setVisible. Furthermore, it is worth noting that the game instance is only created
 * at the initial moment of the program.
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
        int frame_width = 1200;
        int frame_height = 800;
        window_setup(frame_width,frame_height);

        // Game Menu
        panelMenu = new JPanel(new BorderLayout());
        panelMenu.setBorder(new EmptyBorder(0, frame_width/3, frame_height/5, frame_width/3));

        JPanel panelMenuGrid = new JPanel(new GridLayout(3, 1, 0, frame_height / 12));

        ImageIcon logo = new ImageIcon("assets/images/Logo.png");
        JLabel labelLogo = new JLabel(logo);

        JButton buttonPlay = new JButton("Start Game");
        buttonPlay.setFont(new Font("Century Gothic", Font.BOLD, 20));
        buttonPlay.addActionListener(new ButtonInitiateListener());

        JButton buttonPlayers = new JButton("Best Players");
        buttonPlayers.setFont(new Font("Century Gothic", Font.BOLD, 20));
        buttonPlayers.addActionListener(new ButtonRankListener());

        JButton buttonEnd = new JButton("Exit Game");
        buttonEnd.setFont(new Font("Century Gothic", Font.BOLD, 20));
        buttonEnd.addActionListener(new ButtonEndListener());

        panelMenuGrid.add(buttonPlay);
        panelMenuGrid.add(buttonPlayers);
        panelMenuGrid.add(buttonEnd);

        panelMenu.add(labelLogo, BorderLayout.NORTH);
        panelMenu.add(panelMenuGrid, BorderLayout.CENTER);

        // Questions panel
        panelQuestions = new JPanel(new BorderLayout());

        JPanel panelQuestionsGrid = new JPanel(new GridLayout(3, 3, 50, 50));
        panelQuestionsGrid.setBorder(new EmptyBorder(frame_height/6, frame_width/6, frame_height/6, frame_width/6));

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

        // Players Panel
        panelResult = new JPanel(new BorderLayout());

        JPanel panelResultGrid = new JPanel(new GridLayout(4, 1));
        panelResultGrid.setBorder(new EmptyBorder(frame_height/10, frame_width/10, 0, 0));

        JPanel panelFlow1 = new JPanel(new FlowLayout());
        JPanel panelFlow2 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel panelFlow3 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel panelFlow4 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JPanel panelFlow5 = new JPanel(new FlowLayout());

        ImageIcon goldImage = new ImageIcon("assets/images/Gold.png");
        JLabel labelImage1 = new JLabel(goldImage);

        labelPlayer1 = new JLabel("1st place");
        labelPlayer1.setFont(new Font("Century Gothic", Font.BOLD, 18));

        ImageIcon silverImage = new ImageIcon("assets/images/Silver.png");
        JLabel labelImage2 = new JLabel(silverImage);

        labelPlayer2 = new JLabel("2nd place");
        labelPlayer2.setFont(new Font("Century Gothic", Font.BOLD, 18));

        ImageIcon bronzeImage = new ImageIcon("assets/images/Bronze.png");
        JLabel labelImage3 = new JLabel(bronzeImage);

        labelPlayer3 = new JLabel("3rd place");
        labelPlayer3.setFont(new Font("Century Gothic", Font.BOLD, 18));

        ImageIcon penguimIcon = new ImageIcon("assets/images/Penguin.png");
        JLabel labelPinguim = new JLabel(penguimIcon);

        labelPlayerName = new JLabel();
        labelPlayerName.setFont(new Font("Century Gothic", Font.BOLD, 20));

        JButton buttonReturn = new JButton("Return to menu");
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
     * Draw game window
     * @param frame_width
     * @param frame_height
     */
    private void window_setup(int frame_width, int frame_height) {
        setTitle("POOTrivia");
        setSize(frame_width, frame_height);
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {

            @Override
            public void windowClosing(java.awt.event.WindowEvent e) {
                exitGame();
            }
        });
    }

    /**
    * Method that adjusts the questions panel for a new question and updates it according to the information
    * of the question passed as a parameter.
    * @param playQuestion the question
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
        playQuestion.defineTheme(buttons, gameTrivia.getRound());
    }

    /**
     * The ButtonInitiateListener class handles the actions that occur after the user presses the start game button.
     */
    private class ButtonInitiateListener implements ActionListener {
        /**
         * Method that, upon detecting a player interaction with the start game button, executes the reset method,
         * switches the panels, and sets up the questions panel for the first question of the game.
         * @param e the event to be processed
         */
        @Override
        public void actionPerformed(ActionEvent e) {
            gameTrivia.reset();
            panelMenu.setVisible(false);
            panelQuestions.setVisible(true);
            FrameClass.this.add(panelQuestions);
            buttonNext.setText("Next Question");
            nextQuestion(gameTrivia.newQuestion());
        }
    }

    /**
     * The ButtonNext class handles the actions that occur after the next question button is pressed.
     */
    private class ButtonNext implements ActionListener {

        /**
         * Method that, upon detecting the user's interaction with the ButtonNext, updates the questions panel in each round
         * and stores the player's information when the last round of the game is reached. Then, the method that creates
         * the player's file is executed, and finally, it switches to the results panel.
         * @param e the event to be processed
         */
        @Override
        public void actionPerformed(ActionEvent e){
            if(gameTrivia.getRound() < 5) nextQuestion(gameTrivia.newQuestion());
            else {
                String nome = JOptionPane.showInputDialog(null, "Write your name:", "Player Name", JOptionPane.PLAIN_MESSAGE);
                if (nome != null && !nome.isEmpty()) {
                    if(nome.length() < 40) {
                        gameTrivia.getPlayer().setPlayerName(nome);
                        gameTrivia.addPlayer(gameTrivia.getPlayer());
                        gameTrivia.writePlayer(nome);
                        panelQuestions.setVisible(false);
                        panelResult.setVisible(true);
                        labelPlayerName.setText("Your score was " + gameTrivia.getPlayer().getPoints() + "!!! Thank you for playing POOTrivia " + nome + "!!!");
                        gameTrivia.getWinner(labelPlayer1, labelPlayer2, labelPlayer3);
                        FrameClass.this.add(panelResult);
                    }
                    else{
                        JOptionPane.showMessageDialog(null, "Please enter a name with fewer characters (maximum 50).", "Error", JOptionPane.ERROR_MESSAGE);
                    }
                }
                if(nome != null && nome.isEmpty()){
                    JOptionPane.showMessageDialog(null, "Please, enter a valid name.", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        }
    }

    /**
     * The ButtonListen class handles the interactions of the answer buttons.
     */
    private class ButtonListen implements ActionListener {
        /**
         * Method that, after an answer button has been clicked, prevents clicking any other button except the
         * next question button, compares the user's answer with the correct one, and finally adds the correct
         * and incorrect answers to the player's arrays of right and wrong answers.
         * @param e the event to be processed
         */
        @Override
        public void actionPerformed(ActionEvent e){
            JButton button = (JButton) e.getSource();
            for(JButton i: buttons) i.setEnabled(false);
            String answer = button.getText();
            String right_answer = gameTrivia.newQuestion().returnCorrect();
            Jogador player = gameTrivia.getPlayer();
            labelCorrect.setVisible(true);
            buttonNext.setVisible(true);
            ImageIcon image;
            if (answer.equals(right_answer)) {
                image = new ImageIcon("assets/images/Correct.png");
                labelResult.setText("Won " + gameTrivia.newQuestion().calculatePoints() + " points");
                player.addRight(gameTrivia.newQuestion());
            } else {
                image = new ImageIcon("assets/images/Wrong.png");
                player.addWrong(gameTrivia.newQuestion());
            }

            labelCorrect.setIcon(image);
            gameTrivia.nextRound();
            if(gameTrivia.getRound() == 5) buttonNext.setText("End Game");
        }
    }

    /**
     * The ButtonReturnListener class handles the player's interaction with the return-to-menu button.
     */
    private class ButtonReturnListener implements ActionListener {
        /**
         * return to menu
         * @param e event to be processed
         */
        @Override
        public void actionPerformed(ActionEvent e){
            panelResult.setVisible(false);
            panelMenu.setVisible(true);
            FrameClass.this.add(panelMenu);
        }
    }

    /**
     * The ButtonRankListener class handles the player's interaction with the Best Players button.
     */
    private class ButtonRankListener implements ActionListener {

        /**
         * Method that makes the Results panel visible, requesting the best players from the main game class
         * through the getWinner method.
         * @param e the event to be processed
         */
        @Override
        public void actionPerformed(ActionEvent e){
            panelMenu.setVisible(false);
            panelResult.setVisible(true);
            labelPlayerName.setText("Best Players Ranking!!!");
            gameTrivia.getWinner(labelPlayer1, labelPlayer2, labelPlayer3);
            FrameClass.this.add(panelResult);
        }
    }

    /**
     * The ButtonEndListener class handles exiting the game through the End Game button.
     */
    private class ButtonEndListener implements ActionListener {
        /**
         * Method that handles exiting the game.
         * @param e the event to be processed
         */
        @Override
        public void actionPerformed(ActionEvent e){
            exitGame();
        }
    }

    /**
     * Method used to exit the game, either through the End Game button or by clicking the X on the window.
     */
    private void exitGame(){
        if(JOptionPane.showConfirmDialog(null, "Are you sure you want to exit?", "Exit Game", JOptionPane.YES_NO_OPTION) == 0) {
            System.exit(0);
        }
    }
}