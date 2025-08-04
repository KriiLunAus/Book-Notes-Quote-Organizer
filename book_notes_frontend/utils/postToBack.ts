import axios from 'axios';

const BASE_URL = "http://127.0.0.1:8000/";

export const postBook = async (data) => {
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

export const postAuthor = async (data) => {
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


export const postQuote = async (data) => {
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