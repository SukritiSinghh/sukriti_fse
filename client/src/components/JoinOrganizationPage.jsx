import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const JoinOrganizationPage = () => {
    const [orgCode, setOrgCode] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleJoinOrg = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await axios.post('/api/organizations/join_organization/', {
                code: orgCode
            }, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    'Content-Type': 'application/json'
                }
            });

            // Update local storage with new organization and role info
            const userData = JSON.parse(localStorage.getItem('user') || '{}');
            userData.organization = response.data.organization_name;
            userData.role = response.data.role;
            localStorage.setItem('user', JSON.stringify(userData));

            // Show success message and redirect
            alert('Successfully joined organization as Admin!');
            navigate('/dashboard');

        } catch (error) {
            console.error('Error joining organization:', error);
            setError(
                error.response?.data?.error ||
                error.response?.data?.message ||
                'Failed to join organization. Please try again.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-3xl font-bold text-center mb-6 text-green-500">Join Organization</h2>
                
                {error && (
                    <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
                        {error}
                    </div>
                )}

                <form onSubmit={handleJoinOrg} className="space-y-4">
                    <div>
                        <label htmlFor="orgCode" className="block text-sm font-medium text-gray-700 mb-1">
                            Organization Code
                        </label>
                        <input 
                            id="orgCode"
                            type="text" 
                            placeholder="Enter the organization code" 
                            value={orgCode} 
                            onChange={(e) => setOrgCode(e.target.value)} 
                            required 
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500"
                            disabled={loading}
                        />
                    </div>

                    <button 
                        type="submit" 
                        className={`w-full p-2 rounded transition duration-300 ease-in-out ${
                            loading 
                                ? 'bg-gray-400 cursor-not-allowed' 
                                : 'bg-green-500 hover:bg-green-600 text-white'
                        }`}
                        disabled={loading}
                    >
                        {loading ? 'Joining...' : 'Join Organization'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default JoinOrganizationPage;
