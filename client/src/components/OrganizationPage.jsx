import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const OrganizationPage = () => {
  const [organizationName, setOrganizationName] = useState('');
  const [organizationCode, setOrganizationCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const createOrganization = async () => {
    try {
      const response = await axios.post('/api/organizations/', {
        name: organizationName,
        address: ''
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create organization');
    }
  };

  const joinOrganization = async () => {
    try {
      const response = await axios.post(`/api/organizations/${organizationCode}/join/`, {
        code: organizationCode
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      // Navigate to the OrganizationSelectionLandingPage after joining
      navigate('/organization-selection');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to join organization');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Create New Organization</h2>
          <input
            type="text"
            placeholder="Organization Name"
            value={organizationName}
            onChange={(e) => setOrganizationName(e.target.value)}
            className="w-full p-2 border rounded mb-4"
          />
          <button 
            onClick={createOrganization}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Create
          </button>
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Join Existing Organization</h2>
          <input
            type="text"
            placeholder="Organization Code"
            value={organizationCode}
            onChange={(e) => setOrganizationCode(e.target.value)}
            className="w-full p-2 border rounded mb-4"
          />
          <button 
            onClick={joinOrganization}
            className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
          >
            Join
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default OrganizationPage;
