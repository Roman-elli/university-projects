package Temas;
import javax.swing.*;

/**
 * A class Swimming armazena os dados especificos das perguntas e respostas relacionados com esta categoria
 */
public class Swimming extends Sports{
    public Swimming(String question){
        super(question);
    }

    /**
     * método que retorna os pontos da pergunta, caso esta seja respondida corretamente
     * @return pontos da pergunta
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + super.getMajoracao() + 10;
    }

    /**
     * método que insere à label a imagem de Swimming
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("assets/images/Swim.png");
        labelImage.setIcon(image);
    }
}