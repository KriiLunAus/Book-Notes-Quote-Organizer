import React, { useState, useEffect, type JSX } from 'react';
import { FaTrashCan } from "react-icons/fa6";
import { FaExchangeAlt } from "react-icons/fa";
import { ImCross } from "react-icons/im";
import { FaPen } from "react-icons/fa";
import css from "./BookPreview.module.scss";
import { updateBook } from "../../../utils/updateBack";
import type { Book } from "../../types/types.ts";

interface BookPreviewProps {
  book: Book;
  setBooks: React.Dispatch<React.SetStateAction<Book[] | undefined>>;
  handleBookDelete: (id: number) => void;
  handleBookDetails: (id: number) => void;
}

export default function BookPreview({
  book,
  setBooks,
  handleBookDelete,
  handleBookDetails
}: BookPreviewProps): JSX.Element {
  
  const [updateBookField, setUpdateBookField] = useState<boolean>(false);
  const [inputValue, setInputValue] = useState<string>(book.title);

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        setUpdateBookField(false);
        setInputValue(book.title);
      }
    }

    if (updateBookField) {
      window.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [updateBookField, book.title]);

  async function handleBookUpdate(id: number, title: string, authorId: number): Promise<void> {
    const data = { title: title, author_id: authorId };

    try {
      await updateBook(id, data);

      setBooks(prevBooks =>
        prevBooks?.map(book =>
          book.id === id ? { ...book, title } : book
        )
      );

      setUpdateBookField(false);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className={css.bookCard}>
      <div onClick={() => handleBookDelete(book.id)} className={css.deleteBookBtn}>
        <FaTrashCan color='red' />
      </div>

      {!updateBookField ? (
        <div onClick={() => setUpdateBookField(true)} className={css.updateBookBtn}>
          <FaPen color='black' />
        </div>
      ) : (
        <div onClick={() => setUpdateBookField(false)} className={css.updateBookBtn}>
          <ImCross color='black' />
        </div>
      )}

      {updateBookField ? (
        <label>
          <input
            type="text"
            onChange={(e) => setInputValue(e.target.value)}
            value={inputValue}
          />
          <FaExchangeAlt
            onClick={() => handleBookUpdate(book.id, inputValue, book.author.id)}
            className={css.writeChanges}
          />
        </label>
      ) : (
        <h2 onClick={() => handleBookDetails(book.id)}>{book.title}</h2>
      )}

      <p className={css.authorName}>{book.author.name}</p>
    </div>
  );
}
