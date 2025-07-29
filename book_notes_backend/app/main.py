from fastapi import FastAPI
from .routers import books, authors, quotes, markdown, json
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(books.router)
app.include_router(authors.router)
app.include_router(quotes.router)
app.include_router(markdown.router)
app.include_router(json.router)
