import 'antd/dist/reset.css';
import './App.css'
import { Button, Card, Col, Row, Typography, Spin, Empty, Space } from 'antd';
import { useState, useEffect } from 'react';
import APIService from './API/APIService';
import { useFetching } from './hooks/useFetching';
import ProductItem from './components/ProductItem';

const { Text, Title } = Typography;
function App() {
  const [products, setProducts] = useState([])
  const [fetchProducts, isLoading, error] = useFetching(async () => {
      const response = await APIService.getProducts()
      console.log(response)
      setProducts(response.data)
  })
  useEffect(() => {
      fetchProducts()
  },[])

  if (error) {
        return (
            <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
                <Card>
                    <Empty
                        description="Произошла ошибка при загрузке данных"
                        image={Empty.PRESENTED_IMAGE_SIMPLE}
                    />
                    <Button 
                        type="primary" 
                        onClick={fetchProducts}
                        style={{ marginTop: '16px' }}
                    >
                        Повторить попытку
                    </Button>
                </Card>
            </div>
        );
    }

  return (
    <>
     <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            marginBottom: '24px' 
        }}>
            <Title level={2} style={{ margin: 0, color: '#0b0d10ff', marginRight: '16px' }}>
                Товары
            </Title>
            {/* <Button 
                type="primary" 
                icon={<PlusOutlined />} 
                onClick={openModal}
                size="large"
            >
                Добавить товар
            </Button> */}
        </div>

        {isLoading ? (
            <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '200px' 
            }}>
                <Spin size="large" />
            </div>
        ) : products.length > 0 ? (
            <Row gutter={[16, 16]}>
                {products.map(product => (
                    <Col xs={24} sm={12} md={8} lg={6} key={product.ID}>
                      <ProductItem product={product} />
                    </Col>
                ))}
            </Row>
        ) : (
            <div style={{ padding: '48px 0' }}>
                <Empty
                    description="Нет товаров"
                    image={Empty.PRESENTED_IMAGE_SIMPLE}
                />
            </div>
        )}
    </div>
    </>
  )
}

export default App
