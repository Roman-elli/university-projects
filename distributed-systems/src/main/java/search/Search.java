package search;

import java.io.Serializable;

public class Search implements Serializable{
    private String title;
    private String paragraph;
    private String url;
    private int count;

    public Search(String title, String paragraph, String url, int count) {
        this.title = title;
        this.paragraph = paragraph;
        this.url = url;
        this.count = count;
    }

    public String getTitle() {
        return title;
    }

    public String getParagraph() {
        return paragraph;
    }

    public String getUrl() {
        return url;
    }

    public int getCount() {
        return count;
    }
}

