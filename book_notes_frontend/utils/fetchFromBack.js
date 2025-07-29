import axios from 'axios';

const BASE_URL = "http://127.0.0.1:8000/";

export const fetchAuthors = async () => {
  try {
    const response = await axios.get(`${BASE_URL}authors/`)
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}

export const fetchBooks = async () => {
  try {
    const response = await axios.get(`${BASE_URL}books/`)
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}

export const fetchJSON = async () => {
  try {
    const response = await axios.get(`${BASE_URL}export/json`)
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}

export const fetchQuoteTags = async () => {
  try {
    const response = await axios.get(`${BASE_URL}quotes/tags`)
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}