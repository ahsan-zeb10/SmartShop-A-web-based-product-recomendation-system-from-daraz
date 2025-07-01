import React, { useState } from 'react';
import { searchProducts, recordInteraction } from '../utils/api';
import { getUserUUID } from '../utils/uuidUtils';
import { useNavigate } from 'react-router-dom';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const uuid = getUserUUID();
  const navigate = useNavigate();

  const handleSearch = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await searchProducts({ query, page: 1, limit: 20, uuid });
      setProducts(response.data || []);
    } catch (err) {
      setError('Failed to search products');
    } finally {
      setLoading(false);
    }
  };

  const handleProductClick = async (product) => {
    try {
      await recordInteraction({
        uuid,
        action: 'click',
        product_id: product._id,
        category: product.category
      });
      navigate(`/product/${product._id}`);
    } catch (err) {
      console.error('Error recording click:', err);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <div className="flex mb-4">
        <input
          type="text"
          placeholder="Search products..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow p-2 border rounded-l-md focus:outline-none"
        />
        <button
          onClick={handleSearch}
          className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600"
        >
          Search
        </button>
      </div>
      {loading && <div className="text-center py-4">Loading...</div>}
      {error && <div className="text-red-500 text-center py-4">{error}</div>}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {products.map((item) => (
          <div
            key={item._id}
            className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
            onClick={() => handleProductClick(item)}
          >
            <img
              src={item.image_url}
              alt={item.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h3 className="text-lg font-semibold truncate">{item.title}</h3>
              <p className="text-gray-600">Rs. {item.price.toLocaleString()}</p>
              <p className="text-yellow-500">{item.stars} stars</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchPage;