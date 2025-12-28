import { useState, useEffect } from 'react';
import { CartContext } from './CartContext';
import APIService from '../API/APIService';

export const CartProvider = ({ children }) => {
    const [items, setItems] = useState([]);
    const [totalCost, setTotalCost] = useState(0);
    const [loading, setLoading] = useState(false);
    const totalCount = items.reduce(
        (sum, item) => sum + (item.Quantity || 0),
        0
    );

    const fetchCart = async () => {
        setLoading(true);
        try {
            const response = await APIService.getCart();
            setItems(response.data?.Cart?.Items ?? []);
            setTotalCost(response.data?.TotalCost ?? 0);
        } catch (e) {
            console.error('Ошибка при загрузке корзины', e);
            setItems([]);
            setTotalCost(0);
        } finally {
            setLoading(false);
        }
    };

    const addToCart = async (productId, quantity = 1) => {
        await APIService.addToCart(productId, quantity);
        await fetchCart();
    };

    const incrementItem = async (productId, quantity = 1) => {
        await APIService.incrementCartItem(productId, quantity);
        await fetchCart();
    };

    const decrementItem = async (productId, quantity = 1) => {
        console.log('PATCH /decrease payload', { product_id: productId, quantity });
        try {
            await APIService.decrementCartItem(productId, quantity);
        } catch (e) {
            console.error('DECREMENT ERROR', e.response?.data || e.message);
        }
        await fetchCart();
    };

    const removeItem = async (productId, quantity) => {
        try {
            await APIService.removeCartItem(productId, quantity);
        } catch (e) {
            console.error('REMOVE ERROR', e.response?.data || e.message);
        }
        await fetchCart();
    };

    useEffect(() => {
        fetchCart(); 
    }, []);

    return (
        <CartContext.Provider value={{ items, totalCost, totalCount, loading, addToCart, incrementItem, decrementItem, removeItem }}>
            {children}
        </CartContext.Provider>
    );
};