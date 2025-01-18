# Aplikacja wspomagająca naukę języków

W obecnej wersji utworzyłem panel do logowania, 
a także klasę użytkownika, która posłuży nam 
jako klasa bazowa dla reszty użytkowników (aktorów)
korzystających z systemu. 

#### Apka ma wygląd podobny do Githuba.

### Aplikacja działa:
* lokalnie
* przy wykorzystaniu dockera - trzeba mieć dockera

### Aby uruchomić apkę lokalnie:
* wchodzimy w plik ze skryptem *app.py*
* uruchamiamy jak normalny program w Pycharmie

### Aby uruchomić apkę z Dockera:
* instalujemy WSL (w wersji 2)
* instalujemy Dockera (np. Docker desktop)
* uruchamiamy instancję terminala w Pycharm

### Korzystanie z aplikacji:
* uruchamiamy komendą:
  ```bash
  docker-compose up --build
  ```
  
* po wyłączeniu usuwamy kontener:
  ```bash
  docker-compose down -v
  ```