// const axios = require('axios');
// const HmacSHA256 = require('crypto-js/hmac-sha256');
// const encHex = require('crypto-js/enc-hex');

// const appKey = '503026'; // Your app key from Daraz
// const appSecret = 'jY4Vp21A4e2OdPcrmFy1HRGblpX93Wxu'; // Your app secret from Daraz

// // Function to generate the access token
// const generateAccessToken = async () => {
//   const timestamp = Math.floor(Date.now());
//   const signMethod = 'HMAC-SHA256';

//   // Create the query string for token request
//   const queryString = `app_key=${appKey}&timestamp=${timestamp}&sign_method=${signMethod}`;

//   // Generate the signature
//   const sign = HmacSHA256(queryString, appSecret).toString(encHex);

//   // Create the URL for token request
//   const url = `https://api.daraz.pk/rest/v1/auth/token/create?${queryString}&sign=${sign}`;

//   try {
//     const response = await axios.get(url);
//     if (response.data && response.data.access_token) {
//       console.log('Access Token:', response.data.access_token);
//       return response.data.access_token;
//     } else {
//       throw new Error('Failed to retrieve access token');
//     }
//   } catch (error) {
//     console.error('Error fetching access token:', error.response?.data || error.message);
//     throw error;
//   }
// };

// // Function to get products using the access token and various filters
// const getProducts = async (searchTerm) => {
//   try {
//     const accessToken = await generateAccessToken(); // Generate access token
//     const currentTimestamp = Math.floor(Date.now() / 1000); // Current Unix timestamp in seconds
//     const timestamp = currentTimestamp * 1000; // Convert to milliseconds

//     const signMethod = 'HMAC-SHA256'; // Signing method

//     // Define the filters and parameters
//     const limit = '10';
//     const options = '1'; // ReservedStock, RtsStock, PendingStock, RealTimeStock, FulfillmentBySellable
//     const sku_seller_list = '["39817:01:01", "Apple 6S Black"]'; // Example SKU list
//     const offset = '0'; // Deprecated, can be replaced with date for scrolling query
//     const filter = 'live'; // Possible values: all, live, inactive, deleted, image-missing, pending, rejected, sold-out
//     const update_before = '2018-01-01T00:00:00+0800'; // Optional, date filter for updates
//     const create_before = '2018-01-01T00:00:00+0800'; // Optional, date filter for creation
//     const create_after = '2010-01-01T00:00:00+0800'; // Optional, date filter for creation
//     const update_after = '2010-01-01T00:00:00+0800'; // Optional, date filter for updates

//     // Build the query string with all required parameters and filters
//     const queryString = `app_key=${appKey}&timestamp=${timestamp}&sign_method=${signMethod}&search=${encodeURIComponent(searchTerm)}&access_token=${accessToken}&limit=${limit}&options=${options}&sku_seller_list=${sku_seller_list}&offset=${offset}&filter=${filter}&update_before=${update_before}&create_before=${create_before}&create_after=${create_after}&update_after=${update_after}`;

//     // Log the query string for debugging
//     console.log('Query String:', queryString);

//     // Generate HMAC Signature
//     const sign = HmacSHA256(queryString, appSecret);
//     const signHex = sign.toString(encHex);

//     // Log the full URL for debugging
//     const url = `https://api.daraz.pk/rest/v1/product/search?${queryString}&sign=${signHex}`;
//     console.log('Full API URL:', url);

//     // Fetch the products from the API
//     const response = await axios.get(url);

//     // Check if the response has products
//     if (response.data && response.data.products) {
//       console.log('Products:', response.data.products);
//       return response.data.products;
//     } else {
//       throw new Error('No products found.');
//     }
//   } catch (error) {
//     console.error('Error fetching products:', error.message);
//     throw new Error('Failed to fetch products');
//   }
// };

// // Example: Search for products with the keyword 'mobile'
// getProducts('mobile').then((products) => {
//   console.log('Fetched Products:', products);
// }).catch((error) => {
//   console.error('Error:', error.message);
// });


