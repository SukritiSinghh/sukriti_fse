import React, { useState } from 'react';
import { 
  DollarCircleOutlined, 
  FileTextOutlined, 
  LineChartOutlined, 
  UserOutlined, 
  LogoutOutlined 
} from '@ant-design/icons';

const Dashboard = () => {
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

  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [reportType, setReportType] = useState('OTHER');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('description', description);
    formData.append('report_type', reportType);
    formData.append('year', new Date().getFullYear());

    try {
      // Debug token handling
      console.log('==== TOKEN DEBUG ====');
      const token = localStorage.getItem('accessToken');
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      
      console.log('Raw token from localStorage:', token);
      console.log('User info:', user);
      console.log('Token length:', token ? token.length : 0);
      
      // Check if token exists and is valid
      if (!token || token === 'null' || token === 'undefined') {
        throw new Error('No valid authentication token found');
      }

      // Always add Bearer prefix
      const finalToken = `Bearer ${token}`;
      console.log('Final token being sent:', finalToken);
      console.log('===================');
      
      // Add user info to form data
      formData.append('user_id', user.id);

      // Log the complete request details
      console.log('Request details:', {
        url: 'http://localhost:8000/api/finance/reports/',
        method: 'POST',
        headers: {
          'Authorization': finalToken
        }
      });

      console.log('FormData contents:');
      for (let pair of formData.entries()) {
        console.log(pair[0] + ':', pair[1]);
      }

      const response = await fetch('http://localhost:8000/api/finance/reports/', {
        method: 'POST',
        headers: {
          'Authorization': finalToken,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        console.error('Server response:', {
          status: response.status,
          statusText: response.statusText,
          errorData
        });
        throw new Error(`File upload failed: ${errorData?.detail || response.statusText}`);
      }

      const data = await response.json();
      console.log('File uploaded successfully:', data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const YearlyReportsSection = () => {
    const [selectedYear, setSelectedYear] = useState(null);

    const yearlyReports = [
      {
        year: 2023,
        reports: [
          { 
            name: "Annual Report 2023", 
            date: "31 Dec 2023", 
            type: "Balance Sheet",
            description: "Comprehensive financial overview for the year 2023"
          },
          { 
            name: "Q3 Report 2023", 
            date: "30 Sep 2023", 
            type: "Quarterly Report",
            description: "Third quarter financial performance analysis"
          }
        ]
      },
      {
        year: 2022,
        reports: [
          { 
            name: "Annual Report 2022", 
            date: "31 Dec 2022", 
            type: "Annual Financial Statement",
            description: "Detailed financial report for the year 2022"
          }
        ]
      }
    ];

    const ReportsModal = ({ year, reports, onClose }) => (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div className="bg-white rounded-lg shadow-xl w-11/12 max-w-2xl max-h-[80vh] overflow-auto">
          {/* Modal Header */}
          <div className="flex justify-between items-center p-4 border-b">
            <h2 className="text-2xl font-bold">{year} Reports</h2>
            <button 
              onClick={onClose} 
              className="text-gray-600 hover:text-gray-900"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Modal Content */}
          <div className="p-4">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="p-2 text-left">Report Name</th>
                  <th className="p-2 text-left">Date</th>
                  <th className="p-2 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((report, index) => (
                  <tr key={index} className="hover:bg-gray-50 transition-colors">
                    <td className="border-b p-2">
                      <div className="font-medium">{report.name}</div>
                      <div className="text-xs text-gray-500">{report.description}</div>
                    </td>
                    <td className="border-b p-2">{report.date}</td>
                    <td className="border-b p-2 text-center">
                      <button className="text-blue-500 hover:underline px-2 py-1 rounded hover:bg-blue-50">
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );

    return (
      <div className="mt-6">
        <h2 className="text-2xl font-bold mb-4">Yearly Reports</h2>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {yearlyReports.map((yearReport) => (
            <div 
              key={yearReport.year} 
              className="border rounded-lg p-4 cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => setSelectedYear(yearReport)}
            >
              <div className="flex justify-between items-center">
                <span className="text-lg font-semibold">{yearReport.year}</span>
                <span className="text-sm text-gray-600 bg-gray-100 px-2 rounded-full">
                  {yearReport.reports.length} Reports
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Modal for Selected Year */}
        {selectedYear && (
          <ReportsModal 
            year={selectedYear.year} 
            reports={selectedYear.reports} 
            onClose={() => setSelectedYear(null)} 
          />
        )}
      </div>
    );
  };

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
          <form onSubmit={handleSubmit}>
            <div className="flex items-center space-x-4">
              <input 
                type="file" 
                onChange={handleFileChange} 
                className="border p-2 rounded flex-grow" 
                placeholder="Select file" 
                required
              />
              <input 
                type="text" 
                value={title} 
                onChange={(e) => setTitle(e.target.value)} 
                placeholder="Title" 
                className="border p-2 rounded flex-grow" 
                required
              />
              <textarea 
                value={description} 
                onChange={(e) => setDescription(e.target.value)} 
                placeholder="Description" 
                className="border p-2 rounded flex-grow" 
                required
              />
              <select 
                value={reportType} 
                onChange={(e) => setReportType(e.target.value)} 
                className="border p-2 rounded flex-grow"
              >
                <option value="OTHER">Other</option>
                <option value="INCOME">Income Report</option>
                <option value="EXPENSE">Expense Report</option>
                <option value="BUDGET">Budget Plan</option>
                <option value="TAX">Tax Document</option>
              </select>
              <button 
                type="submit" 
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Upload
              </button>
            </div>
          </form>

          <YearlyReportsSection />

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
    </div>
  );
};

export default Dashboard;
