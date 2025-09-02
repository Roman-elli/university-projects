package Temas;
import javax.swing.*;

/**
 * A class Skiing armazena os dados especificos das perguntas e respostas relacionados com esta categoria
 */
public class Skiing extends Sports{
    public Skiing(String question){
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
     * método que insere à label a imagem de Skiing
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Skiing.png");
        labelImage.setIcon(image);
    }
}