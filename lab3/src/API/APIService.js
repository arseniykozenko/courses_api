import axios from "axios";

export const apiClient = axios.create({
    baseURL: "https://api.vitalmeuble.online",
    withCredentials: true
});

apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");

        if (token) {
            config.headers["Authorization"] = `${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default class APIService {
    static async getAllCategories() {
        const response = await apiClient.get("/client/v1/category/all");
        return response;
    }
    static async getProducts(categoryId = 20, limit = 10, offset = 0) {
        const params = new URLSearchParams();
        if (categoryId) params.append('category_id', categoryId);
        params.append('limit', limit);
        params.append('offset', offset);

        const response = await apiClient.get(`/client/v1/product/?${params.toString()}`);
        return response;
    }
    static async getProductById(productId) {
        const response = await apiClient.get(`/client/v2/product/${productId}`);
        return response;
    }
        // Получить корзину
    static async getCart() {
        return apiClient.get('/client/v1/cart/');
    }

    // Добавить товар в корзину
    static async addToCart(productId, quantity = 1) {
        return apiClient.post('/client/v1/cart/item/add', { product_id: productId, quantity: quantity });
    }

    // Увеличить количество
    static async incrementCartItem(productId, quantity = 1) {
        return apiClient.patch('/client/v1/cart/item/increase', { product_id: productId, quantity: quantity });
    }

    // Уменьшить количество
    static async decrementCartItem(productId, quantity = 1) {
        return apiClient.patch('/client/v1/cart/item/decrease', { product_id: productId, quantity: quantity }, );
    }

    // Удалить товар из корзины
    static async removeCartItem(productId, quantity = 1) {
        return apiClient.delete('/client/v1/cart/item/delete', { data: { product_id: productId, quantity: quantity } });
    }

    static async signUp(email, password) {
        return apiClient.post('/client/v1/auth/sign-up', { login: email, password }, {credentials: "include"});
    }

    static async signUpConfirm(ConfirmCode = "string", SignUpToken = "string") {
        return apiClient.post('/client/v1/auth/sign-up-confirm', { ConfirmCode: ConfirmCode, SignUpToken: SignUpToken }, {credentials: "include"});
    }

    // Авторизация
    static async signIn(email, password) {
        return apiClient.post('/client/v1/auth/sign-in', { login: email, password });
    }

    static async signInConfirm(ConfirmationCode = "string", SignInToken = "string") {
        return apiClient.post('/client/v1/auth/sign-in-confirm', { ConfirmationCode: ConfirmationCode, SignInToken: SignInToken });
    }

    static async signOut() {
        return apiClient.post('/client/v1/auth/sign-out');
    }

    static async getOrders() {
        const response = apiClient.get('/client/v1/orders/');
        return response;
    }
}

