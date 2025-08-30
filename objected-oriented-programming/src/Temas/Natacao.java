package Temas;
import javax.swing.*;

/**
 * A class Natacao armazena os dados especificos das perguntas e respostas relacionados com esta categoria
 */
public class Natacao extends Desporto{
    public Natacao(String question){
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
     * método que insere à label a imagem de Natacao
     * @param labelImage label onde será apresentada a imagem
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon("../assets/images/Natação.png");
        labelImage.setIcon(image);
    }
}