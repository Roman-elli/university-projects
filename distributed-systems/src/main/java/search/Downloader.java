package search;

import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import org.jsoup.*;
import org.jsoup.nodes.*;
import org.jsoup.select.*;

public class Downloader {
    private static BufferedWriter downloaderLog; // Log para registrar atividades
    private static final DateTimeFormatter TIMESTAMP_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");    
    private Index local_index; // Referência ao servidor Index local
    private Index extern_index; // Referência ao servidor Index externo
    private GatewayInterface gateway; // Referência ao Gateway

    public Downloader() {
        try {
             // Cria o diretório de logs se não existir
            File logDir = new File("log");
            if (!logDir.exists()) {
                logDir.mkdirs();
            }

            // Cria o arquivo de log para o Downloader
            downloaderLog = new BufferedWriter(new FileWriter("log/downloaderLog_1.txt", false));
            logMessage("Iniciando Downloader...");

            // Adicionando um hook para fechar o log ao desligar
            Runtime.getRuntime().addShutdownHook(new Thread(this::closeLog));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws InterruptedException, RemoteException {
        Downloader downloader = new Downloader();
        downloader.connectToServers(); // Conecta-se aos servidores
        downloader.processUrls(); // Inicia o processamento das URLs
    }

    // Tenta conectar-se ao Gateway e aos servidores Index
    private void connectToServers() {
        while ((local_index == null && extern_index == null) || gateway == null) { 
            try {
                if (gateway == null) {
                    gateway = (GatewayInterface) LocateRegistry.getRegistry(8183).lookup("gateway");
                    logMessage("Conectado ao Gateway");
                }

                if (local_index == null) {
                    local_index = (Index) LocateRegistry.getRegistry(8181).lookup("index");
                    logMessage("Conectado ao Index 1 (Local)");
                }

                if (extern_index == null) {
                    extern_index = (Index) LocateRegistry.getRegistry(8180).lookup("index");
                    logMessage("Conectado ao Index 2 (Externo)");
                }
            } catch (NotBoundException | RemoteException e) {
                logMessage("Erro ao conectar aos servidores: " + e.getMessage());
                gateway = null;
                extern_index = null;
                local_index = null;
                System.out.println("Tentando novamente em 1 segundo...");
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    //Processa os URLS
    private void processUrls() throws InterruptedException, RemoteException {
        while (true) {
             // Aguarda até que haja URLs disponíveis no Gateway
            while (isGatewayEmpty()) {  
                System.out.println("Waiting...");
                Thread.sleep(1000);
            }

            String url = takeNextUrl(); // Obtém a próxima URL do Gateway
            if (url == null) continue;

            // Verifica se a URL é válida para indexação
            if (!isValidHtmlUrl(url)) {
                logMessage("Skipping non-HTML URL: " + url);
                continue;
            }

            logMessage("Processing: " + url);
            Document doc;
            try {
                doc = Jsoup.connect(url).get(); // Faz o download do conteúdo HTML
            } catch (IOException e) {
                logMessage("Failed to download: " + url);
                continue;
            }

            // Processa o conteúdo extraído da página
            String output = doc.text();
            String[] words = output.replaceAll("[\\(\\),.:;!?\"'´^$%&*<>#]", "")
                    .replaceAll("\\d+", "")
                    .replaceAll("\\/", "")
                    .toLowerCase()
                    .split("\\b");

            String title = doc.title().isEmpty() ? "No_title" : doc.title();
            Element firstParagraph = doc.select("p").first();
            String paragraph = (firstParagraph != null && !firstParagraph.text().isEmpty()) ? firstParagraph.text() : "No_paragraph";
            boolean success1 = true;
            boolean success2 = true;
            // Adiciona palavras ao índice
            for (String word : words) {
                if (word.length() > 1 && word.length() < 50) {
                    URLmodel insert = new URLmodel(url, title, paragraph);
                    if(success1) success1 = tryAddToIndex(local_index, word, insert, "IndexServer_1");
                    if(success2) success2 = tryAddToIndex(extern_index, word, insert, "IndexServer_2");



                     // Caso ambos os servidores falhem, tenta reconectar
                    while (!success1 && !success2) {
                        logMessage("Nenhum servidor Index disponível. Tentando reconectar...");
                        local_index = null;
                        extern_index = null;
                        connectToServers();
                        success1 = tryAddToIndex(local_index, word, insert, "IndexServer_1");
                        success2 = tryAddToIndex(extern_index, word, insert, "IndexServer_2");
                        Thread.sleep(1000);
                    }
                }
            }

            // Processa os links internos da página
            Elements links = doc.select("a[href]");
            success1 = true;
            success2 = true;
            for (Element link : links) {
                String rawUrl = link.attr("abs:href");
                String normalizedUrl = normalizeUrl(rawUrl);

                if (normalizedUrl != null) {
                    boolean inserted = false;

                    // Tenta inserir até obter sucesso
                    while (!inserted) { 
                        try {
                            if (gateway != null) {
                                gateway.putIn(normalizeUrl(url), normalizedUrl);
                            } else {
                                logMessage("Gateway offline. Tentando reconectar...");
                                gateway = null;
                                connectToServers();
                                continue;
                            }

                            if(success1) success1 = tryPutNew(local_index, normalizeUrl(url), normalizedUrl, "IndexServer_1");
                            if(success2) success2 = tryPutNew(extern_index, normalizeUrl(url), normalizedUrl, "IndexServer_2");

                            if (success1 || success2) {
                                inserted = true;
                            } else {
                                logMessage("Ambos os IndexServers offline. Tentando reconectar...");
                                extern_index = null;
                                local_index = null;
                                connectToServers();
                            }
                        } catch (RemoteException ex) {
                            logMessage("Falha de conexão. Tentando reconectar...");
                            gateway = null;
                            Thread.sleep(1000);
                        }
                    }
                }
            }
        }
    }

    // Método auxiliar para conectar e verificar o Gateway
    private boolean isGatewayEmpty() {
        while (true) {
            try {
                return gateway.getEmpty();
            } catch (RemoteException e) {
                logMessage("Falha ao conectar ao Gateway. Tentando reconectar...");
                gateway = null;
                connectToServers();
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                }
            }
        }
    }

    //Obtêm o próximo URL da fila de indexação do Gateaway
    private String takeNextUrl() {
        while (true) {
            try {
                return gateway.takeNext();
            } catch (RemoteException e) {
                logMessage("Falha ao obter URL do Gateway. Tentando reconectar...");
                gateway = null;
                connectToServers();
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                }
            }
        }
    }

    //Adiciona os termos no indice invertido
    private boolean tryAddToIndex(Index index, String word, URLmodel insert, String serverName) {
        if (index == null) return false;
        try {
            index.addToIndex(word, insert);
            return true;
        } catch (RemoteException e) {
            return false;
        }
    }

    //Adiciona um URL a estrurura processedUrl nos barrels
    private boolean tryPutNew(Index index, String linker, String url, String serverName) {
        if (index == null) return false;
        try {
            index.putNew(linker, url);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    // Método para registrar mensagens no log
    public static void logMessage(String message) {
        if (downloaderLog == null) return;

        synchronized (downloaderLog) {
            try {
                String timestamp = LocalDateTime.now().format(TIMESTAMP_FORMAT);
                downloaderLog.write("[" + timestamp + "] " + message);
                downloaderLog.newLine();
                downloaderLog.flush();
                System.out.println(message);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // Fecha o arquivo de log corretamente
    public void closeLog() {
        if (downloaderLog == null) return;
        try {
            logMessage("Fechando Downloader...");
            downloaderLog.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //Normaliza o URL
    private static String normalizeUrl(String url) {
        try {
            @SuppressWarnings("deprecation")
            URL u = new URL(url);
            return u.toString();
        } catch (MalformedURLException e) {
            return null;
        }
    }

    //Verifica se o URL é válido
    private static boolean isValidHtmlUrl(String url) {
        String[] invalidExtensions = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3", ".zip", ".rar"};
        for (String ext : invalidExtensions) {
            if (url.toLowerCase().endsWith(ext)) {
                return false;
            }
        }
        return true;
    }
}