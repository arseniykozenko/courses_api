import { useEffect, useState } from 'react';
import APIService from '../API/APIService';

export const useOrders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchOrders = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await APIService.getOrders();
            setOrders(response.data.Orders || []);
        } catch (e) {
            console.error('Ошибка при загрузке заказов', e);
            setError(e.response?.data?.message || e.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOrders();
    }, []);

    return { orders, loading, error };
};
