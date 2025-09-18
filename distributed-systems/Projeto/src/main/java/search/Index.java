package search;

import java.rmi.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public interface Index extends Remote {
    public void putNew(String linker, String url) throws java.rmi.RemoteException;
    public void addToIndex(String word, URLmodel url) throws java.rmi.RemoteException;
    public List<Search> searchWord(String word, int page) throws java.rmi.RemoteException;
    public URLmodel findURLModelForTerm(String url, List<String> terms) throws java.rmi.RemoteException;
    public List<String> listUrls(String url) throws RemoteException;
    public List<String> statistics() throws RemoteException;
    public int getSize() throws RemoteException;
    public ConcurrentHashMap<String, ArrayList<URLmodel>> getIndexedItems() throws RemoteException;
    public ConcurrentHashMap<String, Set<String>> getProcessedUrls() throws RemoteException;
    public ConcurrentHashMap<String, Integer> getSearchList() throws RemoteException;
}