import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = ({ setIsAuthenticated }) => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/auth/users/logout/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                },
                credentials: 'include'
            });

            if (response.ok) {
                // Clear local storage
                localStorage.removeItem('accessToken');
                // Update authentication state
                setIsAuthenticated(false);
                // Redirect to login page
                navigate('/login');
            } else {
                console.error('Logout failed');
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };

    return (
        <button 
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        >
            Logout
        </button>
    );
};

export default LogoutButton;
