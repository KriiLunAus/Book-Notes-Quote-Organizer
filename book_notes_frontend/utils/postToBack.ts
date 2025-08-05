import axios from 'axios';

import type { CreateQuoteInput, CreateBookInput } from '../src/types/types';
const BASE_URL = "http://fastapi_app:8000";

export const postBook = async (data: CreateBookInput) => {
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


export const postQuote = async (data: CreateQuoteInput) => {
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