import { v4 as uuidv4 } from 'uuid';
import Cookies from 'js-cookie';

const UUID_KEY = 'smartshop_user_uuid';
const INTERACTIONS_KEY = 'smartshop_interactions';

export const getUserUUID = () => {
  let uuid = Cookies.get(UUID_KEY) || localStorage.getItem(UUID_KEY);
  if (!uuid) {
    uuid = uuidv4();
    Cookies.set(UUID_KEY, uuid, { expires: 365 }); // 1 year
    localStorage.setItem(UUID_KEY, uuid);
  }
  return uuid;
};

export const recordInteractionLocally = (interaction) => {
  let interactions = JSON.parse(localStorage.getItem(INTERACTIONS_KEY) || '[]');
  interactions.push({ ...interaction, timestamp: Date.now() });
  if (interactions.length > 100) {
    interactions = interactions.slice(-100); // Keep last 100 interactions
  }
  localStorage.setItem(INTERACTIONS_KEY, JSON.stringify(interactions));
};

export const getLocalInteractions = () => {
  return JSON.parse(localStorage.getItem(INTERACTIONS_KEY) || '[]');
};

export const syncInteractions = async (axiosInstance) => {
  const uuid = getUserUUID();
  const interactions = getLocalInteractions();
  if (!interactions.length) return;

  try {
    for (const interaction of interactions) {
      await axiosInstance.post('/api/interaction', {
        uuid,
        type: interaction.type,
        query: interaction.query || null,
        product_id: interaction.product_id || null
      });
    }
    localStorage.setItem(INTERACTIONS_KEY, '[]'); // Clear after sync
  } catch (error) {
    console.error('Failed to sync interactions:', error);
  }
};