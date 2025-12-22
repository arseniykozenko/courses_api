import { Card, Typography, Space, Image, Button, message } from 'antd';
import { useCart } from '../hooks/useCart';
import { useNavigate } from 'react-router-dom';

const { Text, Title: CardTitle } = Typography;
const ProductItem = (props) => {
    const navigate = useNavigate();
    const imageUrl = props.product.Images?.[0]?.ImageURL;
    const { addToCart } = useCart();
    return (
    <>
      <Card
        hoverable
        style={{ 
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          height: '100%'
        }}
        cover={
                imageUrl ? (
                    <Image
                        src={imageUrl}
                        alt={props.product.Title}
                        preview={false}
                        height={180}
                        style={{ objectFit: 'cover' }}
                        onClick={() => navigate(`/products/${props.product.ID}`)}
                    />
                ) : (
                    <div
                        onClick={() => navigate(`/products/${props.product.ID}`)}
                        style={{
                            height: 180,
                            background: '#f5f5f5',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: '#999'
                        }}
                    >
                        Нет изображения
                    </div>
                )
            }
      >
          <Card.Meta
            onClick={() => navigate(`/products/${props.product.ID}`)}
            title={
              <CardTitle level={5} style={{ margin: 0, textWrap: 'wrap' }}>
                {props.product.Title || 'Без названия'}
              </CardTitle>
            }
            description={
              <Space orientation="vertical" size="small" style={{ width: '100%' }}>
                <Text strong style={{ color: '#52c41a' }}>
                  Цена: {props.product.Price} ₽
                </Text>
                <Text type="secondary">
                  В наличии: {props.product.Amount} шт.
                </Text>
                {props.product.ID && (
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    ID: {props.product.ID}
                  </Text>
                )}
              </Space>
            }
          />
        <Button
          type="primary"
          block
          style={{ marginTop: 12 }}
          onClick={(e) => {
              e.stopPropagation();
              addToCart(props.product);
              message.open({
                  type: 'success',
                  content: `${props.product.Title} добавлен в корзину`,
                  duration: 2,
                  onClick: () => navigate('/cart')
              });
          }}
      >
          В корзину
      </Button>
      </Card>

    </>
    )
}

export default ProductItem;