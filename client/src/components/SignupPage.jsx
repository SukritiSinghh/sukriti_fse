// This file has been renamed to SignupPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignupPage = ({ setIsAuthenticated }) => {
    const [username, setusername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        const payload = {
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": confirmPassword,
            // "role": null,
        };
        console.log("Payload:", JSON.stringify(payload));
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/auth/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Signup successful, received data:', data);
                
                // Store tokens and user data
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                // Set authenticated state
                setIsAuthenticated(true);
                
                // Navigate to organization setup
                navigate('/organization-selection');
            } else {
                const errorData = await response.json();
                console.error('Signup failed:', errorData);
                
                // Handle validation errors
                let errorMessage = '';
                if (typeof errorData === 'object') {
                    // Process each field's errors
                    Object.entries(errorData).forEach(([field, errors]) => {
                        if (Array.isArray(errors)) {
                            errorMessage += `${field}: ${errors.join(', ')}\n`;
                        } else if (typeof errors === 'string') {
                            errorMessage += `${field}: ${errors}\n`;
                        }
                    });
                } else {
                    errorMessage = 'Registration failed. Please try again.';
                }
                alert(errorMessage.trim());
            }
        } catch (error) {
            console.error('Network error:', error);
            alert('Network error. Please check your connection and try again.');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-2xl font-bold text-center mb-6">Sign Up</h2>
                <form onSubmit={handleSignup} className="space-y-4">
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setusername(e.target.value)}
                        placeholder="Full Name"
                        required
                        className="w-full p-2 border border-gray-300 rounded"
                    />
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
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Confirm Password"
                        required
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition">
                        Sign Up
                    </button>
                </form>
                <p className="text-center mt-4">
                    Already have an account? <a href="/login" className="text-blue-500 hover:underline">Login</a>
                </p>
            </div>
        </div>
    );
};

export default SignupPage;
