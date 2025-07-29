from pydantic import BaseModel
from typing import Optional, List

# Base models for shared fields


class AuthorBase(BaseModel):
    name: str


class BookBase(BaseModel):
    title: str
    
class QuoteBase(BaseModel):
    content: str
    tags: Optional[str] = ""

# Create/input models


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    pass


class QuoteCreate(QuoteBase):
    book_id: int

# Minimal nested models to break recursion in output


class AuthorNested(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class BookNested(BaseModel):
    id: int
    title: str

    model_config = {"from_attributes": True}

# Full output models


class AuthorOut(AuthorBase):
    id: int
    books: Optional[List[BookNested]] = []

    model_config = {"from_attributes": True}


class BookOut(BookBase):
    id: int
    author: AuthorNested

    model_config = {"from_attributes": True}


class QuoteOut(QuoteBase):
    id: int
    book: BookOut

    model_config = {"from_attributes": True}
