package search;

import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;
import java.util.concurrent.*;
import java.io.*;
import java.util.*;

public class IndexServer_2 extends UnicastRemoteObject implements Index {
    private static BufferedWriter indexLog;  // Log para registrar atividades do servidor
    private ConcurrentHashMap<String, ArrayList<URLmodel>> indexedItems; // Índice de palavras
    private ConcurrentHashMap<String, Set<String>> processedUrls;  // URLs processadas
    private ConcurrentHashMap<String, Integer> searchList; // Contador de buscas por palavra-chave
    //private final String extern_index = "192.168.46.2"; // Endereço IP do servidor externo

 
    public IndexServer_2() throws RemoteException {
        super();
        indexedItems = new ConcurrentHashMap<>();
        processedUrls = new ConcurrentHashMap<>();
        searchList = new ConcurrentHashMap<>();

        try {
            File logDir = new File("log");
            if (!logDir.exists()) logDir.mkdirs();

            indexLog = new BufferedWriter(new FileWriter("log/indexLog_2.txt", false));
            logMessage("Starting index...");
            System.out.println("Index_2 Working...");

            Runtime.getRuntime().addShutdownHook(new Thread(this::closeLog)); // Fecha log ao encerrar
        } catch (IOException e) {
            e.printStackTrace(); // Inicia a sincronização periódica com o servidor externo
        }

        connectToExternIndex();
        startSynchronization();
    }

    // Método que realiza a sincronização periódica entre os servidores
    private void startSynchronization() {
        new Thread(() -> {
            while (true) {
                try {
                    Registry registry = LocateRegistry.getRegistry(8181);
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

    //Conecta inicialmente ao index externo e sincroniza os dados
    private void connectToExternIndex() {
        new Thread(() -> {
            while (true) {
                try {
                    Registry registry = LocateRegistry.getRegistry(8181);
                    Index externServer = (Index) registry.lookup("index");
                    indexedItems.putAll(externServer.getIndexedItems());
                    processedUrls.putAll(externServer.getProcessedUrls());
                    searchList.putAll(externServer.getSearchList());
                    logMessage("Connected to extern index and retrieved data.");
                    break; 
                } catch (Exception e) {
                    logMessage("Failed to connect to extern index: " + e.getMessage() + ", retrying in 5 seconds...");
                    try {
                        Thread.sleep(5000); // Aguarda 5 segundos antes da próxima sincronização
                    } catch (InterruptedException ignored) {}
                }
            }
        }).start();
    }

    public static void main(String[] args) {
        try {
            IndexServer_2 server = new IndexServer_2();
            Registry registry = LocateRegistry.createRegistry(8180);
            registry.rebind("index", server);

            logMessage("Index server is ready...");
            System.out.println("IndexServer_2 is running on port 8180...");
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }

    // Método para adicionar palavras ao índice
    public void addToIndex(String word, URLmodel url) throws RemoteException {
        indexedItems.compute(word, (k, list) -> {
            if (list == null) { 
                list = new ArrayList<>();
            }
            list.add(url);
            return list;
        });
    }
 
    // Métodos para obter os índices e listas armazenadas
    public ConcurrentHashMap<String, ArrayList<URLmodel>> getIndexedItems() throws RemoteException {
        return indexedItems;
    }

    // Métodos para obter os URLS processados
    public ConcurrentHashMap<String, Set<String>> getProcessedUrls() throws RemoteException {
        return processedUrls;
    }

    // Métodos para obter a lista de pesquisa
    public ConcurrentHashMap<String, Integer> getSearchList() throws RemoteException {
        return searchList;
    }

    // Método para armazenar novas URLs processadas
    public void putNew(String linker, String url) throws RemoteException {
        processedUrls.compute(url, (k, links) -> {
            if (links == null) links = ConcurrentHashMap.newKeySet();
            if (!linker.equals("main") && !linker.equals(url)) {
                links.add(linker);
            }
            return links;
        });
    }

    // Método para registrar mensagens no log
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

    // Fecha o arquivo de log corretamente
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

     // Método para obter as estatísticas das palavras mais pesquisadas
    public List<String> statistics() throws RemoteException {
        List<String> tenBest = new ArrayList<>();

        List<Map.Entry<String, Integer>> entryList = new ArrayList<>(searchList.entrySet());
        entryList.sort((entry1, entry2) -> entry2.getValue() - entry1.getValue());

        for (int i = 0; i < Math.min(10, entryList.size()); i++) {
            tenBest.add(entryList.get(i).getKey());
        }
        return tenBest;
    }

    // Método para encontrar um modelo de URL específico
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

    // Método para listar todas as URLs relacionadas a um determinado site
    public List<String> listUrls(String url) throws RemoteException {
        return new ArrayList<>(processedUrls.getOrDefault(url, new HashSet<>()));
    }

    //Obtêm o tamanho dos indices
    public int getSize() throws RemoteException{
        return indexedItems.size();
    }
}