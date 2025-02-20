import React from 'react';
import { 
  DollarCircleOutlined, 
  FileTextOutlined, 
  LineChartOutlined, 
  UserOutlined, 
  LogoutOutlined 
} from '@ant-design/icons';

const LandingPage = () => {
  const financialMetrics = [
    {
      title: 'Total Revenue',
      value: '₹50,00,000',
      icon: <DollarCircleOutlined className="text-green-500" />,
      color: 'bg-green-100'
    },
    {
      title: 'Total Expenses',
      value: '₹30,00,000',
      icon: <LineChartOutlined className="text-red-500" />,
      color: 'bg-red-100'
    },
    {
      title: 'Profit/Loss',
      value: '₹20,00,000',
      icon: <LineChartOutlined className="text-blue-500" />,
      color: 'bg-blue-100'
    },
    {
      title: 'Pending Claims',
      value: '12 Claims',
      icon: <FileTextOutlined className="text-yellow-500" />,
      color: 'bg-yellow-100'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-md p-4 flex justify-between items-center">
        <div className="flex items-center">
          <img src="/logo.svg" alt="InsureTech Logo" className="h-10 mr-4" />
          <nav className="space-x-4">
            <a href="#" className="text-gray-700 hover:text-blue-600">Dashboard</a>
            <a href="#" className="text-gray-700 hover:text-blue-600">Upload Reports</a>
            <a href="#" className="text-gray-700 hover:text-blue-600">Analytics</a>
            <a href="#" className="text-gray-700 hover:text-blue-600">Settings</a>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <UserOutlined className="text-xl" />
          <span>John Doe</span>
          <LogoutOutlined className="text-red-500 cursor-pointer" />
        </div>
      </nav>

      {/* Financial Metrics */}
      <div className="container mx-auto p-6">
        <div className="grid grid-cols-4 gap-4 mb-6">
          {financialMetrics.map((metric, index) => (
            <div 
              key={index} 
              className={`p-4 rounded-lg shadow-md ${metric.color} flex items-center`}
            >
              <div className="mr-4 text-3xl">{metric.icon}</div>
              <div>
                <h3 className="text-sm text-gray-600">{metric.title}</h3>
                <p className="text-xl font-bold">{metric.value}</p>
              </div>
            </div>
          ))}
        </div>

        {/* File Upload Section */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl font-semibold mb-4">Upload Financial Reports</h2>
          <div className="flex items-center space-x-4">
            <input 
              type="file" 
              className="border p-2 rounded flex-grow" 
              placeholder="Select file" 
            />
            <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
              Upload
            </button>
          </div>

          {/* Past Reports Table */}
          <table className="w-full mt-4 border-collapse">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">Report Name</th>
                <th className="border p-2">Date</th>
                <th className="border p-2">Type</th>
                <th className="border p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border p-2">Annual Report 2023</td>
                <td className="border p-2">31 Dec 2023</td>
                <td className="border p-2">Balance Sheet</td>
                <td className="border p-2 text-center">
                  <button className="text-blue-500 hover:underline">View</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Charts & Insights */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Financial Trends</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="border p-4 rounded">
              <h3 className="text-lg mb-2">Revenue & Expense Comparison</h3>
              {/* Placeholder for chart */}
              <div className="h-64 bg-gray-200 flex items-center justify-center">
                Chart Placeholder
              </div>
            </div>
            <div className="border p-4 rounded">
              <h3 className="text-lg mb-2">Claims Processing</h3>
              {/* Placeholder for chart */}
              <div className="h-64 bg-gray-200 flex items-center justify-center">
                Chart Placeholder
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
