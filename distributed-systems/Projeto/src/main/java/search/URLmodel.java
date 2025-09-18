package search;

import java.io.Serializable;

public class URLmodel implements Serializable{

    private String url;
    private String title;
    private String paragraph;

    public URLmodel(String url, String title, String paragraph){
        this.url = url;
        this.title = title;
        this.paragraph = paragraph;
    }

    public String getUrl(){
        return url;
    }
    public String getTitle(){
        return title;
    }
    public String getParagraph(){
        return paragraph;
    }

}