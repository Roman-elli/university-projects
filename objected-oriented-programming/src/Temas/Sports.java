package Temas;
import POOTrivia.Question;

/**
 * a classe Sports subdivide-se em três categorias (natação, futebol e ski) e armazena as informações que são comuns às suas
 * subclasses.
 */
public abstract class Sports extends Question{
    public Sports(String question){
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