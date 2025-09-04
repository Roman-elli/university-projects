package themes;
import core.Question;

/**
 * The Sports class is subdivided into three categories (Swimming, Football, and Skiing) 
 * and stores the information that is common to its subclasses.
 */
public abstract class Sports extends Question{
    public Sports(String question){
        super(question);
    }

    /**
     * Method that returns the bonus points for a question in the sports category
     * @return bonus points
     */
    public int getScoreWeight(){
        return ThemeConfig.SPORTS_POINT_WEIGHT;
    }
}
