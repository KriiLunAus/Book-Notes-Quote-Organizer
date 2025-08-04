export interface Book {
  id: number;
  title: string;
  author: {
    id: number;
    name: string;
  };
  quotes: {
    id: number;
    content: string;
    book_id: number;
  }[];
}