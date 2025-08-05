import React, { useState, type JSX } from 'react';
import css from "./ModalForNewBook.module.scss";
import { postBook, postAuthor } from '../../../utils/postToBack';
import { fetchAuthors, fetchBooks } from '../../../utils/fetchFromBack';
import type { Book, Author } from "../../types/types.ts";


interface ModalForNewBookProps {
  setModal: React.Dispatch<React.SetStateAction<boolean>>;
  setBooks: React.Dispatch<React.SetStateAction<Book[] | undefined>>;
}

interface BookData {
  title?: string;
  author?: string;
}

interface PendingBook {
  title: string;
  authorName: string;
}

export default function ModalForNewBook({
  setModal,
  setBooks
}: ModalForNewBookProps): JSX.Element {
  const [bookData, setBookData] = useState<BookData>({});
  const [authorCreateModal, setAuthorCreateModal] = useState<boolean>(false);
  const [pendingBook, setPendingBook] = useState<PendingBook | null>(null);

  async function handleFindAuthorId(name: string): Promise<number | null | undefined> {
    try {
      const response: Author[] = await fetchAuthors();
      const author = response.find(obj => obj.name === name);
      return author ? author.id : null;
    } catch (err) {
      console.error(err);
    }
  }

  async function handlePostBook(e: React.FormEvent): Promise<void> {
    e.preventDefault();
    if (!bookData.title || !bookData.author) return;

    const authorId = await handleFindAuthorId(bookData.author);

    if (!authorId) {
      setAuthorCreateModal(true);
      setPendingBook({ title: bookData.title, authorName: bookData.author });
      return;
    }

    const data = {
      title: bookData.title,
      author_id: authorId
    };

    await postBook(JSON.stringify(data));
    const updatedBooks = await fetchBooks();
    setBooks(updatedBooks);
    setModal(false);
  }

  async function handleCreateAuthorAndBook(): Promise<void> {
    if (!pendingBook) return;

    try {
      await postAuthor(JSON.stringify({ name: pendingBook.authorName }));

      const newAuthorId = await handleFindAuthorId(pendingBook.authorName);
      if (newAuthorId) {
        await postBook(JSON.stringify({
          title: pendingBook.title,
          author_id: newAuthorId
        }));
      }

      const updatedBooks = await fetchBooks();
      setBooks(updatedBooks);
      setModal(false);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className={css.wrapper}>
      <div className={css.formWrapper}>
        <p>Create a book</p>
        <form onSubmit={handlePostBook}>
          <label>
            Book Title:
            <input
              onChange={(evt) => setBookData(prev => ({ ...prev, title: evt.target.value }))}
              type="text"
              required
            />
          </label>
          <label>
            Author:
            <input
              onChange={(evt) => setBookData(prev => ({ ...prev, author: evt.target.value }))}
              type="text"
              required
            />
          </label>
          <div className={css.buttonsInForm}>
            <button className={css.y} type="submit">Create</button>
            <button
              type="button"
              className={css.n}
              onClick={() => setModal(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      {authorCreateModal && (
        <div className={css.authorCreation}>
          <p>
            There is no author with name: <strong>{bookData.author}</strong>.<br />
            Would you like to create a new author with this name?
          </p>
          <button className={css.y} onClick={handleCreateAuthorAndBook}>Yes</button>
          <button className={css.n} onClick={() => setAuthorCreateModal(false)}>No</button>
        </div>
      )}
    </div>
  );
}
