import {
    Card,
    Typography,
    Row,
    Col,
    Button,
    Empty,
    Image,
    Divider,
    Spin
} from 'antd';
import {
    PlusOutlined,
    MinusOutlined,
    DeleteOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../hooks/useCart';

const { Title, Text } = Typography;

const CartPage = () => {
    const navigate = useNavigate();
    const {
        items,
        totalCost,
        incrementItem,
        decrementItem,
        removeItem
    } = useCart();

    if (!items || items.length === 0) {
        return (
            <div style={{ maxWidth: 800, margin: '80px auto' }}>
                <Empty description="Корзина пуста">
                    <Button type="primary" onClick={() => navigate('/')}>
                        Перейти к товарам
                    </Button>
                </Empty>
            </div>
        );
    }

    return (
        <div style={{ maxWidth: 1000, margin: '0 auto', padding: '32px 24px' }}>
            <Title level={2}>Корзина</Title>

            <Row gutter={[16, 16]}>
                <Col xs={24} md={16}>
                    {items.map(item => (
                        <Card key={item.EntityID} style={{ marginBottom: 16 }}>
                            <Row gutter={16} align="middle">
                                <Col span={6}>
                                    {item.ImageUrl && (
                                        <Image
                                            src={item.ImageUrl}
                                            alt={item.Title}
                                            preview={false}
                                            style={{ borderRadius: 8 }}
                                        />
                                    )}
                                </Col>

                                <Col span={10}>
                                    <Title level={5}>{item.Title}</Title>
                                    <Text type="secondary">{item.CostPerItem} ₽</Text>
                                </Col>

                                <Col span={5}>
                                    <div
                                        style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: 8
                                        }}
                                    >
                                        <Button
                                            icon={<MinusOutlined />}
                                            onClick={() => {decrementItem(item, 1)}}
                                        />
                                        <Text>{item.Quantity}</Text>
                                        <Button
                                            icon={<PlusOutlined />}
                                            onClick={() => {incrementItem(item, 1)}}
                                        />
                                    </div>
                                </Col>

                                <Col span={3}>
                                    <Button
                                        danger
                                        icon={<DeleteOutlined />}
                                        onClick={() => removeItem(item, item.Quantity)}
                                    />
                                </Col>
                            </Row>
                        </Card>
                    ))}
                </Col>

                <Col xs={24} md={8}>
                    <Card>
                        <Title level={4}>Итого</Title>

                        <Divider />

                        <Text strong style={{ fontSize: 18 }}>
                            {totalCost} ₽
                        </Text>

                        <Divider />

                        <Button
                            type="primary"
                            block
                            size="large"
                            style={{ marginBottom: 12 }}
                        >
                            Оформить заказ
                        </Button>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default CartPage;
