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
                "Gere um parágrafo formal curto e informativo explicando: \"%s\". " +
                " o tema pesquisado, mesmo que contenha erros ou seja uma sigla. " +
                "Tente adivinhar o contexto com base no termo e explique de forma clara para um leitor comum. " +
                "Além disso, apenas envie o texto que o cliente deve ler de forma que ache que esteja falando com ele, e se o cliente nao escrever nada, apenas diga para que escreva algo." +
                "caso não tenha contexto, crie um automaticamente. Seja criativo. NUNCA peça para que escreva algo que ajude a responder melhor, apenas responda algo sobre a pesquisa, pode ser uma curiosidade",
                userQuery
            );

            JSONObject payload = new JSONObject()
                .put("contents", new JSONArray()
                    .put(new JSONObject()
                        .put("parts", new JSONArray()
                            .put(new JSONObject().put("text", prompt)))));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // Construção do corpo da requisição
            HttpEntity<String> request = new HttpEntity<>(payload.toString(), headers);

            // Chamada para a API do Gemini
            ResponseEntity<String> response = restTemplate.exchange(
                GEMINI_URL + geminiApiKey,
                HttpMethod.POST,
                request,
                String.class
            );

            // Verificar a resposta
            if (response.getStatusCode() == HttpStatus.OK) {
                JSONObject json = new JSONObject(response.getBody());
                return json.getJSONArray("candidates")
                           .getJSONObject(0)
                           .getJSONObject("content")
                           .getJSONArray("parts")
                           .getJSONObject(0)
                           .getString("text");
            } else {
                return "Erro ao gerar texto com IA.";
            }

        } catch (Exception e) {
            e.printStackTrace();
            return "Erro ao acessar o serviço da IA.";
        }
    }
}
