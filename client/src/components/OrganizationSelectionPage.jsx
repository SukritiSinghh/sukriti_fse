// This file has been renamed to OrganizationSelectionPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const OrganizationSelectionPage = () => {
    const [orgName, setOrgName] = useState('');
    const [orgCode, setOrgCode] = useState('');
    const navigate = useNavigate();

    const handleCreateOrg = (e) => {
        e.preventDefault();
        // Add logic to create organization here
        navigate('/admin-dashboard'); // Redirect to admin dashboard
    };

    const handleJoinOrg = (e) => {
        e.preventDefault();
        // Add logic to join organization here
        navigate('/user-dashboard'); // Redirect to user dashboard
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-3xl font-bold text-center mb-6 text-blue-500">Organization Selection</h2>
                
                <div className="mb-8">
                    <h3 className="text-2xl font-semibold mb-4 text-green-500">Create Organization</h3>
                    <form onSubmit={handleCreateOrg} className="space-y-4">
                        <input 
                            type="text" 
                            placeholder="Organization Name" 
                            value={orgName} 
                            onChange={(e) => setOrgName(e.target.value)} 
                            required 
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <input 
                            type="text" 
                            placeholder="Address" 
                            required 
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <button 
                            type="submit" 
                            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-300 ease-in-out"
                        >
                            Create & Proceed
                        </button>
                    </form>
                </div>

                <div>
                    <h3 className="text-2xl font-semibold mb-4 text-green-500">Join Organization</h3>
                    <form onSubmit={handleJoinOrg} className="space-y-4">
                        <input 
                            type="text" 
                            placeholder="Organization Code" 
                            value={orgCode} 
                            onChange={(e) => setOrgCode(e.target.value)} 
                            required 
                            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500"
                        />
                        <button 
                            type="submit" 
                            className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600 transition duration-300 ease-in-out"
                        >
                            Request to Join
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default OrganizationSelectionPage;
