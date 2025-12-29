import {
    Card,
    Typography,
    Row,
    Col,
    Image,
    Divider,
    Spin,
    Empty,
    Tag
} from 'antd';
import { useOrders } from '../hooks/UseOrders'

const { Title, Text } = Typography;

const orderStatusMap = {
    0: { text: 'Создан', color: 'default' },
    1: { text: 'В обработке', color: 'processing' },
    2: { text: 'Отправлен', color: 'blue' },
    3: { text: 'Доставлен', color: 'success' },
    4: { text: 'Отменён', color: 'error' }
};

const OrdersPage = () => {
    const { orders, loading, error } = useOrders();

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: 80 }}>
                <Spin size="large" />
            </div>
        );
    }

    if (!orders.length) {
        return (
            <div style={{ maxWidth: 800, margin: '80px auto' }}>
                <Empty description="У вас пока нет заказов" />
            </div>
        );
    }

    return (
        <div style={{ maxWidth: 1000, margin: '0 auto', padding: '32px 24px' }}>
            <Title level={2}>Мои заказы</Title>

            {orders.map(order => {
                const status = orderStatusMap[order.Status] || {
                    text: 'Неизвестно',
                    color: 'default'
                };

                return (
                    <Card key={order.ID} style={{ marginBottom: 24 }}>
                        {/* Заголовок заказа */}
                        <Row justify="space-between" align="middle">
                            <Col>
                                <Title level={5}>Заказ №{order.ID}</Title>
                                <Tag color={status.color}>{status.text}</Tag>
                            </Col>
                            <Col>
                                <Text strong>{order.TotalCost} ₽</Text>
                            </Col>
                        </Row>

                        {/* <Divider /> */}

                        {/* Товары */}
                        {/* {order.Items.map(item => (
                            <Row
                                key={item.ProductID}
                                gutter={16}
                                align="middle"
                                style={{ marginBottom: 12 }}
                            >
                                <Col span={4}>
                                    {item.ImageUrl && (
                                        <Image
                                            src={item.ImageUrl}
                                            preview={false}
                                            style={{ borderRadius: 6 }}
                                        />
                                    )}
                                </Col>

                                <Col span={14}>
                                    <Text strong>{item.Title}</Text>
                                    <br />
                                    <Text type="secondary">
                                        {item.CostPerItem} ₽ × {item.Quantity}
                                    </Text>
                                </Col>

                                <Col span={6} style={{ textAlign: 'right' }}>
                                    <Text strong>{item.TotalCost} ₽</Text>
                                </Col>
                            </Row>
                        ))}

                        <Divider /> */}

                        {/* Доставка */}
                        {/* <Text type="secondary">
                            Адрес доставки: {order.DeliveryInfo.ReceiveAddress}
                        </Text> */}
                    </Card>
                );
            })}
        </div>
    );
};

export default OrdersPage;
