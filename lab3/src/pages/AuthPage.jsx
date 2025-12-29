// AuthPage.jsx
import { useNavigate } from 'react-router-dom';
import {
    Tabs,
    Form,
    Input,
    Button,
    Modal,
    Typography,
    message,
    Spin
} from 'antd';
import { useAuth } from '../hooks/UseAuth';

const { TabPane } = Tabs;
const { Title } = Typography;


const AuthPage = () => {
    const navigate = useNavigate();
    const {
        loading,
        error,
        signUp,
        signIn
    } = useAuth();

    const [signUpForm] = Form.useForm();
    const [loginForm] = Form.useForm();

    const handleSignUp = async (values) => {
        try {
            await signUp(values.email, values.password);
            message.success('Регистрация прошла, подтвердите аккаунт');
            navigate('/');
        } catch (err) {
            message.error(err.message || 'Ошибка регистрации');
        }
    };


    const handleLogin = async (values) => {
        try {
            const token = await signIn(values.email, values.password);
            message.success('Вход выполнен!');
            console.log('AccessToken:', token);
            navigate('/');
        } catch (err) {
            message.error(err.message || 'Ошибка входа');
        }
    };

    return (
        <div style={{ maxWidth: 400, margin: '80px auto', padding: 24 }}>
            <Title level={2} style={{ textAlign: 'center', marginBottom: 32 }}>
                Войти / Регистрация
            </Title>

            <Tabs defaultActiveKey="login">
                <TabPane tab="Вход" key="login">
                    <Form form={loginForm} layout="vertical" onFinish={handleLogin}>
                        <Form.Item
                            label="Email"
                            name="email"
                            rules={[{ required: true, message: 'Введите email' }]}
                        >
                            <Input type="email" />
                        </Form.Item>

                        <Form.Item
                            label="Пароль"
                            name="password"
                            rules={[{ required: true, message: 'Введите пароль' }]}
                        >
                            <Input.Password />
                        </Form.Item>

                        <Form.Item>
                            <Button type="primary" htmlType="submit" block loading={loading}>
                                Войти
                            </Button>
                        </Form.Item>
                    </Form>
                </TabPane>

                <TabPane tab="Регистрация" key="signup">
                    <Form form={signUpForm} layout="vertical" onFinish={handleSignUp}>
                        <Form.Item
                            label="Email"
                            name="email"
                            rules={[{ required: true, message: 'Введите email' }]}
                        >
                            <Input type="email" />
                        </Form.Item>

                        <Form.Item
                            label="Пароль"
                            name="password"
                            rules={[{ required: true, message: 'Введите пароль' }]}
                        >
                            <Input.Password />
                        </Form.Item>

                        <Form.Item>
                            <Button type="primary" htmlType="submit" block loading={loading}>
                                Зарегистрироваться
                            </Button>
                        </Form.Item>
                    </Form>
                </TabPane>
            </Tabs>

        </div>
    );
};

export default AuthPage;
