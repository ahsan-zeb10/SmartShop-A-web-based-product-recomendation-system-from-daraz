import React from 'react';

const features = [
  {
    title: 'Smart Recommendations',
    description: 'Get personalized product suggestions based on real user reviews and sentiment analysis.',
    icon: '🤖'
  },
  {
    title: 'Real User Reviews',
    description: 'Access authentic user experiences and make informed purchasing decisions.',
    icon: '📝'
  },
  {
    title: 'Sentiment Analysis',
    description: 'Our AI analyzes thousands of reviews to provide accurate product insights.',
    icon: '🧠'
  },
  {
    title: 'Easy Comparison',
    description: 'Compare products based on ratings, reviews, and sentiment scores.',
    icon: '⚖️'
  }
];

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-sky-300 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">About SmartShop</h1>
          <p className="text-xl text-gray-600">Making online shopping smarter and more reliable</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8 mb-12 transform hover:scale-[1.01] transition-transform duration-300">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">What is SmartShop?</h2>
          <p className="text-gray-600 text-lg leading-relaxed">
            SmartShop is an intelligent product recommendation system that helps you find the best products
            based on real user reviews and sentiment analysis. Our platform uses advanced AI technology to
            analyze product reviews and provide you with accurate recommendations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="bg-white rounded-xl shadow-lg p-6 transform hover:scale-[1.02] transition-all duration-300 hover:shadow-xl"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8 mb-12 transform hover:scale-[1.01] transition-transform duration-300">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">How It Works</h2>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-blue-600 font-bold">1</span>
              </div>
              <p className="text-gray-600 text-lg">Search for any product you're interested in</p>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-blue-600 font-bold">2</span>
              </div>
              <p className="text-gray-600 text-lg">Our system analyzes thousands of reviews using sentiment analysis</p>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-blue-600 font-bold">3</span>
              </div>
              <p className="text-gray-600 text-lg">Get recommendations based on real user experiences</p>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-blue-600 font-bold">4</span>
              </div>
              <p className="text-gray-600 text-lg">Compare products based on ratings, reviews, and sentiment scores</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8 transform hover:scale-[1.01] transition-transform duration-300">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">Our Mission</h2>
          <p className="text-gray-600 text-lg leading-relaxed">
            We aim to make online shopping smarter and more reliable by providing data-driven insights
            that help you make informed purchasing decisions. Our platform takes the guesswork out of
            online shopping by analyzing real user experiences and presenting them in an easy-to-understand format.
          </p>
          <div className="mt-8 flex justify-center">
            <button className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-8 py-3 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About; 