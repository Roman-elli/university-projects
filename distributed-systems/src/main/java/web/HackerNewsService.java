package web;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class HackerNewsService {
    // Hacker News API URL for top stories
    private final String TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json";
    
    // Base URL for retrieving details of a specific story
    private final String ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/%d.json";

    // Permitted types of items (stories, job openings, and polls)
    private final List<String> allowedTypes = Arrays.asList("story", "job", "poll");

    // Limit on results to be returned
    private static final int MAX_RESULTS = 10;

    // Search attempt limit
    private static final int MAX_ATTEMPTS = 50;

    // Method that searches for the main stories containing the query in the content
    public List<HackerNewsResult> fetchTopStories(String query) {
        RestTemplate restTemplate = new RestTemplate();
        List<HackerNewsResult> results = new ArrayList<>();

        try {
            String json = restTemplate.getForObject(TOP_STORIES_URL, String.class);
            JSONArray ids = new JSONArray(json);

            int found = 0;
            int attempts = 0;

            for (int i = 0; i < ids.length() && found < MAX_RESULTS && attempts < MAX_ATTEMPTS; i++) {
                attempts++;

                int storyId = ids.getInt(i);
                String storyJson = restTemplate.getForObject(String.format(ITEM_URL, storyId), String.class);
                JSONObject story = new JSONObject(storyJson);

                String type = story.optString("type", "");

                if (!allowedTypes.contains(type)) {
                    continue;
                }

                if (story.has("url") && story.has("title")) {
                    String url = story.getString("url");
                    String title = story.getString("title");

                    String textContent = fetchPageText(url);

                    if (textContent != null && textContent.toLowerCase().contains(query.toLowerCase())) {
                        results.add(new HackerNewsResult(title, url));
                        found++;
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return results;
    }

    // Method that searches for and extracts text from a web page
    private String fetchPageText(String urlString) {
        try {
            Document doc = Jsoup.connect(urlString)
                                .userAgent("Mozilla/5.0")
                                .timeout(5000)
                                .get();
            return doc.text();
        } catch (Exception e) {
            // Ignore errors when loading the page
        }
        return null;
    }
}
