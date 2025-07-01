// import React, { useState, useEffect } from 'react';
// import { Card, Spin, Typography } from 'antd';
// import axios from 'axios';
// import { getUserId, recordInteraction } from 'utils/cookieUtils';
// import { useNavigate } from 'react-router-dom';

// const { Title } = Typography;
// const API_URL = 'http://127.0.0.1:8000/api';

// const Recommendations = () => {
//   const [recommendations, setRecommendations] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchRecommendations = async () => {
//       try {
//         const userId = await getUserId();
//         const response = await axios.get(`${API_URL}/recommendations?user_id=${userId}`);
//         setRecommendations(response.data.data);
//         setLoading(false);
//       } catch (err) {
//         console.error('Failed to load recommendations:', err);
//         setLoading(false);
//       }
//     };
//     fetchRecommendations();
//   }, []);

//   const handleViewProduct = (productId) => {
//     recordInteraction('click', { product_id: productId });
//     navigate(`/product/${productId}`);
//   };

//   if (loading) return <div className="flex justify-center py-8"><Spin size="large" /></div>;
//   if (!recommendations.length) return null;

//   return (
//     <div className="w-11/12 px-4 mb-8">
//       <Title level={3} className="text-gray-800">Recommended for You</Title>
//       <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
//         {recommendations.map(product => (
//           <Card
//             key={product._id}
//             hoverable
//             cover={<img alt={product.title} src={product.image_url} className="h-40 object-contain" />}
//             onClick={() => handleViewProduct(product._id)}
//             className="border rounded-lg bg-white shadow-lg hover:shadow-xl transition"
//           >
//             <Card.Meta
//               title={<span className="text-md">{product.title.substring(0, 50)}...</span>}
//               description={
//                 <div className="flex flex-col">
//                   <p className="text-gray-700 font-bold">Rs {product.price.toFixed(2)}</p>
//                   <div className="flex items-center justify-between text-sm">
//                     <span className="text-yellow-500">
//                       ★ {product.stars || 'N/A'}/5 ({product.review_count || '0'})
//                     </span>
//                     <span className="bg-blue-500 text-white px-1 py-1 rounded-full text-xs">
//                       {(product.sentiment_score * 2).toFixed(1)}/10
//                     </span>
//                   </div>
//                 </div>
//               }
//             />
//           </Card>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default Recommendations;