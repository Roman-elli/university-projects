package themes;
import javax.swing.*;

/**
 * The Skiing class stores the specific data of questions and answers related to this category.
 */
public class Skiing extends Sports{
    public Skiing(String question){
        super(question);
    }

    /**
     * Method that returns the points of the question if it is answered correctly
     * @return points of the question
     */
    public int calculatePoints(){
        return (super.getQuestionPoints() + super.getScoreWeight()) * ThemeConfig.SKIING_POINT_WEIGHT;
    }

    /**
     * Method that sets the Skiing image on the label
     * @param labelImage label where the image will be displayed
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon(ThemeConfig.SKIING_ICON);
        labelImage.setIcon(image);
    }
}
