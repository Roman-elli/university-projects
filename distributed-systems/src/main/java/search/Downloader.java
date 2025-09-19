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
    private static BufferedWriter downloaderLog;
    private static final DateTimeFormatter TIMESTAMP_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");    
    private Index local_index;
    private Index extern_index;
    private GatewayInterface gateway;

    public Downloader() {
        try {
            File logDir = new File("log");
            if (!logDir.exists()) {
                logDir.mkdirs();
            }

            downloaderLog = new BufferedWriter(new FileWriter("log/downloaderLog_1.txt", false));
            logMessage("Starting Downloader...");

            Runtime.getRuntime().addShutdownHook(new Thread(this::closeLog));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws InterruptedException, RemoteException {
        Downloader downloader = new Downloader();
        downloader.connectToServers();
        downloader.processUrls();
    }

    // No index server available. Attempting to reconnect
    private void connectToServers() {
        while ((local_index == null && extern_index == null) || gateway == null) { 
            try {
                if (gateway == null) {
                    gateway = (GatewayInterface) LocateRegistry.getRegistry(8183).lookup("gateway");
                    logMessage("Connected to the Gateway");
                }

                if (local_index == null) {
                    local_index = (Index) LocateRegistry.getRegistry(8181).lookup("index");
                    logMessage("Connected to Index 1 (Local)");
                }

                if (extern_index == null) {
                    extern_index = (Index) LocateRegistry.getRegistry(8180).lookup("index");
                    logMessage("Connected to Index 2 (External)");
                }
            } catch (NotBoundException | RemoteException e) {
                logMessage("Error connecting to servers: " + e.getMessage());
                gateway = null;
                extern_index = null;
                local_index = null;
                System.out.println("Trying again in 1 second...");
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    // Processes URLs
    private void processUrls() throws InterruptedException, RemoteException {
        while (true) {
            while (isGatewayEmpty()) {  
                System.out.println("Waiting...");
                Thread.sleep(1000);
            }

            String url = takeNextUrl();
            if (url == null) continue;

            if (!isValidHtmlUrl(url)) {
                logMessage("Skipping non-HTML URL: " + url);
                continue;
            }

            logMessage("Processing: " + url);
            Document doc;
            try {
                doc = Jsoup.connect(url).get();
            } catch (IOException e) {
                logMessage("Failed to download: " + url);
                continue;
            }

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

            for (String word : words) {
                if (word.length() > 1 && word.length() < 50) {
                    URLmodel insert = new URLmodel(url, title, paragraph);
                    if(success1) success1 = tryAddToIndex(local_index, word, insert, "IndexServer_1");
                    if(success2) success2 = tryAddToIndex(extern_index, word, insert, "IndexServer_2");

                    while (!success1 && !success2) {
                        logMessage("No Index servers available. Attempting to reconnect...");
                        local_index = null;
                        extern_index = null;
                        connectToServers();
                        success1 = tryAddToIndex(local_index, word, insert, "IndexServer_1");
                        success2 = tryAddToIndex(extern_index, word, insert, "IndexServer_2");
                        Thread.sleep(1000);
                    }
                }
            }

            Elements links = doc.select("a[href]");
            success1 = true;
            success2 = true;
            for (Element link : links) {
                String rawUrl = link.attr("abs:href");
                String normalizedUrl = normalizeUrl(rawUrl);

                if (normalizedUrl != null) {
                    boolean inserted = false;

                    while (!inserted) { 
                        try {
                            if (gateway != null) {
                                gateway.putIn(normalizeUrl(url), normalizedUrl);
                            } else {
                                logMessage("Gateway offline. Attempting to reconnect...");
                                gateway = null;
                                connectToServers();
                                continue;
                            }

                            if(success1) success1 = tryPutNew(local_index, normalizeUrl(url), normalizedUrl, "IndexServer_1");
                            if(success2) success2 = tryPutNew(extern_index, normalizeUrl(url), normalizedUrl, "IndexServer_2");

                            if (success1 || success2) {
                                inserted = true;
                            } else {
                                logMessage("Both IndexServers offline. Attempting to reconnect....");
                                extern_index = null;
                                local_index = null;
                                connectToServers();
                            }
                        } catch (RemoteException ex) {
                            logMessage("Connection failure. Attempting to reconnect...");
                            gateway = null;
                            Thread.sleep(1000);
                        }
                    }
                }
            }
        }
    }

    // Auxiliary method for connecting and verifying the Gateway
    private boolean isGatewayEmpty() {
        while (true) {
            try {
                return gateway.getEmpty();
            } catch (RemoteException e) {
                logMessage("Failed to connect to the gateway. Attempting to reconnect...");
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

    // Get the next URL from the Gateway indexing queue
    private String takeNextUrl() {
        while (true) {
            try {
                return gateway.takeNext();
            } catch (RemoteException e) {
                logMessage("Failed to obtain Gateway URL. Attempting to reconnect...");
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

    // Add terms to the inverted index
    private boolean tryAddToIndex(Index index, String word, URLmodel insert, String serverName) {
        if (index == null) return false;
        try {
            index.addToIndex(word, insert);
            return true;
        } catch (RemoteException e) {
            return false;
        }
    }

    // Adds a URL to the processedURL structure in barrels
    private boolean tryPutNew(Index index, String linker, String url, String serverName) {
        if (index == null) return false;
        try {
            index.putNew(linker, url);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    // Method for logging messages
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

    // Close the log file correctly
    public void closeLog() {
        if (downloaderLog == null) return;
        try {
            logMessage("Closing Downloader...");
            downloaderLog.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Normalize URL
    private static String normalizeUrl(String url) {
        try {
            @SuppressWarnings("deprecation")
            URL u = new URL(url);
            return u.toString();
        } catch (MalformedURLException e) {
            return null;
        }
    }

    // Check if the URL is valid
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