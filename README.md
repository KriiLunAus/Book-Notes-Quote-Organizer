# 📚 Book Notes & Quote Organizer

A simple and efficient web app to log books and store memorable quotes. Users can tag quotes for easy filtering and export their notes to Markdown for future use.

---

## 🛠 Tech Stack

- **Backend**: FastAPI  
- **Database**: PostgreSQL  
- **Frontend**: React (Vite)  

---

## ✨ Features

- 📖 CRUD operations for books and quotes 
- 📝 Add and tag quotes  
- 🔍 Filter quotes by tags (including "untagged" quotes)  
- ⬇️ Export notes to Markdown  

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Node.js 
- Docker 

---

## ⚙️ Backend Setup (FastAPI)

```bash
# Clone the repo and navigate to backend
git clone https://github.com/kriilunaus/book-notes-quote-organizer.git
cd book-notes-quote-organizer/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
To run this project, you will need to add the following environment variables to your .env file

"DB_HOST"
"DB_PORT"
"DATABASE_URL"

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload

```

## 🖥️Frontend setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

## 🐳 Docker

Make sure you have Docker and Docker Compose installed.


```bash
# Run the app:
docker-compose up --build

# To stop containers:
docker-compose down
```

## 📦 API Endpoints

| Method | Endpoint         | Description                  |
| ------ | ---------------- | ---------------------------- |
| GET    | /books           | List all books               |
| POST   | /books           | Create a new book            |
| PUT    | /books/{id}      | Update book info             |
| DELETE | /books/{id}      | Delete a book                |
| GET    | /quotes          | List quotes with tags filter |
| POST   | /quotes          | Add a quote                  |
| PUT    | /quotes/{id}     | Update a quote               |
| POST   | /quotes/{id}     | Delete a quote               |
| GET    | /export/markdown | Export all books to markdown |
| GET    | /export/json     | Export all books to json     |
 
Full interactive API docs available at /docs (Swagger UI).


## 📂 Project Structure

```arduino

book-notes-quote-organizer/
│
├── backend/
│   ├── app/  
|   |   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
