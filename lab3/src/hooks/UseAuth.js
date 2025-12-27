// useAuth.js
import { useState } from 'react';
import APIService from '../API/APIService';

export const useAuth = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const signUp = async (email, password) => {
        setLoading(true);
        setError(null);
        try {
            await APIService.signUp(email, password);
            const response = await APIService.signUpConfirm();
            const { AccessToken } = response.data;
            localStorage.setItem('AccessToken', AccessToken);
            return AccessToken;
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.message || err.message);
        } finally {
            setLoading(false);
        }
    };

    const signIn = async (email, password) => {
        setLoading(true);
        setError(null);
        try {
            await APIService.signIn(email, password);
            const response = await APIService.signInConfirm();
            const { AccessToken } = response.data;
            localStorage.setItem('AccessToken', AccessToken);
            return AccessToken;
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.message || err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const signOut = () => {
        const response = APIService.signOut();
        localStorage.removeItem('AccessToken');
        window.location.href = '/';
        return response;
    };

    const isAuth = Boolean(localStorage.getItem('AccessToken'));

    return {
        loading,
        error,
        isAuth,
        signUp,
        signIn,
        signOut,
    };
};
