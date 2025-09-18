package search;

import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.util.List;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) {
        GatewayInterface gateway = null;
        String ip_address_gateway = "192.168.46.51"; // IP fixo do Gateway

        // Tenta conectar ao Gateway repetidamente até conseguir
        gateway = connectToGateway(ip_address_gateway);
        
        // Scanner para entrada de dados do usuário
        Scanner scanner = new Scanner(System.in);
        boolean working = true;

        // Exibe mensagem de boas-vindas
        System.out.println("============================================");
        System.out.println("Welcome to Googol service!!!");
        System.out.println("Your best search platform!!!");
        System.out.println("============================================");

        // Loop principal do cliente
        while (working) {
            System.out.println("\nServiços disponíveis:");
            System.out.println("  (1) Indexar novo URL");
            System.out.println("  (2) Pesquisar página por termos");
            System.out.println("  (3) Consultar lista de páginas relacionadas");
            System.out.println("  (4) Consultar estatísticas");
            System.out.println("  (0) Finalizar serviço.");
            System.out.print("\nDigite o número da opção desejada: ");

            String option = scanner.nextLine();

            // Verifica se a entrada contém apenas números antes de converter
            if (!option.matches("\\d+")) {  
                System.out.println("Opção inválida! Por favor, digite um número válido.");
                continue;
            }

            int escolha = Integer.parseInt(option);

            try {
                switch (escolha) {
                    case 1:
                        // Indexação de um novo URL
                        System.out.print("\nDigite o URL que deseja indexar: ");
                        String message = scanner.nextLine();
                        String result = gateway.proccessUrl(message);
                        System.out.println("Resultado: " + result);
                        break;

                    case 2:
                        // Pesquisa por termos
                        System.out.print("\nDigite os termos que deseja pesquisar: ");
                        message = scanner.nextLine();
                        int page = 1;

                        while (true) {
                            List<Search> result_search = gateway.makeSearch(message, page);

                            if (!result_search.isEmpty()) {
                                System.out.println("\n===== Resultados da Pesquisa =====\n");
                                for (int i = 0; i < result_search.size(); i++) {
                                    System.out.println("Resultado #" + ((page - 1) * 10 + (i + 1)) + ":");
                                    System.out.println("====================================");
                                    System.out.println(result_search.get(i));
                                    System.out.println("====================================\n");
                                }

                                System.out.println("\nPressione ENTER para ver mais ou digite '0' para sair.");
                                if (scanner.nextLine().equals("0")) break;
                                page++;
                            } else {
                                System.out.println("\nNenhum resultado encontrado.");
                                break;
                            }
                        }
                        break;

                    case 3:
                        // Consulta de páginas relacionadas
                        System.out.print("\nDigite a página específica que deseja consultar: ");
                        message = scanner.nextLine();
                        List<String> result_search = gateway.getUrlList(message);
                        if (!result_search.isEmpty()) {
                            System.out.println("\n===== Páginas Relacionadas =====\n");
                            for (String resultItem : result_search) {
                                System.out.println("====================================");
                                System.out.println(resultItem);
                                System.out.println("====================================\n");
                            }
                        } else {
                            System.out.println("\nNenhum resultado encontrado.");
                        }
                        break;

                    case 4:
                        // Consulta de estatísticas
                        System.out.println("\nRequisição de estatísticas enviada...");
                        List<String> resultStatistics = gateway.getStatistics();
                        if(resultStatistics.isEmpty()){
                            System.out.println("Servidor indisponível...");
                        }
                        else{
                            System.out.println("\n===== Estatísticas =====\n");
                            for (String stat : resultStatistics) {
                                System.out.println("-> " + stat);
                            }
                            System.out.println("====================================\n");
                        }
                        break;

                    case 0:
                        // Finaliza o serviço
                        working = false;
                        System.out.println("\nObrigado por usar o Googol! Até a próxima.");
                        break;

                    default:
                        System.out.println("Opção inválida! Tente novamente.");
                }
            } catch (RemoteException e) {
                System.out.println("Erro ao comunicar com o Gateway. Tentando reconectar...");
                gateway = connectToGateway(ip_address_gateway);
            }
        }

        scanner.close();
    }

    // Método para tentar reconectar ao Gateway
    private static GatewayInterface connectToGateway(String ip_address_gateway) {
        GatewayInterface gateway = null;
        while (gateway == null) {
            try {
                // Conectando ao Gateway via RMI
                gateway = (GatewayInterface) LocateRegistry.getRegistry(8183).lookup("gateway");
                System.out.println("Conectado ao Gateway!");
            } catch (RemoteException | NotBoundException e) {
                // Se o gateway estiver offline, aguarda e tenta novamente
                System.out.println("Gateway offline... Tentando novamente em 2 segundos...");
                try {
                    Thread.sleep(1000); // Pausa de 1 segundo antes de tentar novamente
                } catch (InterruptedException ie) {
                    System.out.println("Erro ao tentar reconectar: " + ie.getMessage());
                    ie.printStackTrace();
                }
            }
        }
        return gateway;
    }
}