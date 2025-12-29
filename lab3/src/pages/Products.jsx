import { Button, Card, Col, Row, Typography, Spin, Empty, Tabs, Pagination } from 'antd';
import { useState, useEffect } from 'react';
import APIService from '../API/APIService';
import { useFetching } from '../hooks/useFetching';
import ProductItem from '../components/ProductItem';

const { Text, Title } = Typography;

const Products = () => {
    const [products, setProducts] = useState([])
    const [activeCategory, setActiveCategory] = useState(null);
    const [categories, setCategories] = useState([]);
    const [limit, setLimit] = useState(10);
    const [offset, setOffset] = useState(0);
    const [allProductsLength, setAllProductsLength] = useState(0);
    const [fetchCategories] = useFetching(async () => {
        const response = await APIService.getAllCategories()
        console.log(response.data.Categories)
        setCategories(response.data.Categories)
    })
    const [fetchProducts, isLoading, error] = useFetching(async (categoryId = 20, limitParam = limit, offsetParam = offset) => {
        const response = await APIService.getProducts(categoryId, limitParam, offsetParam)
        console.log(response.data.Products)
        setProducts(response.data.Products)
    })
        const [fetchTotalProducts] = useFetching(async (categoryId = 20) => {
        const response = await APIService.getProducts(categoryId, 10000, 0);
        setAllProductsLength(response.data.Products.length);
    });


    useEffect(() => {
        fetchCategories()
        fetchProducts(activeCategory ?? 20, limit, offset)
        fetchTotalProducts(activeCategory ?? 20);
    }, [])

    const onTabChange = (key) => {
        const categoryId = key === 'all' ? null : Number(key);
        setActiveCategory(categoryId);
        setOffset(0);
        fetchProducts(categoryId, limit, 0);
        fetchTotalProducts(categoryId);
    };

    const onPageChange = (page, pageSize) => {
        const newOffset = (page - 1) * pageSize;
        setOffset(newOffset);
        setLimit(pageSize);
        fetchProducts(activeCategory ?? 20, pageSize, newOffset);
    };
    const tabItems = categories.map(cat => ({
        key: cat.ID ?? 'all',
        label: cat.Name,
    }));


    if (error) {
        return (
            <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
                <Card>
                    <Empty description="Произошла ошибка при загрузке данных" image={Empty.PRESENTED_IMAGE_SIMPLE} />
                    <Button type="primary" onClick={() => fetchProducts(activeCategory ?? 20, limit, offset)} style={{ marginTop: 16 }}>
                        Повторить попытку
                    </Button>
                </Card>
            </div>
        );
    }
    return(
        <>
            <div style={{ padding: '32px 24px', maxWidth: '1400px', margin: '0 auto', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '24px',
                    flexDirection: 'column'
                }}>
                    <Title level={1} style={{ textAlign: 'center', marginBottom: 32, color: '#1a1a1a' }}>
                        Товары
                    </Title>
                    <Tabs
                        items={tabItems}
                        onChange={onTabChange}
                        defaultActiveKey="all"
                        tabBarGutter={24}
                        size="large"
                        style={{ marginBottom: 40 }}
                        tabBarStyle={{ justifyContent: 'center' }}
                    />    
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
                ) : ( 
                <>
                    <Row gutter={[16, 16]}>
                        {products.map((product) => (
                            <Col xs={24} sm={12} md={8} lg={6} key={product.ID}>
                                <ProductItem product={product} />
                            </Col>
                        ))}
                    </Row>
                    <div style={{ marginTop: 32, display: 'flex', justifyContent: 'center' }}>
                        <Pagination
                            current={Math.floor(offset / limit) + 1}
                            pageSize={limit}
                            total={allProductsLength}
                            onChange={onPageChange}
                            showSizeChanger
                            pageSizeOptions={[1, 2, 3, 4, 5, 10]}
                        />
                    </div>
                </>
                )}
                {products.length === 0 && !isLoading && !error && (
                    <div style={{ 
                        display: 'flex', 
                        justifyContent: 'center', 
                        alignItems: 'center', 
                        height: '200px' 
                    }}>
                        <Empty description="Нет товаров" />
                    </div>
                )
               }
            </div>
        </>
    )
}

export default Products;