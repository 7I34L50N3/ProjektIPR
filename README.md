# Aplikacja wspomagająca naukę języków

Projekt aplikacji webowej służącej do wspomagania nauki języków obcych. Interfejs graficzny został zainspirowany designem platformy GitHub.

<img width="960" height="462" alt="image" src="https://github.com/user-attachments/assets/49ad3519-be2e-492f-978c-769c4403a96a" />


## Stan obecny
W aktualnej wersji zaimplementowano:
- Panel logowania.
- Bazową klasę użytkownika, która stanowi fundament dla pozostałych ról (aktorów) w systemie.

## Środowiska uruchomieniowe
Aplikację można uruchomić na dwa sposoby:
- **Lokalnie** (bezpośrednio w środowisku Python).
- **W kontenerze** (przy wykorzystaniu platformy Docker).

---

## Instrukcja uruchomienia

### 1. Uruchomienie lokalne
Aby uruchomić aplikację w klasycznym środowisku programistycznym (np. PyCharm):
- Należy otworzyć plik głównego skryptu `app.py`.
- Uruchomić plik standardowo z poziomu IDE lub wykonując w terminalu poniższe polecenie:
```
  python app.py
 ```

### 2. Uruchomienie przy użyciu platformy Docker

Uruchomienie w kontenerze wymaga odpowiedniego przygotowania środowiska systemowego.

**Wymagania wstępne (dla systemu Windows):**

* Zainstalowany komponent WSL 2 (Windows Subsystem for Linux).
* Zainstalowane środowisko Docker (np. aplikacja Docker Desktop).

**Kroki uruchomieniowe:**

* Należy uruchomić wiersz poleceń (np. zintegrowany terminal w środowisku PyCharm).
* Zbudować i uruchomić kontener za pomocą polecenia:
```bash
docker-compose up --build
```

---

## Dostęp do aplikacji

Po poprawnym zainicjowaniu (niezależnie od wybranej metody), aplikacja jest dostępna w przeglądarce internetowej pod adresem:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
