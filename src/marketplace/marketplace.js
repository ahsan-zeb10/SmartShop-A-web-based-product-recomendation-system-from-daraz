import React from 'react';
import { useNavigate } from 'react-router-dom';

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

const Marketplace = () => {
  const navigate = useNavigate();

  const handleCategoryClick = (category) => {
    navigate(`/marketplace/${category}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-sky-300 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Explore Categories</h1>
          <p className="text-xl text-gray-600">Discover products across various categories</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {categories.map((category) => (
            <div 
              key={category.name} 
              className={`group bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 cursor-pointer`}
              onClick={() => handleCategoryClick(category.name)}
            >
              <div className="p-4">
                <div className="text-3xl mb-2">{category.icon}</div>
                <h2 className="text-lg font-semibold text-gray-800 mb-1 capitalize">{category.name}</h2>
                <p className="text-sm text-gray-600">{category.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Marketplace; 