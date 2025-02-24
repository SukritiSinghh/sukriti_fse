// LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = ({ setIsAuthenticated }) => {
    const [username, setusername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        // Clear previous tokens before login
        localStorage.removeItem("accessToken"); // Remove access token
        localStorage.removeItem("refreshToken"); // Remove refresh token (if stored)

        console.log('Login attempt with username:', username);
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/auth/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
                credentials: 'include'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            localStorage.setItem('accessToken', data.access);

            // Fetch user data after successful login
            const userResponse = await fetch('http://127.0.0.1:8000/api/v1/auth/me/', {
                headers: {
                    'Authorization': `Bearer ${data.access}`,
                },
                credentials: 'include'
            });

            if (userResponse.ok) {
                const userData = await userResponse.json();
                setIsAuthenticated(true);
                console.log('User Data:', userData);

                // Check if user has an organization
                if (userData.organization) {
                    // Redirect to the dashboard with organization details
                    navigate('/dashboard', { 
                        state: { 
                            name: userData.organization.name,
                            code: userData.organization.code 
                        } 
                    });
                } else {
                    navigate('/organization-selection');
                }
            } else {
                throw new Error('Failed to fetch user data');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert(error.message || 'Login failed. Please check your credentials and try again.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-md">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        Sign in to your account
                    </h2>
                </div>
                <form className="mt-8 space-y-6" onSubmit={handleLogin}>
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div>
                            <label htmlFor="username" className="sr-only">
                                Username
                            </label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setusername(e.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">
                                Password
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Sign in
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;