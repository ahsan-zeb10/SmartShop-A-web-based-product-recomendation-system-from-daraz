// import React, { useState, useEffect } from 'react';
// import { Card, Spin, Typography, Button } from 'antd';
// import { ShoppingOutlined } from '@ant-design/icons';
// import axios from 'axios';
// import { recordInteraction } from 'utils/cookieUtils';
// import { useParams } from 'react-router-dom';

// const { Title } = Typography;
// const API_URL = 'http://127.0.0.1:8000/api';

// const ProductDetail = () => {
//   const { productId } = useParams();
//   const [product, setProduct] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchProduct = async () => {
//       try {
//         await recordInteraction('view', { product_id: productId });
//         const response = await axios.get(`${API_URL}/products/${productId}`);
//         setProduct(response.data.data);
//         setLoading(false);
//       } catch (err) {
//         setError('Failed to load product');
//         setLoading(false);
//       }
//     };
//     fetchProduct();
//   }, [productId]);

//   if (loading) return <div className="flex justify-center py-8"><Spin size="large" /></div>;
//   if (error) return <p className="text-red-500 text-center">{error}</p>;
//   if (!product) return <p className="text-center">Product not found</p>;

//   return (
//     <div className="w-full px-4 py-8">
//       <Card
//         cover={<img alt={product.title} src={product.image_url} className="h-96 object-cover" />}
//         actions={[
//           <Button icon={<ShoppingOutlined />}>
//             <a href={product.link} target="_blank" rel="noopener noreferrer">View on Daraz</a>
//           </Button>
//         ]}
//         className="max-w-2xl mx-auto shadow-md"
//       >
//         <Card.Meta
//           title={<Title level={4}>{product.title}</Title>}
//           description={
//             <div>
//               <p className="text-gray-600 text-lg">Rs {product.price.toFixed(2)}</p>
//               <p className="text-yellow-500">{product.stars} stars ({product.review_count} reviews)</p>
//               <p className="text-gray-600 mt-2">Sentiment Score: {(product.sentiment_score * 2).toFixed(1)}/10</p>
//               {product.reviews && product.reviews.length > 0 && (
//                 <div className="mt-3">
//                   <h4 className="text-sm font-semibold text-gray-700">Recent Reviews</h4>
//                   {product.reviews.slice(0, 2).map((review, index) => (
//                     <div key={index} className="text-xs mt-2">
//                       <p className="font-medium">{review.reviewer}</p>
//                       <p className="text-gray-600">{review.review}</p>
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </div>
//           }
//         />
//       </Card>
//     </div>
//   );
// };

// export default ProductDetail;