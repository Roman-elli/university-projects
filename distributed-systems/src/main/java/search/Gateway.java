package search;

import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.UnicastRemoteObject;
import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.Random;
import java.util.Set;

// Classe Gateway que implementa a interface GatewayInterface
public class Gateway extends UnicastRemoteObject implements GatewayInterface {
    private ConcurrentLinkedQueue<String> urlsToIndex; //Fila de URLs a serem indexadas
    private BufferedWriter gateLog; // Arquivo de log
    private Set<String> urlsVisitadas; // Set utilizado para garantir que o mesmo site nao sera indexado mais de uma vez
    private Index  index_1; // Referência para o primeiro servidor de indexação
    private Index index_2; // Referência para o segundo servidor de indexação
    //private final String ip_address_2;
    private static final DateTimeFormatter TIMESTAMP_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private double response_time_index_1, response_time_index_2; // Tempo médio de resposta dos servidores
    private int request_count_index_1, request_count_index_2;// Contagem de requisições para cada servidor

    
    public Gateway() throws RemoteException {
        super();
        response_time_index_1 = 0;
        response_time_index_2 = 0;
        request_count_index_1 = 0;
        request_count_index_2 = 0;
        urlsToIndex = new ConcurrentLinkedQueue<>();
        urlsVisitadas = new HashSet<>();
        //ip_address_2 = "192.168.46.2"; // Definição do IP do segundo servidor

        try {
            // Cria um diretório se não existir
            File logDir = new File("log");
            if (!logDir.exists()) {
                logDir.mkdirs();
            }

             // Cria um arquivo de log para registrar as atividades do Gateway
            gateLog = new BufferedWriter(new FileWriter("log/gateLog.txt", false));
            logMessage("Starting Gateway...");

            // Hook para fechar o arquivo ao desligar
            Runtime.getRuntime().addShutdownHook(new Thread(this::closeLog));
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Iniciar conexão com os servidores Index
        connectToIndex();
    }

    //Método para conectar-se aos servidores de indexação
    private void connectToIndex() {
        int attempts = 0;
        while ((index_1 == null || index_2 == null) && attempts < 1) {
            try {
                if (index_1 == null) {
                    // Conectando ao primeiro servidor de indexação (local)
                    index_1 = (Index) LocateRegistry.getRegistry(8181).lookup("index");
                    logMessage("Conectado ao Index 1 localmente");
                }
                if (index_2 == null) {
                    // Conectando ao segundo servidor de indexação (remoto)
                    index_2 = (Index) LocateRegistry.getRegistry(8180).lookup("index");
                    logMessage("Conectado ao Index 2");
                }
            } catch (NotBoundException | RemoteException e) {
                logMessage("Erro ao conectar aos IndexServers: " + e.getMessage());
                
            }
            attempts++;
        }
    }

    // Método para enviar URLs para os servidores de indexação
    private void sendToIndex(String key, String url) {
        boolean sent = false;

        while (!sent) {
            try {
                if (index_1 != null) {
                    index_1.putNew(key, url);
                    logMessage("Enviado ao Index 1: " + url);
                    sent = true;
                }
            } catch (RemoteException e) {
                logMessage("Erro ao enviar para Index 1. Tentando reconectar...");
                index_1 = null;
                connectToIndex();
            }

            try {
                if (index_2 != null) {
                    index_2.putNew(key, url);
                    logMessage("Enviado ao Index 2: " + url);
                    sent = true;
                }
            } catch (RemoteException e) {
                logMessage("Erro ao enviar para Index 2. Tentando reconectar...");
                index_2 = null;
                connectToIndex();
            }

            if (!sent) {
                logMessage("Nenhum Index disponível. Aguardando...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException ie) {
                    ie.printStackTrace();
                }
            }
        }
    }
    
    // Método para obter a próxima URL na fila
    public String takeNext() throws RemoteException {
        return urlsToIndex.poll();
    }

     // Verifica se a fila de URLs está vazia
    public boolean getEmpty() throws RemoteException {
        return urlsToIndex.isEmpty();
    }

    // Adiciona uma URL à fila se ainda não estiver nela
    public void putIn(String linker, String url) throws RemoteException {
        if (!urlsToIndex.contains(url)) urlsToIndex.offer(url);
    }

    // Método para registrar mensagens no log
    public synchronized void logMessage(String message) {
        try {
            if (gateLog != null) {
                String timestamp = LocalDateTime.now().format(TIMESTAMP_FORMAT);
                gateLog.write("[" + timestamp + "] " + message);
                gateLog.newLine();
                gateLog.flush();
                System.out.println(message);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Fecha o arquivo de log corretamente
    public void closeLog() {
        try {
            if (gateLog != null) {
                logMessage("Fechando Gateway...");
                gateLog.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Processa uma URL e a adiciona ao índice
    public String proccessUrl(String message) throws RemoteException {
        if (message.startsWith("https://") || message.startsWith("http://") ) {
            if(!urlsVisitadas.contains(message)){
                urlsToIndex.add(message);
                urlsVisitadas.add(message);
                logMessage("URL INDEX: " + message);
                sendToIndex("main", message);
                return "Url indexed";
            }else return "Url already indexed";
        }
        return "Invalid URL";
    }

    // Método para realizar buscas nos servidores de indexação
    public List<Search> makeSearch(String message, int page) throws RemoteException {
        logMessage("SEARCH KEYS: " + message);
        Random random = new Random();
        boolean useFirstIndex = random.nextBoolean(); // Escolhe aleatoriamente entre index_1 e index_2

        long startTime = System.nanoTime();
        try {
            List<Search> results = (useFirstIndex ? index_1 : index_2).searchWord(message, page);
            updateResponseTime(useFirstIndex ? 1 : 2, System.nanoTime() - startTime);
            return results;
        } catch (RemoteException e1) {
            logMessage("Erro ao buscar no " + (useFirstIndex ? "Index 1" : "Index 2"));

            startTime = System.nanoTime();
            try {
                List<Search> results = (useFirstIndex ? index_2 : index_1).searchWord(message, page);
                updateResponseTime(useFirstIndex ? 2 : 1, System.nanoTime() - startTime);
                return results;
            } catch (RemoteException e2) {
                logMessage("Nenhum Index disponível. Tentando reconectar...");
                index_2 = null;
                index_1 = null;
                connectToIndex();

                startTime = System.nanoTime();
                List<Search> results = index_1.searchWord(message, page);
                updateResponseTime(1, System.nanoTime() - startTime);
                return results;
            }
        }
    }

     // Atualiza o tempo médio de resposta dos servidores
    private void updateResponseTime(int index, long durationNano) {
        double durationMs = durationNano / 1_000_000.0;  // Converte para milissegundos

        if (index == 1) {
            response_time_index_1 = ((response_time_index_1 * request_count_index_1) + durationMs) / (request_count_index_1 + 1);
            request_count_index_1++;
        } else {
            response_time_index_2 = ((response_time_index_2 * request_count_index_2) + durationMs) / (request_count_index_2 + 1);
            request_count_index_2++;
        }
    }

    //Função que retorna as estatisticas do sistema
    public List<String> getStatistics() throws RemoteException {
        List<String> statisticsList = new ArrayList<>();
        connectToIndex();
        try {
            statisticsList = index_1.statistics();
            statisticsList.add("Barrel 1 Ativo!!!\nTamanho do index: " + index_1.getSize());
            statisticsList.add("Tempo médio de resposta (Barrel 1): " + String.format("%.1f", response_time_index_1 / 100) + " décimas de segundo");
        } catch (Exception e1) {
            logMessage("Erro ao obter estatísticas no Index 1.");
            index_1 = null;
            connectToIndex();
        }

        try {
            //List<String> stats2 = index_2.statistics();
            //statisticsList.addAll(stats2);
            statisticsList.add("Barrel 2 Ativo!!!\nTamanho do index: " + index_2.getSize());
            statisticsList.add("Tempo médio de resposta (Barrel 2): " + String.format("%.1f", response_time_index_2 / 100) + " décimas de segundo");
        } catch (Exception e2) {
            logMessage("Erro ao obter estatísticas no Index 2.");
            index_2 = null;
            connectToIndex();
        }
    return statisticsList;
    }

    public List<String> getFormattedStatistics() throws RemoteException {
        List<String> statsRaw = getStatistics(); // Método já existente que retorna List<String>
        List<String> topWords = statsRaw.size() > 10 ? statsRaw.subList(0, 10) : statsRaw;

        List<String> formattedList = new ArrayList<>();
        if(topWords.size() > 0){
            formattedList.add("10 palavras mais pesquisadas:");
            formattedList.addAll(topWords);
        }
        else{
            formattedList.add("No searches were made until this moment.");
        }

        return formattedList;
    }

    
    //Lista de URL'S que levam a uma pagina específica
    public List<String> getUrlList(String message) throws RemoteException {
        logMessage("ANALYSE SPECIFIC URL: " + message);
        try {
            return index_1.listUrls(message);
        } catch (RemoteException e1) {
            logMessage("Erro ao consultar URLs no Index 1. Tentando Index 2...");
            try {
                return index_2.listUrls(message);
            } catch (RemoteException e2) {
                logMessage("Nenhum Index disponível. Tentando reconectar...");
                index_1 = null;
                index_2 = null;
                connectToIndex();
                return index_1.listUrls(message);
            }
        }
    }

    public static void main(String[] args) {
        try {
            Gateway gateway = new Gateway();
            Registry registry = LocateRegistry.createRegistry(8183);
            registry.rebind("gateway", gateway); // Registrando corretamente o serviço
            gateway.logMessage("Gateway pronto. Aguardando conexões...");
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }
}
