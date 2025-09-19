package web;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import org.json.JSONArray;
import org.json.JSONObject;

@Service
public class GeminiService {

    @Value("${gemini.api.key}")
    private String geminiApiKey;

    private static final String GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=";

    public String generateText(String userQuery) {
        try {
            RestTemplate restTemplate = new RestTemplate();

            // Construir o prompt baseado na consulta do usuário
            String prompt = String.format(
                "Generate a short, informative formal paragraph explaining: \"%s\", remember to dont put anything more, only the answer. " +
                " the researched topic, even if it contains errors or is an acronym. " +
                "Try to guess the context based on the term and explain it clearly to a general reader.. " +
                "In addition, just send the text that the customer should read in a way that makes them feel like you are talking to them, and if the customer does not write anything, just tell them to write something.." +
                "If there is no context, create one automatically. Be creative. NEVER ask them to write something that will help answer the question better, just respond with something about the search, it could be a curiosity.",
                userQuery
            );

            JSONObject payload = new JSONObject()
                .put("contents", new JSONArray()
                    .put(new JSONObject()
                        .put("parts", new JSONArray()
                            .put(new JSONObject().put("text", prompt)))));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<String> request = new HttpEntity<>(payload.toString(), headers);

            ResponseEntity<String> response = restTemplate.exchange(
                GEMINI_URL + geminiApiKey,
                HttpMethod.POST,
                request,
                String.class
            );

            if (response.getStatusCode() == HttpStatus.OK) {
                JSONObject json = new JSONObject(response.getBody());
                return json.getJSONArray("candidates")
                           .getJSONObject(0)
                           .getJSONObject("content")
                           .getJSONArray("parts")
                           .getJSONObject(0)
                           .getString("text");
            } else {
                return "Error generating text with AI.";
            }

        } catch (Exception e) {
            e.printStackTrace();
            return "Error accessing the AI service.";
        }
    }
}
