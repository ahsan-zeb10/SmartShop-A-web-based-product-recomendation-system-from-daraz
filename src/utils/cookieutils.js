// import Cookies from 'js-cookie';
// import axios from 'axios';

// const API_URL = 'http://127.0.0.1:8000/api';

// export const getUserId = async () => {
//   let userId = Cookies.get('userId');
//   if (!userId) {
//     const response = await axios.get(`${API_URL}/user-id`);
//     userId = response.data.user_id;
//     Cookies.set('userId', userId, { expires: 365 });
//   }
//   return userId;
// };

// export const recordInteraction = async (interactionType, data) => {
//   try {
//     const userId = await getUserId();
//     await axios.post(`${API_URL}/interactions`, { user_id: userId, interaction_type: interactionType, data });
//   } catch (error) {
//     console.error('Error recording interaction:', error);
//   }
// };