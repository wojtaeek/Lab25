# Lab 25

Projekt Django służący do zarządzania ofertą kursów, kategoriami oraz
rejestracją uczestników.

## Funkcjonalności

- Dodawanie, edycja i usuwanie kategorii kursów
- Dodawanie, edycja i usuwanie kursów
- Publikowanie/ukrywanie kursów i kategorii (pole "publish")
- Rejestracja użytkowników na kursy przez formularz
- Zarządzanie zgłoszeniami na kursy
- Obsługa statusów zgłoszeń (np. otwarte/zamknięte)
- Prosty system zgłaszania i zamykania "issue"
- Przechowywanie schematów i formularzy w plikach

## Wymagania

- Python 3.8+
- Django 3.2+
- Baza danych SQLite (domyślnie) lub inna obsługiwana przez Django

## Instalacja

1. Sklonuj repozytorium:

   ```bash
   git clone <adres_repozytorium>
   cd <nazwa_katalogu>
   ```

2. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

3. Wykonaj migracje:

   ```bash
   python manage.py migrate
   ```

4. Uruchom serwer deweloperski:

   ```bash
   python manage.py runserver
   ```

5. Otwórz przeglądarkę i przejdź pod adres: [http://localhost:8000/](http://localhost:8000/)

6. Alternatywnie, możesz użyć Docker:

    ```bash
    docker-compose up --build
    ```

## Użytkowanie

- Panel administracyjny: `/admin/`
- Dodawanie kategorii i kursów: odpowiednie zakładki w panelu
- Rejestracja na kurs: formularz dostępny na stronie kursu

## Struktura projektu

```
.
├── app
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_button.py
│   │   ├── 0003_issue.py
│   │   ├── 0004_alter_category_parent_category.py
│   │   ├── 0005_alter_category_order_alter_course_order.py
│   │   └── __init__.py
│   ├── models.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── partials
│   │   │   ├── add_category.html
│   │   │   ├── add_course.html
│   │   │   ├── category.html
│   │   │   ├── course_detail.html
│   │   │   ├── course.html
│   │   │   ├── issue.html
│   │   │   ├── navbar.html
│   │   │   ├── panel_oferta.html
│   │   │   ├── register.html
│   │   │   └── template.html
│   │   └── registration
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docker-compose.yml
├── Dockerfile
├── Lab25
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── media
│   ├── form_1.json
│   ├── form_2.json
│   ├── form_3.json
│   ├── form_4.json
│   ├── schema_1.txt
│   ├── schema_2.txt
│   └── schema_3.txt
├── README.md
├── requirements.txt
└── static
    └── javascript
        └── js.js
```
