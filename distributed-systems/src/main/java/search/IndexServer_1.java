package search;

import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;
import java.util.concurrent.*;
import java.io.*;
import java.util.*;

public class IndexServer_1 extends UnicastRemoteObject implements Index {
    private static BufferedWriter indexLog;
    private ConcurrentHashMap<String, ArrayList<URLmodel>> indexedItems;
    private ConcurrentHashMap<String, Set<String>> processedUrls;
    private ConcurrentHashMap<String, Integer> searchList;
    // private final String extern_index = "192.168.46.2";

    public IndexServer_1() throws RemoteException {
        super();
        indexedItems = new ConcurrentHashMap<>();
        processedUrls = new ConcurrentHashMap<>();
        searchList = new ConcurrentHashMap<>();

        try {
            File logDir = new File("log");
            if (!logDir.exists()) logDir.mkdirs();

            indexLog = new BufferedWriter(new FileWriter("log/indexLog_1.txt", false));
            logMessage("Starting index...");
            System.out.println("Index_1 Working...");

            Runtime.getRuntime().addShutdownHook(new Thread(this::closeLog));
        } catch (IOException e) {
            e.printStackTrace();
        }

        connectToExternIndex();
        startSynchronization();
    }

    // Method that performs periodic synchronization between servers
    private void startSynchronization() {
        new Thread(() -> {
            while (true) {
                try {
                    Registry registry = LocateRegistry.getRegistry(8180);
                    Index externServer = (Index) registry.lookup("index");
                    
                    externServer.getIndexedItems().forEach(indexedItems::putIfAbsent);
                    externServer.getProcessedUrls().forEach(processedUrls::putIfAbsent);
                    externServer.getSearchList().forEach(searchList::putIfAbsent);
                    
                    logMessage("Synchronized missing data with extern index.");
                    
                } catch (Exception e) {
                    logMessage("Failed to sync with extern index: " + e.getMessage());
                }
                try {
                    Thread.sleep(10000);
                } catch (InterruptedException ignored) {}
            }
        }).start();
    }

    // Initially connects to the external index and synchronizes the data
    private void connectToExternIndex() {
        new Thread(() -> {
            while (true) {
                try {
                    Registry registry = LocateRegistry.getRegistry(8180);
                    Index externServer = (Index) registry.lookup("index");
                    indexedItems.putAll(externServer.getIndexedItems());
                    processedUrls.putAll(externServer.getProcessedUrls());
                    searchList.putAll(externServer.getSearchList());
                    logMessage("Connected to extern index and retrieved data.");
                    break; 
                } catch (Exception e) {
                    logMessage("Failed to connect to extern index: " + e.getMessage() + ", retrying in 5 seconds...");
                    try {
                        Thread.sleep(5000);
                    } catch (InterruptedException ignored) {}
                }
            }
        }).start();
    }

    public static void main(String[] args) {
        try {
            IndexServer_1 server = new IndexServer_1();
            Registry registry = LocateRegistry.createRegistry(8181);
            registry.rebind("index", server);

            logMessage("Index server is ready...");
            System.out.println("IndexServer_1 is running on port 8181...");
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }

    // Method for adding words to the index
    public void addToIndex(String word, URLmodel url) throws RemoteException {
        indexedItems.compute(word, (k, list) -> {
            if (list == null) { 
                list = new ArrayList<>();
            }
            list.add(url);
            return list;
        });
    }
 
    // Method for obtaining stored indexes and lists
    public ConcurrentHashMap<String, ArrayList<URLmodel>> getIndexedItems() throws RemoteException {
        return indexedItems;
    }

    // Method for obtaining processed URLs
    public ConcurrentHashMap<String, Set<String>> getProcessedUrls() throws RemoteException {
        return processedUrls;
    }

    // Method for obtaining the search list
    public ConcurrentHashMap<String, Integer> getSearchList() throws RemoteException {
        return searchList;
    }

    // Method for storing newly processed URLs
    public void putNew(String linker, String url) throws RemoteException {
        processedUrls.compute(url, (k, links) -> {
            if (links == null) links = ConcurrentHashMap.newKeySet();
            if (!linker.equals("main") && !linker.equals(url)) {
                links.add(linker);
            }
            return links;
        });
    }

    // Method for logging messages
    public static void logMessage(String message) {
        if (indexLog == null) return;

        try {
            synchronized (indexLog) {
                indexLog.write(message);
                indexLog.newLine();
                indexLog.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Close the log file correctly
    public void closeLog() {
        if (indexLog == null) return;
        try {
            synchronized (indexLog) {
                indexLog.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Method for searching words in the index
    public List<Search> searchWord(String word, int page) throws RemoteException {
        searchList.merge(word, 1, Integer::sum);

        List<String> terms = new ArrayList<>();
        for (String term : word.toLowerCase().split(" ")) {
            if (term.length() > 1 && term.length() < 50) {
                terms.add(term);
            }
        }
        
        Map<String, Integer> urlCountMap = new HashMap<>();
        boolean firstTerm = true; 
    
        for (String term : terms) {
            List<URLmodel> urlModels = indexedItems.get(term);
            if (urlModels == null) {
                return new ArrayList<>();
            }
    
            Map<String, Integer> termUrlCount = new HashMap<>();
            for (URLmodel model : urlModels) {
                int linkCount = processedUrls.getOrDefault(model.getUrl(), new HashSet<>()).size();
                termUrlCount.put(model.getUrl(), linkCount);
            }
    
            if (firstTerm) {
                urlCountMap.putAll(termUrlCount);
                firstTerm = false;
            } else {
                urlCountMap.keySet().retainAll(termUrlCount.keySet());
            }
    
            if (urlCountMap.isEmpty()) {
                return new ArrayList<>();
            }
        }
    
        List<Map.Entry<String, Integer>> sortedUrls = new ArrayList<>(urlCountMap.entrySet());
        sortedUrls.sort((entry1, entry2) -> Integer.compare(entry2.getValue(), entry1.getValue()));
    
        List<Search> resultList = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : sortedUrls) {
            String url = entry.getKey();
            int count = entry.getValue();
    
            URLmodel model = findURLModelForTerm(url, terms);
            if (model != null) {
                Search result = new Search(
                    model.getTitle(),
                    model.getParagraph(),
                    url,
                    count
                );
                resultList.add(result);
            }
        }
    
        int startIndex = (page - 1) * 10;
        int endIndex = Math.min(startIndex + 10, resultList.size());
        return (startIndex >= resultList.size()) ? new ArrayList<>() : new ArrayList<>(resultList.subList(startIndex, endIndex));
    }

     // Method for obtaining statistics on the most searched words
    public List<String> statistics() throws RemoteException {
        List<String> tenBest = new ArrayList<>();

        List<Map.Entry<String, Integer>> entryList = new ArrayList<>(searchList.entrySet());
        entryList.sort((entry1, entry2) -> entry2.getValue() - entry1.getValue());

        for (int i = 0; i < Math.min(10, entryList.size()); i++) {
            tenBest.add(entryList.get(i).getKey());
        }
        return tenBest;
    }

    // Method for finding a specific URL pattern
    public URLmodel findURLModelForTerm(String url, List<String> terms) throws RemoteException {
        for (String term : terms) {
            List<URLmodel> urlModels = indexedItems.get(term);
            if (urlModels != null) {
                for (URLmodel model : urlModels) {
                    if (model.getUrl().equals(url)) {
                        return model;
                    }
                }
            }
        }
        return null;
    }

    // Method for listing all URLs related to a given website
    public List<String> listUrls(String url) throws RemoteException {
        return new ArrayList<>(processedUrls.getOrDefault(url, new HashSet<>()));
    }

    // Obtain the size of the indexes
    public int getSize() throws RemoteException{
        return indexedItems.size();
    }
}