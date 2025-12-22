import Products from "../components/Products"
import ProductPage from "../components/ProductPage"
import CartPage from "../components/CartPage"

export const appRoutes = [
    {path: '/', component: Products},
    {path: '/products', component: Products},
    {path: '/products/:id', component: ProductPage},
    {path: '/cart', component: CartPage}
]