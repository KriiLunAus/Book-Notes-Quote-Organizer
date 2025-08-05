export interface Quote {
  id: number;
  content: string;
  tags?: string;
  book_id: number;
}

export interface CreateQuoteInput {
  content: string;
  tags?: string;
  book_id: number;
}

export interface Book {
  id: number;
  title: string;
  author: {
    id: number;
    name: string;
  };
  quotes: Quote[];
}

export interface CreateBookInput {
  title: string;
  author_id : number;
}

export interface Author {
  id: number;
  name: string;
}

