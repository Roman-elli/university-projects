package web;

public class HackerNewsResult {
    private String title;
    private String url;
    private String gatewayResponse;

    public HackerNewsResult(String title, String url) {
        this.title = title;
        this.url = url;
        this.gatewayResponse = "";
    }

    public String getTitle() {
        return title;
    }

    public String getUrl() {
        return url;
    }

    public String getGatewayResponse() {
        return gatewayResponse;
    }

    public void setGatewayResponse(String gatewayResponse) {
        this.gatewayResponse = gatewayResponse;
    }
}
