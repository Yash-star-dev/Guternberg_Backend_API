📚 Project Gutenberg Books API
A Django REST API to explore public domain books from Project Gutenberg. It supports detailed filtering, rich metadata, and efficient pagination.

✨ Key Features
🔎 Filter by ID, title, author, language, MIME type, subject, or bookshelf via query params

👨‍💻 Rich metadata: authors, subjects, languages, bookshelves, formats

📄 Download links in plain text, HTML, EPUB, and more

📚 Optimized ORM with select_related/prefetch_related for relationships

📦 Pagination: 25 results per page

🛠️ PostgreSQL-backed using Project Gutenberg data dump

📘 Clean JSON output via DRF serializers

## Project Structure

```
gutenberg_api_pro/
├── gutenberg_api_pro/      # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/                  # Django app for books API
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Technologies Used
1. Python 3

2. Django

3. python-dotenv (for managing .env configs)

## Installation

2. Create virtual env

```bash
cd project/
python3 -m venv env
source env/bin/activate
```
3. Install depndance
```bash
pip install -r requirements.txt
```
4. Create ".env"
```bash
DB_NAME=DB_NAME
DB_USER=POSTGRES_USER_NAME
DB_PASSWORD=POSTGRES_PASSWORD
DB_HOST=db_postgres
DB_PORT=POSTGRES_PORT

```

4. Run server

```bash
python3 manage.py run server
```

5. Docker (optional)

```bash
docker compose up --build
```
6. Now, you can access the api in postman
```bash
http://localhost:8000/api/books/?book_id=84&language=en&mime_type=text/plain&topic=Fiction&author=Austen&title=Pride
```
7. Now, you can access the api in swagger
```bash
http://127.0.0.1:8000/swagger/
```
8. Parame filter:
```bash
book_id:
language:
mime_type:text/plain
topic:Fiction
author:Austen
title:Pride
```