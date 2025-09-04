package themes;
import javax.swing.*;

/**
 * The Swimming class stores the specific data of questions and answers related to this category.
 */
public class Swimming extends Sports{
    public Swimming(String question){
        super(question);
    }

    /**
     * Method that returns the points of the question if it is answered correctly
     * @return points of the question
     */
    public int calculatePoints(){
        return super.getQuestionPoints() + super.getScoreWeight() + ThemeConfig.SWIM_POINT_WEIGHT;
    }

    /**
     * Method that sets the Swimming image on the label
     * @param labelImage label where the image will be displayed
     */
    public void changeImage(JLabel labelImage){
        ImageIcon image = new ImageIcon(ThemeConfig.SWIM_ICON);
        labelImage.setIcon(image);
    }
}
