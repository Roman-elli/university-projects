# 🌐 Googol Search Engine – Distributed Web Crawler & Search Platform

This project implements a **distributed search engine** built with **Java RMI** for backend indexing and **Spring Boot** for a modern web interface.  
It features multiple processes working in tandem: URL downloading, indexing, queue management, and live statistics, along with AI-enhanced content summaries.

---

## 🚀 Features

🔹 **Distributed Indexing with Java RMI**  
  - Two `IndexServer`s maintain separate indices with periodic synchronization.  
  - Stores **inverted indices**, **processed URLs**, and **search statistics**.

🔹 **Downloader (Web Crawler)**  
  - Fetches HTML content from URLs using `Jsoup`.  
  - Cleans and tokenizes text, updates indices, and extracts links for further crawling.  
  - Automatically reconnects to index servers and the gateway if any node goes offline.

🔹 **Gateway Interface**  
  - Manages the **queue of URLs** to be processed.  
  - Acts as the central point for all download and search requests.

🔹 **Client & Web Interface**  
  - Originally had a console-based RMI client.  
  - Now replaced with a **Spring Boot web frontend**.  
  - Provides pages for:
    - Querying the search engine
    - Indexing new URLs
    - Viewing search statistics (live via WebSocket)
    - Inspecting URLs related to a specific site
    - Fetching HackerNews-related content for a given query

🔹 **AI Integration**  
  - `GeminiService` uses **Generative AI** to produce short, informative text summaries for user queries.  
  - Enhances the search experience with **contextual explanations**.

🔹 **HackerNews Content Fetching**  
  - `HackerNewsService` fetches top stories, jobs, and polls containing the user’s query.  
  - Uses `Jsoup` to extract page text and filter relevant results.

🔹 **WebSockets for Live Statistics**  
  - Updates search statistics in real time for all connected clients.  
  - Handles multiple concurrent WebSocket sessions.  

---

## 📂 Project Structure

- **`search/`** 💻  
  Java RMI backend components:
  - `Downloader.java` → Handles URL crawling and indexing.
  - `IndexServer_1.java` & `IndexServer_2.java` → Maintain distributed indices.
  - `Client.java` → Original RMI console client (superseded by web frontend).
  - `Gateway.java` → Manage URL queue and search requests.
  - `URLmodel.java` & `Search.java` → Data structures for indexing and results.

- **`web/`** 🌐  
  Spring Boot frontend:
  - `ServingWebContentApplication.java` → Main Spring Boot application.
  - `WebController.java` → Routes, query handling, indexing, and integration with RMI Gateway.
  - `GeminiService.java` → Generates AI summaries for queries.
  - `HackerNewsService.java` → Fetches and filters HackerNews content.
  - `WebSocketConfig.java` → WebSocket setup for live statistics.
  - `templates/` → Thymeleaf HTML templates for web pages.
  - `static/` → CSS and image assets.

- **`log/`** 📝  
  Stores logs for downloader and index servers:
  - `downloaderLog_*.txt`  
  - `indexLog_*.txt`

---

## 🕹️ How to Run

1. Build & compile the project
    ```bash
    ./build/mvnw package
    ./build/build.cmd
    ```

2. Insert your gemini api key in the file `src\main\resources\application.properties`
    ```bash
    gemini.api.key=YOUR_API_KEY_HERE
    ```

3. Start Index Servers
   ```bash
   ./build/run-server-1.cmd
   ./build/run-server-2.cmd
   ```

4. Start Gateway
    ```bash
    ./build/run-gateway.cmd
    ```

5. Start Downloader
     ```bash
   ./build/run-downloader.cmd
   ```

6. Start Client or Web application
    ```bash
    ./build/mvnw spring-boot:run
    ```
7. Open in browser
    ```bash
    localhost:8080/
    ```