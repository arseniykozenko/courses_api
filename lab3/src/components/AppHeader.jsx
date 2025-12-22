import { Layout, Menu, Badge, Button, Dropdown, Space, Typography } from 'antd';
import {
    ShoppingCartOutlined,
    OrderedListOutlined,
    UserOutlined,
    LoginOutlined,
    LogoutOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../hooks/useCart';

const { Header } = Layout;
const { Text } = Typography;

const AppHeader = () => {
    const navigate = useNavigate();
    const { totalCount } = useCart();

    const isAuth = false;

    const userMenuItems = [
        {
            key: 'orders',
            icon: <OrderedListOutlined />,
            label: 'Мои заказы',
            onClick: () => navigate('/orders')
        },
        {
            key: 'logout',
            icon: <LogoutOutlined />,
            label: 'Выйти',
            danger: true,
            onClick: () => console.log('logout')
        }
    ];

    return (
        <Header
            style={{
                background: '#fff',
                padding: '0 24px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
                position: 'sticky',
                top: 0,
                zIndex: 100
            }}
        >
            {/* ЛОГО */}
            <Text
                strong
                style={{ fontSize: 20, cursor: 'pointer' }}
                onClick={() => navigate('/')}
            >
                Vital Tech
            </Text>

            {/* ПРАВАЯ ЧАСТЬ */}
            <Space size="large">
                {/* Корзина */}
                <Badge count={totalCount} showZero>
                    <ShoppingCartOutlined
                        style={{ fontSize: 22, cursor: 'pointer' }}
                        onClick={() => navigate('/cart')}
                    />
                </Badge>

                {/* Заказы */}
                <OrderedListOutlined
                    style={{ fontSize: 22, cursor: 'pointer' }}
                    onClick={() => navigate('/orders')}
                />

                {/* Авторизация */}
                {isAuth ? (
                    <Dropdown
                        menu={{ items: userMenuItems }}
                        placement="bottomRight"
                    >
                        <UserOutlined
                            style={{ fontSize: 22, cursor: 'pointer' }}
                        />
                    </Dropdown>
                ) : (
                    <Button
                        type="primary"
                        icon={<LoginOutlined />}
                        onClick={() => navigate('/login')}
                    >
                        Войти
                    </Button>
                )}
            </Space>
        </Header>
    );
};

export default AppHeader;
