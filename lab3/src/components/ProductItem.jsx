import { Card, Button, Typography, Space, Modal } from 'antd';
import { DeleteOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';

const ProductItem = ({ product }) => {
    return (
    <>
      <Card
        hoverable
        style={{ 
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          height: '100%'
        }}
        actions={[
        //   <Button 
        //     type="text" 
        //     icon={<EditOutlined />} 
        //     size="small"
        //     onClick={(e) => {
        //       e.stopPropagation();
        //       console.log('Редактировать товар:', product.ID);
        //     }}
        //   >
        //     Редактировать
        //   </Button>,
        //   <Button 
        //     type="text" 
        //     danger 
        //     icon={<DeleteOutlined />} 
        //     size="small"
        //     onClick={(e) => {
        //       e.stopPropagation();
        //       handleDeleteClick();
        //     }}
        //   >
        //     Удалить
        //   </Button>
        ]}
      >
        <Card.Meta
          title={
            <Title level={5} style={{ margin: 0 }}>
              {product.Title || 'Без названия'}
            </Title>
          }
          description={
            <Space direction="vertical" size="small" style={{ width: '100%' }}>
              {product.Desc && (
                <Text type="secondary" style={{ display: 'block' }}>
                  {product.Desc}
                </Text>
              )}
              <Text strong style={{ color: '#52c41a' }}>
                Цена: {product.Price} ₽
              </Text>
              <Text type="secondary">
                В наличии: {product.Amount} шт.
              </Text>
              {product.ID && (
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  ID: {product.ID}
                </Text>
              )}
            </Space>
          }
        />
      </Card>
    </>
    )
}

export default ProductItem;