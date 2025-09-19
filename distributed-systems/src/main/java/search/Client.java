package search;

import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.util.List;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) {
        GatewayInterface gateway = null;
        String ip_address_gateway = "192.168.46.51"; // Gateway IP

        // Keep trying to connect to the Gateway until you succeed.
        gateway = connectToGateway(ip_address_gateway);
        
        // Scanner for user data input
        Scanner scanner = new Scanner(System.in);
        boolean working = true;

        // Welcome messages
        System.out.println("============================================");
        System.out.println("Welcome to Googol service!!!");
        System.out.println("Your best search platform!!!");
        System.out.println("============================================");

        // Client menu
        while (working) {
            System.out.println("\nAvailable services:");
            System.out.println("  (1) Index new URL");
            System.out.println("  (2) Search page by terms");
            System.out.println("  (3) See list of related pages");
            System.out.println("  (4) View statistics");
            System.out.println("  (0) Complete service");
            System.out.print("\nEnter the number of the desired option: ");

            String option = scanner.nextLine();

            // Check that the input contains only numbers before converting
            if (!option.matches("\\d+")) {  
                System.out.println("Invalid option! Please enter a valid number.");
                continue;
            }

            int escolha = Integer.parseInt(option);

            try {
                switch (escolha) {
                    case 1:
                        // Indexing a new URL
                        System.out.print("\nEnter the URL you want to index: ");
                        String message = scanner.nextLine();
                        String result = gateway.proccessUrl(message);
                        System.out.println("Result: " + result);
                        break;

                    case 2:
                        // Search by terms
                        System.out.print("\nEnter the terms you want to search for: ");
                        message = scanner.nextLine();
                        int page = 1;

                        while (true) {
                            List<Search> result_search = gateway.makeSearch(message, page);

                            if (!result_search.isEmpty()) {
                                System.out.println("\n===== Search results =====\n");
                                for (int i = 0; i < result_search.size(); i++) {
                                    System.out.println("Result #" + ((page - 1) * 10 + (i + 1)) + ":");
                                    System.out.println("====================================");
                                    System.out.println(result_search.get(i));
                                    System.out.println("====================================\n");
                                }

                                System.out.println("\nPress ENTER to see more or type ‘0’ to exit.");
                                if (scanner.nextLine().equals("0")) break;
                                page++;
                            } else {
                                System.out.println("\nNo results found.");
                                break;
                            }
                        }
                        break;

                    case 3:
                        // View related pages
                        System.out.print("\nEnter the specific page you wish to view: ");
                        message = scanner.nextLine();
                        List<String> result_search = gateway.getUrlList(message);
                        if (!result_search.isEmpty()) {
                            System.out.println("\n===== Related Pages =====\n");
                            for (String resultItem : result_search) {
                                System.out.println("====================================");
                                System.out.println(resultItem);
                                System.out.println("====================================\n");
                            }
                        } else {
                            System.out.println("\nNo results found.");
                        }
                        break;

                    case 4:
                        // Statistics query
                        System.out.println("\nStatistics request sent...");
                        List<String> resultStatistics = gateway.getStatistics();
                        if(resultStatistics.isEmpty()){
                            System.out.println("Server unavailable...");
                        }
                        else{
                            System.out.println("\n===== Statistics =====\n");
                            for (String stat : resultStatistics) {
                                System.out.println("-> " + stat);
                            }
                            System.out.println("====================================\n");
                        }
                        break;

                    case 0:
                        // Finish the job
                        working = false;
                        System.out.println("\nThank you for using Googol! See you next time..");
                        break;

                    default:
                        System.out.println("Invalid option! Please try again..");
                }
            } catch (RemoteException e) {
                System.out.println("Error communicating with the Gateway. Attempting to reconnect...");
                gateway = connectToGateway(ip_address_gateway);
            }
        }

        scanner.close();
    }

    // Method for attempting to reconnect to the Gateway
    private static GatewayInterface connectToGateway(String ip_address_gateway) {
        GatewayInterface gateway = null;
        while (gateway == null) {
            try {
                gateway = (GatewayInterface) LocateRegistry.getRegistry(8183).lookup("gateway");
                System.out.println("Connected to Gateway!");
            } catch (RemoteException | NotBoundException e) {
                System.out.println("Gateway offline... Trying again in 2 seconds...");
                try {
                    Thread.sleep(1000); // Pause for 1 second before trying again
                } catch (InterruptedException ie) {
                    System.out.println("Error while attempting to reconnect: " + ie.getMessage());
                    ie.printStackTrace();
                }
            }
        }
        return gateway;
    }
}