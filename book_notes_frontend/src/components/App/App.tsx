import { useState, useEffect, type JSX } from "react";
import { fetchSingleBook, fetchBooks } from "../../../utils/fetchFromBack.ts";
import { deleteBook } from "../../../utils/deleteFromBack.ts";
import css from './App.module.scss';
import BooksList from "../BooksList/BooksList.js";
import ModalForNewBook from '../ModalForNewBook/ModalForNewBook.js';
import ModalForBookDetails from "../ModalForBookDetails/ModalForBookDetails.js";
import type { Book } from "../../types/types.ts";

export default function App(): JSX.Element {
  const [createBookModal, setCreateBookModal] = useState<boolean>(false);
  const [bookDetailsModal, setBookDetailsModal] = useState<boolean>(false);    
  const [bookDetails, setBookDetails] = useState<Book | null>(null);    
  const [books, setBooks] = useState<Book[] | undefined>();
  const [allBooks, setAllBooks] = useState<Book[]>([]);

  useEffect(() => {
    async function getBooks() {    
      try {
        const response: Book[] = await fetchBooks();
        setBooks(response);
        setAllBooks(response);
      } catch (err) {
        console.error(err);
      }
    }
    getBooks();
  }, []);

  async function handleBookDelete(id: number): Promise<void> {
    try {
      await deleteBook(id);
      setBooks((prevBooks) => {
        if (prevBooks) {
          return prevBooks.filter(book => book.id !== id);
        }
      });
    } catch (err) {
      console.error(err);
    }
  }

  async function handleBookDetails(id: number): Promise<void> {
    try {
      const response: Book = await fetchSingleBook(id);
      setBookDetails(response);
      setBookDetailsModal(true);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <section className={css.appWrapper}>
      <BooksList 
        books={books}
        allBooks={allBooks}
        setBooks={setBooks}
        setCreateBookModal={setCreateBookModal} 
        handleBookDetails={handleBookDetails} 
        handleBookDelete={handleBookDelete}
      />
      
      {createBookModal && (
        <ModalForNewBook 
          setBooks={setBooks} 
          setModal={setCreateBookModal} 
        />
      )}

      {bookDetailsModal && bookDetails && (
        <ModalForBookDetails 
          setModal={setBookDetailsModal} 
          bookDetails={bookDetails} 
          handleBookDetails={handleBookDetails}
        />
      )}
    </section>
  );
}

