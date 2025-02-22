// This file has been renamed to LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        // Add authentication logic here
        const userRole = 'admin'; // This should come from your authentication logic
        if (userRole === 'admin') {
            navigate('/admin-dashboard');
        } else {
            navigate('/user-dashboard');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-2xl font-bold text-center mb-6">Login</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition">
                        Login
                    </button>
                </form>
                <p className="text-center mt-4">
                    <a href="#" className="text-blue-500 hover:underline">Forgot Password?</a>
                </p>
                <p className="text-center mt-2">
                    Don't have an account? <a href="/signup" className="text-blue-500 hover:underline">Sign Up</a>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
