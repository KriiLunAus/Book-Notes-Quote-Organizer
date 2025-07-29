from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")
    quotes = relationship("Quote", back_populates="book")


class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    tags = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'))

    book = relationship("Book", back_populates="quotes")
