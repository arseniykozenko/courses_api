import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Card,
    Typography,
    Spin,
    Empty,
    Row,
    Col,
    Descriptions,
    Divider,
    Rate,
    Button,
    Image,
    message
} from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import APIService from '../API/APIService';
import { useCart } from '../hooks/useCart';


const { Title, Text, Paragraph } = Typography;

const ProductPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { addToCart } = useCart();

    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                setLoading(true);
                const response = await APIService.getProductById(id);
                setProduct(response.data.Product);
            } catch (e) {
                setError('Не удалось загрузить товар');
            } finally {
                setLoading(false);
            }
        };

        fetchProduct();
    }, [id]);

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 80 }}>
                <Spin size="large" />
            </div>
        );
    }

    if (error || !product) {
        return <Empty description={error || 'Товар не найден'} style={{ marginTop: 80 }} />;
    }

    return (
        <div style={{ maxWidth: 1200, margin: '0 auto', padding: '32px 24px' }}>
            <Button
                type="link"
                icon={<ArrowLeftOutlined />}
                onClick={() => navigate(-1)}
                style={{ marginBottom: 24 }}
            >
                Назад
            </Button>

            <Row gutter={[32, 32]}>
                <Col xs={24} md={14}>
                    <Card>
                        {product.Images?.length > 0 && (
                            <Image.PreviewGroup>
                                <div
                                    style={{
                                        display: 'grid',
                                        gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
                                        gap: 16,
                                        marginBottom: 24
                                    }}
                                >
                                    {product.Images.map(img => (
                                        <Image
                                            key={img.ID}
                                            src={img.ImageURL}
                                            alt={product.Title}
                                            height={170}
                                            style={{
                                                borderRadius: 10,
                                                objectFit: 'cover'
                                            }}
                                        />
                                    ))}
                                </div>
                            </Image.PreviewGroup>
                        )}

                        <Title level={2}>{product.Title}</Title>

                        <Text style={{ fontSize: 24, color: '#1890ff', fontWeight: 600 }}>
                            {product.Price} ₽
                        </Text>

                        <Button
                            type="primary"
                            block
                            style={{ marginTop: 16 }}
                            onClick={ async () => { 
                                try {
                                    await addToCart(product, 1), 
                                    message.open({
                                        type: 'success',
                                        content: `${product.Title} добавлен в корзину`,
                                        duration: 2,
                                        onClick: () => navigate('/cart')
                                    })
                                } catch(e) {
                                    console.error('Ошибка при добавлении в корзину', e);
                                    message.error('Ошибка при добавлении в корзину');
                                }    
                            }}
                            
                        >
                            Добавить в корзину
                        </Button>

                        <Divider />

                        <Paragraph>{product.Desc}</Paragraph>

                        {product.Characteristics?.map(group => (
                            <div key={group.ID} style={{ marginTop: 24 }}>
                                <Title level={4}>{group.Title}</Title>

                                <Descriptions
                                    column={1}
                                    size="small"
                                    bordered
                                >
                                    {group.Characteristics.map(item => (
                                        <Descriptions.Item
                                            key={item.ID}
                                            label={item.Key}
                                        >
                                            {item.Value}
                                        </Descriptions.Item>
                                    ))}
                                </Descriptions>
                            </div>
                        ))}
                    </Card>
                </Col>

                <Col xs={24} md={10}>
                    <Card title="Отзывы">
                        {product.Reviews && product.Reviews.length > 0 ? (
                            product.Reviews.map((review, index) => (
                                <Card
                                    key={index}
                                    type="inner"
                                    style={{ marginBottom: 16 }}
                                >
                                    {review.Rating && (
                                        <Rate
                                            disabled
                                            defaultValue={review.Rating}
                                        />
                                    )}
                                    <Paragraph style={{ marginTop: 8 }}>
                                        {review.Review}
                                    </Paragraph>
                                </Card>
                            ))
                        ) : (
                            <Empty description="Отзывов пока нет" />
                        )}
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default ProductPage;
