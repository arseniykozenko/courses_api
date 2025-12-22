import { Layout } from 'antd';
import { BrowserRouter } from 'react-router-dom'
import 'antd/dist/reset.css';
import './App.css'
import AppRouter from './AppRouter.jsx'
import AppHeader from './components/AppHeader.jsx';
import { CartProvider } from './context/CartProvider.jsx';

const { Content } = Layout;

function App() {  

  return (
    <CartProvider>
      <BrowserRouter>
        <Layout>
          <AppHeader />
          <Content>
            <AppRouter />
          </Content>
        </Layout>
      </BrowserRouter>
    </CartProvider>
  )
}

export default App;
