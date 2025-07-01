import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const categories = [
  {
    name: 'phone',
    description: 'Mobile phones and smartphones',
    icon: '📱'
  },
  {
    name: 'laptop',
    description: 'Laptops and notebooks',
    icon: '💻'
  },
  {
    name: 'tablet',
    description: 'Tablets and iPads',
    icon: '📱'
  },
  {
    name: 'smartwatch',
    description: 'Smartwatches and wearables',
    icon: '⌚'
  },
  {
    name: 'headphones',
    description: 'Headphones and earphones',
    icon: '🎧'
  },
  {
    name: 'camera',
    description: 'Cameras and photography equipment',
    icon: '📸'
  },
  {
    name: 'television',
    description: 'Televisions and smart TVs',
    icon: '📺'
  },
  {
    name: 'refrigerator',
    description: 'Refrigerators and cooling appliances',
    icon: '❄️'
  },
  {
    name: 'washing machine',
    description: 'Washing machines and laundry appliances',
    icon: '🧺'
  }
];

const CategoryProducts = () => {
  const { category } = useParams();
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Find current category index
  const currentIndex = categories.findIndex(cat => cat.name === category);
  const prevCategory = currentIndex > 0 ? categories[currentIndex - 1].name : null;
  const nextCategory = currentIndex < categories.length - 1 ? categories[currentIndex + 1].name : null;

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`http://localhost:5000/api/products?category=${category}`);
        if (response.data.success) {
          setProducts(response.data.data);
        } else {
          setError('Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        setError('Error fetching products. Please try again later.');
      }
      setLoading(false);
    };

    fetchProducts();
  }, [category]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-sky-300 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/marketplace')}
              className="bg-white text-blue-600 px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
              Back to Categories
            </button>
          </div>
          <div className="flex items-center space-x-4">
            {prevCategory && (
              <button
                onClick={() => navigate(`/marketplace/${prevCategory}`)}
                className="bg-white text-blue-600 px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                {categories[currentIndex - 1].name}
              </button>
            )}
            {nextCategory && (
              <button
                onClick={() => navigate(`/marketplace/${nextCategory}`)}
                className="bg-white text-blue-600 px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center"
              >
                {categories[currentIndex + 1].name}
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </button>
            )}
          </div>
        </div>

        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 capitalize">{category} Products</h1>
          <p className="text-gray-600 mt-2">Browse through our selection of {category} products</p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : products.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <a 
                key={product._id} 
                href={product.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="group bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 block"
              >
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={product.image_url}
                    alt={product.title}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <div className="absolute bottom-2 left-2 right-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <div className="flex text-yellow-400">
                          {[...Array(5)].map((_, i) => (
                            <svg
                              key={i}
                              className={`w-3 h-3 ${i < (product.stars || 0) ? 'text-yellow-400' : 'text-gray-300'}`}
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                          ))}
                        </div>
                        <span className="text-white text-xs">{product.review_count}</span>
                      </div>
                      {product.sentiment_score && (
                        <div className="bg-white/90 backdrop-blur-sm rounded-full px-2 py-0.5">
                          <span className={`text-xs font-semibold ${
                            product.sentiment_score >= 4 ? 'text-green-600' : 
                            product.sentiment_score >= 3 ? 'text-yellow-600' : 'text-red-600'
                          }`}>
                            {product.sentiment_score.toFixed(1)}/5
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="text-sm font-medium text-gray-800 mb-1 line-clamp-2">{product.title}</h3>
                  <div className="flex items-center justify-between">
                    <p className="text-lg font-bold text-blue-600">{product.price}</p>
                    <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-3 py-1.5 rounded-md text-sm">
                      View on Daraz
                    </div>
                  </div>
                  <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
                    <span>{product.sold_count || '0 sold'}</span>
                    <span>{product.review_count || '0 reviews'}</span>
                  </div>
                  
                  {/* Reviews Section */}
                  {product.reviews && product.reviews.length > 0 && (
                    <div className="mt-3 border-t pt-3">
                      <h4 className="text-xs font-semibold text-gray-700 mb-2">Recent Reviews</h4>
                      <div className="space-y-2">
                        {product.reviews.slice(0, 2).map((review, index) => (
                          <div key={index} className="text-xs">
                            <div className="flex items-center mb-1">
                              <span className="font-medium text-gray-800">{review.reviewer}</span>
                              <div className="flex ml-2">
                                {[...Array(5)].map((_, i) => (
                                  <svg
                                    key={i}
                                    className={`w-2.5 h-2.5 ${i < review.rating ? 'text-yellow-400' : 'text-gray-300'}`}
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                  >
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                  </svg>
                                ))}
                              </div>
                            </div>
                            <p className="text-gray-600 line-clamp-2">{review.review}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Sentiment Analysis */}
                  {product.sentiment_score && (
                    <div className="mt-3 border-t pt-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-semibold text-gray-700">Sentiment Analysis</span>
                        <div className={`text-xs font-semibold ${
                          product.sentiment_score >= 4 ? 'text-green-600' : 
                          product.sentiment_score >= 3 ? 'text-yellow-600' : 'text-red-600'
                        }`}>
                          {product.sentiment_score.toFixed(1)}/5
                        </div>
                      </div>
                      <div className="mt-1">
                        <div className="w-full bg-gray-200 rounded-full h-1.5">
                          <div 
                            className={`h-1.5 rounded-full ${
                              product.sentiment_score >= 4 ? 'bg-green-500' : 
                              product.sentiment_score >= 3 ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${(product.sentiment_score / 5) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                      <div className="mt-1 text-xs text-gray-500">
                        {product.positive_reviews} out of {product.reviews?.length || 0} reviews are positive
                      </div>
                    </div>
                  )}
                </div>
              </a>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="text-4xl mb-3">😕</div>
            <p className="text-lg text-gray-600">No products found in this category.</p>
            <p className="text-sm text-gray-500 mt-1">Try selecting a different category or check back later.</p>
          </div>
        )}

        {/* Navigation buttons at the bottom */}
        <div className="flex justify-between mt-8">
          {prevCategory && (
            <button
              onClick={() => navigate(`/marketplace/${prevCategory}`)}
              className="bg-white text-blue-600 px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Previous: {categories[currentIndex - 1].name}
            </button>
          )}
          {nextCategory && (
            <button
              onClick={() => navigate(`/marketplace/${nextCategory}`)}
              className="bg-white text-blue-600 px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-shadow flex items-center"
            >
              Next: {categories[currentIndex + 1].name}
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default CategoryProducts; 