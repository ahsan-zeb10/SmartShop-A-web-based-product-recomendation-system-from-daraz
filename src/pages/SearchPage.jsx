import React, { useState } from 'react';
import { Input, Button, Row, Col, Card, Spin, Alert } from 'antd';
import axios from 'axios';
import { getUserUUID, recordInteractionLocally, syncInteractions } from '../utils/userTracking';

const { Meta } = Card;

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const uuid = getUserUUID();
      recordInteractionLocally({ type: 'search', query });
      await syncInteractions(axios);
      const response = await axios.get(`http://localhost:8000/api/search?query=${encodeURIComponent(query)}`);
      setProducts(response.data.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch products');
      setLoading(false);
    }
  };

  const handleProductClick = (productId) => {
    recordInteractionLocally({ type: 'click', product_id: productId });
    syncInteractions(axios);
    console.log(`Clicked product ${productId}`);
  };

  return (
    <div style={{ padding: '20px' }}>
      <Input.Search
        placeholder="Search products..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onSearch={handleSearch}
        enterButton
        style={{ marginBottom: '20px' }}
      />
      {loading && <Spin tip="Loading products..." />}
      {error && <Alert message={error} type="error" />}
      <Row gutter={[16, 16]}>
        {products.map((product) => (
          <Col xs={24} sm={12} md={8} lg={6} key={product._id}>
            <Card
              hoverable
              cover={<img alt={product.title} src={product.image_url} style={{ height: '200px', objectFit: 'cover' }} />}
              onClick={() => handleProductClick(product._id)}
            >
              <Meta
                title={product.title}
                description={`Rs. ${product.price.toFixed(2)} | ${product.stars} stars`}
              />
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default SearchPage;