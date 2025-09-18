package web;

import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.socket.messaging.SessionConnectedEvent;
import org.springframework.web.socket.messaging.SessionDisconnectEvent;

import search.GatewayInterface;
import search.Search;

@Controller
public class WebController {

    private GatewayInterface gateway = null;
    private Thread statisticsThread;
    private volatile boolean running = false;

    @Autowired
    private GeminiService geminiService;

    @Autowired
    private HackerNewsService hackerNewsService;

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    private int activeWebSocketSessions = 0;

    public WebController() {
        gateway = connectToGateway();
    }

    @EventListener
    public synchronized void handleWebSocketConnectListener(SessionConnectedEvent event) {
        System.out.println("Cliente conectou via WebSocket.");
        activeWebSocketSessions++;
        System.out.println("Web Sockets ativos: " + activeWebSocketSessions);

        if (!running) {
            running = true;
            statisticsThread = new Thread(() -> {
                List<String> previousStats = null;
                while (running) {
                    try {
                        List<String> currentStats = gateway.getFormattedStatistics();

                        if (previousStats == null || !previousStats.equals(currentStats)) {
                            messagingTemplate.convertAndSend("/topic/statistics", currentStats);
                            previousStats = currentStats;
                        }

                        Thread.sleep(1000);
                    } catch (RemoteException e) {
                        System.out.println("Erro ao comunicar com o Gateway. Tentando reconectar...");
                        gateway = connectToGateway();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        System.out.println("Thread de estatísticas interrompida.");
                    }
                }
            });
            statisticsThread.start();
        }
    }

    @EventListener
    public synchronized void handleWebSocketDisconnectListener(SessionDisconnectEvent event) {
        System.out.println("Cliente desconectou do WebSocket.");
        activeWebSocketSessions--;

        if (activeWebSocketSessions <= 0) {
            running = false;
            if (statisticsThread != null && statisticsThread.isAlive()) {
                statisticsThread.interrupt();
            }
        }
    }

    // Redireciona para a pagina principal
    @GetMapping("/")
    public String redirect() {
        return "redirect:/greetings";
    }

    // Pagina principal
    @GetMapping("/greetings")
    public String principal() {
        return "greetings";
    }

    // Pagina que apresenta o resultado da pesquisa e o texto gerado pela Gemini
    @GetMapping("/search")
    public String buscar(@RequestParam(name = "query", required = false, defaultValue = "") String query,
                         @RequestParam(name = "page", defaultValue = "1") int page, Model model) {
        String AItext = geminiService.generateText(query);
        try {
            List<Search> result_search = gateway.makeSearch(query, page);
            boolean hasNextPage = result_search.size() > 0;

            model.addAttribute("textoIA", AItext);
            model.addAttribute("result", result_search);
            model.addAttribute("hasNextPage", hasNextPage);
            model.addAttribute("query", query);
            model.addAttribute("page", page);

            if (!hasNextPage) {
                model.addAttribute("noMoreResults", "Não existem mais resultados");
            }

            return "search";
        } catch (RemoteException e) {
            System.out.println("Erro ao comunicar com o Gateway. Tentando reconectar...");
            gateway = connectToGateway();
        }
        return "search";
    }

    // Pagina que executa a funçao de indexação de um site colocado no input
    @GetMapping("/indexing")
    public String inserir(@RequestParam(name = "query", required = false, defaultValue = "Empty") String query, Model model) throws RemoteException {
        try {
            String result = gateway.proccessUrl(query);
            model.addAttribute("result", result);
            return "indexing";
        } catch (RemoteException e) {
            System.out.println("Erro ao comunicar com o Gateway. Tentando reconectar...");
            gateway = connectToGateway();
        }
        return "indexing";
    }

    // Pagina dedicada a apresentação das estatisticas via web socket
    @GetMapping("/statistics")
    public String estatisticas() {
        return "statistics";
    }

    // Pagina dedicada na apresentação dos sites que ligação a um site especificado no input
    @GetMapping("/specificurl")
    public String buscarUrl(@RequestParam(name = "query", required = false, defaultValue = "") String query, Model model) {
        try {
            List<String> result_busca = gateway.getUrlList(query);
            model.addAttribute("result", result_busca);
            return "specificurl";
        } catch (RemoteException e) {
            System.out.println("Erro ao comunicar com o Gateway. Tentando reconectar...");
            gateway = connectToGateway();
        }
        return "specificurl";
    }

    // Pagina dedicada aos resultados dos dados obtidos pela API do HackerNews
    @GetMapping("/hacker")
    public String hacker(@RequestParam(name = "query", required = false, defaultValue = "") String query, Model model) {
        try {
            List<HackerNewsResult> items = hackerNewsService.fetchTopStories(query);
            for (HackerNewsResult item : items) {
                String response = gateway.proccessUrl(item.getUrl());
                item.setGatewayResponse(response);
            }
            model.addAttribute("resultados", items);
        } catch (RemoteException e) {
            System.out.println("Erro ao comunicar com o Gateway. Tentando reconectar...");
            gateway = connectToGateway();
        }
        return "hacker";
    }

    // Função dedicada a manter a conexão com o Gateway caso haja um problema de conexão
    private static GatewayInterface connectToGateway() {
        GatewayInterface gateway = null;
        while (gateway == null) {
            try {
                gateway = (GatewayInterface) LocateRegistry.getRegistry(8183).lookup("gateway");
                System.out.println("Conectado ao Gateway!");
            } catch (RemoteException | NotBoundException e) {
                System.out.println("Gateway offline... Tentando novamente em 2 segundos...");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException ie) {
                    System.out.println("Erro ao tentar reconectar: " + ie.getMessage());
                    ie.printStackTrace();
                }
            }
        }
        return gateway;
    }
}
