import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const OrganizationSelectionLandingPage = () => {
    const navigate = useNavigate();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isJoining, setIsJoining] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const openModal = (isJoin) => {
        setIsJoining(isJoin);
        setIsModalOpen(true);
        setError(null);
        setSuccess(null);
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setSuccess(null);

        const token = localStorage.getItem('accessToken');
        if (!token) {
            setError('Please login first. No authentication token found.');
            setIsLoading(false);
            navigate('/login');
            return;
        }

        // Log the token for debugging
        console.log('Using token:', token);

        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            let response;
            if (isJoining) {
                // Join existing organization
                response = await fetch('http://localhost:8000/api/v1/org/organizations/join_organization/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    credentials: 'include',
                    body: JSON.stringify({ code: data.code }),
                });
            } else {
                // Create new organization
                response = await fetch('http://localhost:8000/api/v1/org/organizations/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        name: data.name,
                        code: data.code,
                    }),
                });
            }

            if (!response.ok) {
                const result = await response.json();
                throw new Error(result.error || result.message || `HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();

            setSuccess(isJoining ? 'Organization joined successfully! Redirecting...' : 'Organization created successfully! Redirecting...');
            setTimeout(() => navigate('/dashboard', { state: { name: data.name, code: data.code } }), 2000);

        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-2xl w-96 text-center">
                <h2 className="text-3xl font-bold mb-6 text-blue-600">Get Started with Your Organization</h2>
                <div className="flex flex-col md:flex-row gap-4">
                    <button 
                        onClick={() => openModal(false)} 
                        className="flex-1 bg-blue-600 text-white p-6 rounded-lg hover:bg-blue-700 transition duration-300 transform hover:scale-105 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                        aria-label="Create Organization"
                    >
                        🏢 Create Organization
                    </button>
                    <button 
                        onClick={() => openModal(true)} 
                        className="flex-1 bg-green-600 text-white p-6 rounded-lg hover:bg-green-700 transition duration-300 transform hover:scale-105 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                        aria-label="Join Organization"
                    >
                        🔑 Join Organization
                    </button>
                </div>
            </div>

            {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300">
                    <div className="bg-white p-6 rounded-lg shadow-2xl w-96 relative">
                        <button 
                            onClick={closeModal} 
                            className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 focus:outline-none"
                            aria-label="Close Modal"
                        >
                            ❌
                        </button>
                        <h3 className="text-2xl font-bold mb-4">{isJoining ? 'Join Existing Organization' : 'Create New Organization'}</h3>
                        {error && <p className="text-red-500 mb-4">{error}</p>}
                        {success && <p className="text-green-500 mb-4">{success}</p>}
                        <form onSubmit={handleSubmit}>
                            {isJoining ? (
                                <input 
                                    type="text" 
                                    name="code"
                                    placeholder="Enter Organization Code" 
                                    required 
                                    className="w-full p-2 border border-gray-300 rounded mb-4 focus:ring-2 focus:ring-green-500"
                                    aria-label="Organization Code"
                                />
                            ) : (
                                <> 
                                    <input 
                                        type="text" 
                                        name="name"
                                        placeholder="Organization Name" 
                                        required 
                                        className="w-full p-2 border border-gray-300 rounded mb-4 focus:ring-2 focus:ring-blue-500"
                                        aria-label="Organization Name"
                                    />
                                    <input 
                                        type="text" 
                                        name="code"
                                        placeholder="Organization Code" 
                                        required 
                                        className="w-full p-2 border border-gray-300 rounded mb-4 focus:ring-2 focus:ring-blue-500"
                                        aria-label="Organization Code"
                                    />
                                </>
                            )}
                            <button 
                                type="submit" 
                                disabled={isLoading}
                                className={`w-full ${isJoining ? 'bg-green-600 hover:bg-green-700' : 'bg-blue-600 hover:bg-blue-700'} text-white p-2 rounded transition duration-300 ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 hover:shadow-lg'}`}
                                aria-label={isJoining ? 'Join Organization' : 'Create Organization'}
                            >
                                {isLoading ? 'Processing...' : (isJoining ? 'Join Organization' : 'Create Organization')}
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default OrganizationSelectionLandingPage;
