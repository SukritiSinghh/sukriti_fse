// This file has been renamed to UserDashboard.jsx
import React from 'react';

const UserDashboard = () => {
    return (
        <div>
            <h2>User Dashboard</h2>
            <section>
                <h3>Assigned Role & Organization Details</h3>
                {/* Display User Role and Organization */}
            </section>
            <section>
                <h3>Upload/View Financial Data</h3>
                {/* Upload/View functionality based on role */}
            </section>
            <section>
                <h3>Insights & Reports</h3>
                {/* Read-Only Insights */}
            </section>
        </div>
    );
};

export default UserDashboard;
