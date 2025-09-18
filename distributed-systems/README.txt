Para garantir a funcionalidade do Googol tem de seguir os seguintes passos:
1º Instale o código no seu computador e meta-o no visual studio
2º Abra 5 powershell 
3º Corra os seguintes comandos em cada uma das powershell:
- java -cp "./lib/jsoup-1.18.3.jar;." search.IndexServer_1
- java -cp "./lib/jsoup-1.18.3.jar;." search.IndexServer_2
- java -cp "./lib/jsoup-1.18.3.jar;." search.Gateway
- java -cp "./lib/jsoup-1.18.3.jar;." search.Downloader
- ./mvnw spring-boot:run
4º Abra no seu navegador neste link: localhost:8080/

5º Caso tenha o interesse em utilizar HTTPS siga os seguintes passos:
- Verifique na linha de comandos se o NGINX é reconhecido ("nginx -version")
- Caso não seja reconhecido, verifique o processo de instalação presente no link: https://nginx.org/en/docs/install.html
- De start o servidor reverso ("start nginx")
- Abra no seu navegador neste link: https://localhost

Desfrute da aplicação