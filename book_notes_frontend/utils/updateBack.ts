import axios from 'axios';

const BASE_URL = "http://127.0.0.1:8000/";


export const updateBook = async (id ,data) => {
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

export const updateQuote = async (id ,data) => {
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