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
    // URL da API do Hacker News para as principais histórias
    private final String TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json";
    
    // URL base para buscar detalhes de uma história específica
    private final String ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/%d.json";

    // Tipos permitidos de itens (histórias, vagas e enquetes)
    private final List<String> allowedTypes = Arrays.asList("story", "job", "poll");

    // Limite de resultados a serem retornados
    private static final int MAX_RESULTS = 10;
    // Limite de tentativas de busca
    private static final int MAX_ATTEMPTS = 50;

    // Método que busca as principais histórias que contenham a query no conteúdo
    public List<HackerNewsResult> fetchTopStories(String query) {
        RestTemplate restTemplate = new RestTemplate();
        List<HackerNewsResult> results = new ArrayList<>();

        try {
            // Obtém a lista de IDs das histórias
            String json = restTemplate.getForObject(TOP_STORIES_URL, String.class);
            JSONArray ids = new JSONArray(json);

            int found = 0;      // Contador de resultados encontrados
            int attempts = 0;   // Contador de tentativas feitas

            // Percorre os IDs até atingir o limite de resultados ou tentativas
            for (int i = 0; i < ids.length() && found < MAX_RESULTS && attempts < MAX_ATTEMPTS; i++) {
                attempts++;

                int storyId = ids.getInt(i);
                // Busca os detalhes da história
                String storyJson = restTemplate.getForObject(String.format(ITEM_URL, storyId), String.class);
                JSONObject story = new JSONObject(storyJson);

                String type = story.optString("type", "");
                // Ignora tipos não permitidos
                if (!allowedTypes.contains(type)) {
                    continue;
                }

                // Verifica se a história possui título e URL
                if (story.has("url") && story.has("title")) {
                    String url = story.getString("url");
                    String title = story.getString("title");

                    // Busca o texto da página referenciada
                    String textContent = fetchPageText(url);
                    // Se o texto contiver a query, adiciona aos resultados
                    if (textContent != null && textContent.toLowerCase().contains(query.toLowerCase())) {
                        results.add(new HackerNewsResult(title, url));
                        found++;
                    }
                }
            }
        } catch (Exception e) {
            // Em caso de erro, imprime a exceção
            e.printStackTrace();
        }

        return results;
    }

    // Método que busca e extrai o texto de uma página da web
    private String fetchPageText(String urlString) {
        try {
            // Usa Jsoup para carregar o conteúdo da página
            Document doc = Jsoup.connect(urlString)
                                .userAgent("Mozilla/5.0") // Define um user-agent
                                .timeout(5000)            // Tempo limite de 5 segundos
                                .get();
            return doc.text(); // Retorna apenas o texto da página
        } catch (Exception e) {
            // Ignora erros ao carregar a página
        }
        return null;
    }
}
