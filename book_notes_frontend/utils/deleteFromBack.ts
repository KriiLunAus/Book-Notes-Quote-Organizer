import axios from 'axios';

const BASE_URL = "http://fastapi_app:8000";

export const deleteBook = async (id: number) => {
  try {
    const response = await axios.delete(`${BASE_URL}books/${id}`)
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}

export const deleteQuote = async (id: number) => {
  try {
    const response = await axios.delete(`${BASE_URL}quotes/${id}`)
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}