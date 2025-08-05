import axios from 'axios';
import type { Book, CreateQuoteInput } from '../src/types/types';
const BASE_URL = "http://fastapi_app:8000";




export const updateBook = async (id: number, data: Partial<Book>) => {
  try {
    const response = await axios.put(`${BASE_URL}books/${id}`, data, {
      headers:{
        "Content-Type" : "application/json",
      }
    })
    return response.data;
  } catch (error) {
    console.error('Error during creating the book:', error);
    throw error;
  }
}

export const updateQuote = async (id: number, data: CreateQuoteInput) => {
  try {
    const response = await axios.put(`${BASE_URL}quotes/${id}`, data, {
      headers:{
        "Content-Type" : "application/json",
      }
    })
    return response.data;
  } catch (error) {
    console.error('Error during creating the book:', error);
    throw error;
  }
}