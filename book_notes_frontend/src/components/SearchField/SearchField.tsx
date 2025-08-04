import { useEffect, useState, type JSX } from "react";
import css from "./SearchField.module.scss";
import type { Book } from "../../types/types.ts";

interface SearchFieldProps {
  allBooks: Book[];
  setBooks: React.Dispatch<React.SetStateAction<Book[] | undefined>>;
}

export default function SearchField({
  allBooks,
  setBooks,
}: SearchFieldProps): JSX.Element {
  const [searchField, setSearchField] = useState<string>("");

  useEffect(() => {
    const filteredBooks = allBooks.filter((book) =>
      book.title.toLowerCase().includes(searchField.toLowerCase())
    );
    setBooks(filteredBooks);
  }, [searchField, allBooks, setBooks]);

  return (
    <div className={css.searchField}>
      <input
        type="text"
        placeholder="Search by title..."
        value={searchField}
        onChange={(evt) => setSearchField(evt.target.value)}
      />
    </div>
  );
}
