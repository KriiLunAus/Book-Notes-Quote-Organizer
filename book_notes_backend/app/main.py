from fastapi import FastAPI
from .routers import books, authors, quotes, markdown, json
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(quotes.router)
app.include_router(markdown.router)
app.include_router(json.router)

