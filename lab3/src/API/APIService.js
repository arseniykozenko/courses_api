import axios from "axios";

export const apiClient = axios.create({
    baseURL: "http://api.vitalmeuble.online",
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
}

