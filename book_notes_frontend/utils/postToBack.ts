import axios from 'axios';
import type { Book, Quote } from '../types/types';
const BASE_URL = "http://127.0.0.1:8000/";

export const postBook = async (data: Book) => {
  try {
    const response = await axios.post(`${BASE_URL}books/`, data, {
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

export const postAuthor = async (data: string) => {
  try {
    const response = await axios.post(`${BASE_URL}authors/`, data, {
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


export const postQuote = async (data: Quote) => {
  try {
    const response = await axios.post(`${BASE_URL}quotes/`, data, {
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