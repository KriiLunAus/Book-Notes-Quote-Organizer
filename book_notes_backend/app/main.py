from fastapi import FastAPI
from .routers import books, authors, quotes
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(quotes.router)
