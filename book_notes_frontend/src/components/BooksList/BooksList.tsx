import { type JSX } from 'react';
import css from "./BooksList.module.scss";
import BookPreview from '../BookPreview/BookPreview';
import SearchField from '../SearchField/SearchField';
import type { Book } from "../../types/types.ts";

interface BooksListProps {
  book: Book;
  books: Book[] | undefined;
  allBooks: Book[];
  setBooks: React.Dispatch<React.SetStateAction<Book[] | undefined>>;
  setCreateBookModal: React.Dispatch<React.SetStateAction<boolean>>;
  handleBookDelete: (id: number) => void;
  handleBookDetails: (id: number) => void;
}

export default function BooksList({
  books,
  allBooks,
  setBooks,
  setCreateBookModal,
  handleBookDelete,
  handleBookDetails
}: BooksListProps): JSX.Element {

  return (
    <div className={css.wrapper}>
      <SearchField allBooks={allBooks} setBooks={setBooks} />

      {books !== undefined && books.map((book) => (
        <BookPreview
          key={book.id}
          book={book}
          setBooks={setBooks}
          handleBookDetails={handleBookDetails}
          handleBookDelete={handleBookDelete}
        />
      ))}

      <button
        className={css.createBookBtn}
        onClick={() => setCreateBookModal(true)}
      >
        Create new book
      </button>
    </div>
  );
}
