import React, { useState } from 'react';
import { 
  DollarCircleOutlined, 
  FileTextOutlined, 
  LineChartOutlined, 
  UserOutlined, 
  LogoutOutlined 
} from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { message } from 'antd';
import { jwtDecode } from "jwt-decode"; // Named import
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const Dashboard = () => {
  const location = useLocation();
  const { name, code } = location.state || {}; 
  console.log(name, code);
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
  const [reportType, setReportType] = useState('OTHER');
  const [year, setYear] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedData, setProcessedData] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const processDocuments = async () => {
    try {
      setIsProcessing(true);
      const token = localStorage.getItem('accessToken');
      
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/documents/process/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log("Processing result:", response.data);
      
      // Display processed data
      if (response.data.processed_documents) {
        const processedDocs = response.data.processed_documents;
        setProcessedData(processedDocs);
        message.success('Documents processed successfully');
      } else if (response.data.error) {
        message.error(`Processing failed: ${response.data.error}`);
      }
    } catch (error) {
      console.error("Error processing documents:", error);
      message.error('Failed to process documents');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileUpload = async (file, year) => {
    try {
      if (!name) {
        message.error('Organization name is required');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);
      formData.append('organization', name);
      formData.append('year', year);
      formData.append('reportType', reportType);

      // Get the token from local storage
      const token = localStorage.getItem('accessToken');
      if (token) {
        // Decode the token to get user information
        const decodedToken = jwtDecode(token);
        const username = decodedToken.username; // Assuming the username is stored in the token
        formData.append('uploaded_by', username); // Append the username
      }

      // Log the form data
      console.log('Form data contents:');
      for (let pair of formData.entries()) {
        console.log(pair[0] + ':', pair[1]);
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/v1/documents/upload/`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log('Response status:', response.status);
      const responseText = await response.text();
      console.log('Response text:', responseText);

      if (!response.ok) {
        let errorMessage;
        try {
          const errorData = JSON.parse(responseText);
          errorMessage = errorData.error || errorData.message || 'Failed to upload file';
        } catch (e) {
          errorMessage = 'Failed to upload file: ' + responseText;
        }
        throw new Error(errorMessage);
      }

      const result = JSON.parse(responseText);
      console.log('File uploaded successfully:', result);
      message.success('File uploaded successfully');

      // After successful upload, trigger document processing
      await processDocuments();

      // Clear the file input
      setFile(null);
    } catch (error) {
      console.error('Error uploading file:', error);
      message.error(error.message || 'Failed to upload file');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      await handleFileUpload(file, year);
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white p-6 rounded-lg shadow-md mb-6">
            <h2 className="text-2xl font-semibold mb-4">Upload Financial Document</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Document Type</label>
                <select
                  value={reportType}
                  onChange={(e) => setReportType(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="OTHER">Select Type</option>
                  <option value="BALANCE_SHEET">Balance Sheet</option>
                  <option value="CHARGESHEET">Charge Sheet</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Year</label>
                <input
                  type="number"
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                  placeholder="Enter year"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">File</label>
                <input
                  type="file"
                  onChange={handleFileChange}
                  className="mt-1 block w-full"
                  accept=".xlsx,.xls,.csv"
                />
              </div>
              <div className="flex justify-between items-center">
                <button
                  type="submit"
                  className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  disabled={!file || isProcessing}
                >
                  {isProcessing ? 'Processing...' : 'Upload'}
                </button>
                
                <button
                  type="button"
                  onClick={processDocuments}
                  className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  disabled={isProcessing}
                >
                  {isProcessing ? 'Processing Documents...' : 'Process Pending Documents'}
                </button>
              </div>
            </form>
          </div>

          <YearlyReportsSection />

          {/* Display Processed Data */}
          {processedData.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-md mt-6">
              <h2 className="text-2xl font-semibold mb-4">Processed Documents</h2>
              {processedData.map((doc, index) => (
                <div key={doc.document_id} className="mb-4 p-4 border rounded">
                  <h3 className="text-xl font-medium">{doc.title}</h3>
                  <p className="text-gray-600">Type: {doc.report_type}</p>
                  
                  {doc.processed_data && (
                    <div className="mt-2">
                      {doc.processed_data.type === 'balance_sheet' && (
                        <div className="grid grid-cols-2 gap-4">
                          {Object.entries(doc.processed_data.data).map(([key, value]) => (
                            <div key={key} className="p-2 bg-gray-50 rounded">
                              <span className="font-medium">{key.replace(/_/g, ' ').toUpperCase()}: </span>
                              {key === 'processed_at' ? new Date(value).toLocaleString() : value}
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {doc.processed_data.type === 'chargesheet' && (
                        <div className="overflow-x-auto">
                          <table className="min-w-full mt-2">
                            <thead>
                              <tr className="bg-gray-50">
                                <th className="px-4 py-2">Date</th>
                                <th className="px-4 py-2">Charges</th>
                                <th className="px-4 py-2">Amount</th>
                              </tr>
                            </thead>
                            <tbody>
                              {doc.processed_data.data.map((charge, idx) => (
                                <tr key={idx} className="border-t">
                                  <td className="px-4 py-2">{new Date(charge.date).toLocaleDateString()}</td>
                                  <td className="px-4 py-2">{charge.charges}</td>
                                  <td className="px-4 py-2">{charge.amount}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {doc.error && (
                    <div className="text-red-600 mt-2">
                      Error: {doc.error}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Charts & Insights */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-4">Financial Trends</h2>
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
