# Cocktail Manager API

Projekt REST API służący do zarządzania przepisami na koktajle, ich składnikami oraz recenzjami użytkowników. Aplikacja została stworzona przy użyciu Django REST Framework.

## Zrealizowane wymagania

W projekcie zaimplementowano w 100% wymagania podstawowe oraz pokryto sekcję **Nice to have**:

* **Pełny CRUD:** Tworzenie, odczyt, aktualizacja i usuwanie koktajli oraz składników.
* **Baza danych:** Zaprojektowana relacyjna baza danych (SQLite). Do repozytorium dołączono plik `Schemat_bazy_danych.png` przedstawiający diagram ze wszystkimi relacjami i kluczami obcymi.
* **Paginacja i Walidacja:** Wyniki są stronicowane, a błędne dane wejściowe zwracają odpowiednie kody błędów.
* **Autoryzacja i Uprawnienia:** 
  * Każdy może przeglądać listę przepisów i składników.
  * Tylko zalogowany użytkownik może dodać koktajl lub napisać recenzję.
  * Tylko autor przepisu lub Administrator posiada uprawnienia do jego edycji oraz usunięcia.
* **Złożone filtrowanie:** Możliwość filtrowania koktajli po kategorii, a także sortowania i wyszukiwania tekstowego w nazwie.
* **Testy automatyczne:** Napisane testy integracyjne sprawdzające autoryzację, tworzenie obiektów i filtrowanie.
* **Dokumentacja API (Swagger):** W pełni interaktywna, automatycznie wygenerowana dokumentacja zgodna ze standardem OpenAPI.

## Technologie

* Python 3
* Django
* Django REST Framework (DRF)
* drf-spectacular (Swagger)
* django-filter
* SQLite

## Instrukcja uruchomienia (lokalnie)

1. **Sklonuj repozytorium i przejdź do folderu projektu:**
   ```bash
   git clone https://github.com/AnnaPalinska/cocktail-manager-api.git
   cd cocktail-manager-api