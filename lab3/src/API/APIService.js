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
    static async getProducts() {
        const response = await apiClient.get("/client/v1/product/", {});
        return response;
    }
}

