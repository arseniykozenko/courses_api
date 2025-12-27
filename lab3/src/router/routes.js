import Products from "../components/Products"
import ProductPage from "../components/ProductPage"
import CartPage from "../components/CartPage"
import AuthPage from "../components/AuthPage"

export const appRoutes = [
    {path: '/', component: Products},
    {path: '/products', component: Products},
    {path: '/products/:id', component: ProductPage},
    {path: '/cart', component: CartPage},
    {path: '/auth', component: AuthPage},
]