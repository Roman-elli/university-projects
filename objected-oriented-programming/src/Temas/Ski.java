package Temas;
import javax.swing.*;

/**
 * A class Ski armazena os dados especificos das perguntas e respostas relacionados com esta categoria
 */
public class Ski extends Desporto{
    public Ski(String question){
        super(question);
    }

    /**
     * método que retorna os pontos da pergunta, caso esta seja respondida corretamente
     * @return pontos da pergunta
     */
    public int calculatePoints(){
        return (super.getQuestionPoints() + super.getMajoracao()) * 2;
    }

    /**
     * método que insere à label a imagem de Ski
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("../assets/images/Ski.png");
        labelImage.setIcon(image);
    }
}