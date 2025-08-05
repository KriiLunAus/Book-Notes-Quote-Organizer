import { ImCross } from "react-icons/im";
import { useState, useEffect } from "react";
import { FaTrashCan,  FaPen } from "react-icons/fa6";
import { FaExchangeAlt } from "react-icons/fa";
import { postQuote } from "../../../utils/postToBack.ts";
import { deleteQuote } from "../../../utils/deleteFromBack.ts";
import { updateQuote } from "../../../utils/updateBack.ts";
import css from "./ModalForBookDetails.module.scss";
import type { Quote, Book, CreateQuoteInput } from "../../types/types.ts";

interface Props {
  setModal: (value: boolean) => void;
  bookDetails: Book;
  handleBookDetails: (id: number) => Promise<void>;
}

export default function ModalForBookDetails({
  setModal,
  bookDetails,
  handleBookDetails,
}: Props) {
  const [expandedQuotes, setExpandedQuotes] = useState<Record<number, boolean>>({});
  const [newNoteForm, setNewNoteForm] = useState(false);
  const [newNoteData, setNewNoteData] = useState<CreateQuoteInput>({ content: "", tags: "", book_id: 0});
  const [editingQuoteId, setEditingQuoteId] = useState<number | null>(null);
  const [quoteUpdateData, setQuoteUpdateData] = useState({ content: "", tags: "", book_id: 0});
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);


  useEffect(() => {
    setNewNoteForm(false);
    setEditingQuoteId(null);
    setNewNoteData({ content: "", tags: "", book_id: bookDetails.id });

    const tagsSet = new Set<string>();
    bookDetails.quotes.forEach((quote) => {
      if (quote.tags) {
        quote.tags.split(",").forEach((tag) => {
          const trimmed = tag.trim();
          if (trimmed) tagsSet.add(trimmed);
        });
      }else{
        tagsSet.add("No tags")
      }
    });
    setAvailableTags(Array.from(tagsSet));
    }, [bookDetails.id, bookDetails.quotes]);

  const toggleQuote = (id: number) => {
    setExpandedQuotes((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  async function handlePostQuote(data: CreateQuoteInput) {
    await postQuote(data);
    await handleBookDetails(bookDetails.id);
    setNewNoteForm(false);
  }

  async function handleDeleteQuote(id: number) {
    await deleteQuote(id);
    await handleBookDetails(bookDetails.id);
  }

  function startEditing(quote: Quote) {
    setEditingQuoteId(quote.id);
    setQuoteUpdateData({
      content: quote.content,
      tags: quote.tags || "",
      book_id: bookDetails.id,
    });
  }

  async function handleUpdateQuote(id: number) {
    await updateQuote(id, quoteUpdateData);
    setEditingQuoteId(null);
    await handleBookDetails(bookDetails.id);
  }

  return (
    <div className={css.bookDetailsWrapper}>
      <div onClick={() => setModal(false)} className={css.exitBookDetails}>
        <ImCross color="darkgray" />
      </div>
      <div>
        <h2>{bookDetails.title}</h2>
        <p>
          <strong>Author:</strong> {bookDetails.author.name}
        </p>

      <div className={css.tagFilterSection}>
  <h4>Filter by tags:</h4>
  {availableTags.map((tag) => (
    <label key={tag} className={css.tagFilterLabel}>
      <input
        type="checkbox"
        value={tag}
        checked={selectedTags.includes(tag)}
        onChange={() => {
          setSelectedTags((prev) =>
            prev.includes(tag)
              ? prev.filter((t) => t !== tag)
              : [...prev, tag]
          );
        }}
      />
      #{tag}
    </label>
  ))}
</div>

        {!newNoteForm && <ul>
          {bookDetails.quotes
          .filter((quote) => {
            if (selectedTags.length === 0) return true;

            const hasTags = !!quote.tags && quote.tags.trim() !== "";

            if (selectedTags.includes("No tags")) {
              return !hasTags;
            }

            if (!hasTags) return false;
            if(quote.tags !== undefined){
              const quoteTags = quote.tags.split(",").map((tag) => tag.trim()); 
              return selectedTags.every((selected) => quoteTags.includes(selected));
            }
            })
          .map((quote) => (
            <li key={quote.id} className={css.quoteItem}>
              <div
                onClick={() => handleDeleteQuote(quote.id)}
                className={css.deleteQuoteBtn}
              >
                <FaTrashCan color="red" />
              </div>

              {editingQuoteId === quote.id ? (
                <>
                  <label className={css.updateQuoteFields}>
                    Note/Quote:
                    <textarea
                      value={quoteUpdateData.content}
                      onChange={(e) =>
                        setQuoteUpdateData((prev) => ({
                          ...prev,
                          content: e.target.value,
                        }))
                      }
                    />
                  </label>
                  <label className={css.updateQuoteFields}>
                    Tags:
                    <input
                      type="text"
                      value={quoteUpdateData.tags}
                      onChange={(e) =>
                        setQuoteUpdateData((prev) => ({
                          ...prev,
                          tags: e.target.value,
                        }))
                      }
                    />
                  </label>
                  <FaExchangeAlt  
                    onClick={() => handleUpdateQuote(quote.id)}
                    className={css.updateQuoteBtn}/>
                  <ImCross onClick={() => setEditingQuoteId(null)}
                    className={css.closeUpdateWindow}/>
                </>
              ) : (
                <>
                  <div
                    onClick={() => startEditing(quote)}
                    className={css.updateBtn}
                    title="Edit quote"
                  >
                    <FaPen />
                  </div>
                  <p
                    className={`${css.quoteContent} ${
                      expandedQuotes[quote.id] ? css.expanded : ""
                    }`}
                    onClick={() => toggleQuote(quote.id)}
                    title="Click to expand/collapse"
                  >
                    "{quote.content}"
                  </p>
                  {quote.tags && (
                    <p className={css.tagLine}>
                      <strong>Tags:</strong>{" "}
                      {quote.tags.split(",").map((tag, index) => (
                        <span key={index} className={css.tag}>
                          #{tag}
                        </span>
                      ))}
                    </p>
                  )}
                </>
              )}
            </li>
          ))}

          <li>
              <button
                onClick={() => setNewNoteForm(true)}
                className={css.addNewNoteBtn}
              >
                Add new note/quote
              </button>
          </li>
        </ul>}

        {newNoteForm && (
          <form
            onSubmit={(evt) => {
              evt.preventDefault();
              handlePostQuote(newNoteData);
            }}
            className={css.addQuoteForm}
          >
            <label>
              New Note/Quote:
              <textarea
                onChange={(evt) =>
                  setNewNoteData((prev) => ({
                    ...prev,
                    content: evt.target.value,
                  }))
                }
                id="note"
                name="note"
              />
            </label>
            <label>
              Tags:
              <input
                onChange={(evt) =>
                  setNewNoteData((prev) => ({
                    ...prev,
                    tags: evt.target.value,
                  }))
                }
                id="tags"
                name="tags"
                type="text"
              />
            </label>
            <button type="submit" className={css.addNewNoteBtn}>
              Add new note
            </button>
            <button
              type="button"
              onClick={() => setNewNoteForm(false)}
              className={css.closeForm}
            >
              Close form
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
