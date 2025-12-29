import Products from "../pages/Products"
import ProductPage from "../pages/ProductPage"
import CartPage from "../pages/CartPage"
import AuthPage from "../pages/AuthPage"
import OrdersPage from "../pages/OrdersPage"

export const appRoutes = [
    {path: '/', component: Products},
    {path: '/products', component: Products},
    {path: '/products/:id', component: ProductPage},
    {path: '/cart', component: CartPage},
    {path: '/auth', component: AuthPage},
]

export const privateRoutes = [
    {path: '/orders', component: OrdersPage},
]