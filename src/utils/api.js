// import axios from 'axios';

// const API_URL = 'http://127.0.0.1:8000/api';

// export const recordInteraction = async (interaction) => {
//   try {
//     const response = await axios.post(`${API_URL}/interactions`, interaction);
//     return response.data;
//   } catch (error) {
//     console.error('Error recording interaction:', error);
//     throw error;
//   }
// };

// export const getRecommendations = async (uuid) => {
//   try {
//     const response = await axios.get(`${API_URL}/recommendations`, { params: { uuid } });
//     return response.data;
//   } catch (error) {
//     console.error('Error fetching recommendations:', error);
//     throw error;
//   }
// };

// export const searchProducts = async (params) => {
//   try {
//     const response = await axios.get(`${API_URL}/search`, { params });
//     return response.data;
//   } catch (error) {
//     console.error('Error searching products:', error);
//     throw error;
//   }
// };

// export const getSentiment = async (product_id, uuid) => {
//   try {
//     const response = await axios.get(`${API_URL}/sentiment/${product_id}`, { params: { uuid } });
//     return response.data;
//   } catch (error) {
//     console.error('Error fetching sentiment:', error);
//     throw error;
//   }
// };