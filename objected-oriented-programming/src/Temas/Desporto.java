package Temas;
import POOTrivia.Pergunta;

/**
 * a classe Desporto subdivide-se em três categorias (natação, futebol e ski) e armazena as informações que são comuns às suas
 * subclasses.
 */
public abstract class Desporto extends Pergunta{
    public Desporto(String question){
        super(question);
    }

    /**
     * método que retorna a majoração da pergunta da categoria desporto
     * @return majoração
     */
    public int getMajoracao(){
        return 3;
    }
}