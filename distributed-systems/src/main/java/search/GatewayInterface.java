package search;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface GatewayInterface extends Remote {
    void logMessage(String message) throws RemoteException;
    void closeLog() throws RemoteException;
    String proccessUrl(String message) throws RemoteException;
    public List<Search> makeSearch(String message, int page) throws RemoteException;
    public List<String> getUrlList(String message) throws RemoteException;
    public String takeNext() throws RemoteException;
    public boolean getEmpty() throws java.rmi.RemoteException;
    public void putIn(String linker, String url) throws java.rmi.RemoteException;
    public List<String> getStatistics() throws RemoteException;
    public List<String> getFormattedStatistics() throws RemoteException;
}
