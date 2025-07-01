// const express = require('express');
// const cors = require('cors');
// const dotenv = require('dotenv');
// const { getProducts } = require('./api');

// dotenv.config();

// const app = express();
// app.use(cors());
// app.use(express.json());

// app.get('/api/products', async (req, res) => {
//   const { searchTerm } = req.query; // Get searchTerm from the query string

//   if (!searchTerm) {
//     return res.status(400).json({ error: 'Search term is required' });
//   }

//   try {
//     const products = await getProducts(searchTerm);
//     res.json(products); // Send the products data as the response
//   } catch (error) {
//     res.status(500).json({ error: error.message });
//   }
// });

// const PORT = process.env.PORT || 5000;
// app.listen(PORT, () => {
//   console.log(`Server is running on port ${PORT}`);
// });


