// This file has been renamed to OrganizationSelectionPage.jsx
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

const OrganizationSelectionPage = () => {
    const [orgName, setOrgName] = useState('');
    const [orgCode, setOrgCode] = useState('');
    const history = useHistory();

    const handleCreateOrg = (e) => {
        e.preventDefault();
        // Add logic to create organization here
        history.push('/admin-dashboard'); // Redirect to admin dashboard
    };

    const handleJoinOrg = (e) => {
        e.preventDefault();
        // Add logic to join organization here
        history.push('/user-dashboard'); // Redirect to user dashboard
    };

    return (
        <div>
            <h2>Organization Selection</h2>
            <h3>Create Organization</h3>
            <form onSubmit={handleCreateOrg}>
                <input type="text" placeholder="Organization Name" value={orgName} onChange={(e) => setOrgName(e.target.value)} required />
                <input type="text" placeholder="Address" required />
                <button type="submit">Create & Proceed</button>
            </form>
            <h3>Join Organization</h3>
            <form onSubmit={handleJoinOrg}>
                <input type="text" placeholder="Organization Code" value={orgCode} onChange={(e) => setOrgCode(e.target.value)} required />
                <button type="submit">Request to Join</button>
            </form>
        </div>
    );
};

export default OrganizationSelectionPage;
