import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Layout, 
  Menu, 
  Card, 
  Upload, 
  message, 
  Select, 
  Form, 
  Input, 
  Button,
  Statistic,
  Table,
  Modal,
  Spin,
  Avatar,
  Dropdown
} from 'antd';
import {
  UploadOutlined,
  DashboardOutlined,
  BarChartOutlined,
  SettingOutlined,
  LogoutOutlined,
  UserOutlined,
  FileTextOutlined,
  PieChartOutlined,
  DollarOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import { API_BASE_URL } from '../config';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const { Header, Sider, Content } = Layout;
const { Option } = Select;

const Dashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [file, setFile] = useState(null);
  const [reportType, setReportType] = useState('BALANCE_SHEET');
  const [year, setYear] = useState(new Date().getFullYear());
  const [loading, setLoading] = useState(false);
  const [financialMetrics, setFinancialMetrics] = useState({
    totalRevenue: 0,
    totalExpenses: 0,
    profitLoss: 0,
    pendingClaims: 0
  });
  const [yearlyReports, setYearlyReports] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [reportsModalVisible, setReportsModalVisible] = useState(false);
  const [processedDocuments, setProcessedDocuments] = useState([]);
  const [username, setUsername] = useState('');
  const [organization, setOrganization] = useState('');
  const [aiInsights, setAiInsights] = useState({
    riskScore: null,
    recommendations: [],
    trends: {},
    predictedMetrics: {}
  });

  // Mock data for charts
  const revenueData = [
    { month: 'Jan', revenue: 4000, expenses: 2400 },
    { month: 'Feb', revenue: 3000, expenses: 1398 },
    { month: 'Mar', revenue: 2000, expenses: 9800 },
    { month: 'Apr', revenue: 2780, expenses: 3908 },
    { month: 'May', revenue: 1890, expenses: 4800 },
    { month: 'Jun', revenue: 2390, expenses: 3800 },
  ];

  const claimsData = [
    { name: 'Processed', value: 400 },
    { name: 'Pending', value: 300 },
    { name: 'Rejected', value: 100 },
  ];

  const trendData = [
    { month: 'Jan', claims: 65, risk: 35 },
    { month: 'Feb', claims: 59, risk: 39 },
    { month: 'Mar', claims: 80, risk: 42 },
    { month: 'Apr', claims: 81, risk: 40 },
    { month: 'May', claims: 56, risk: 36 },
    { month: 'Jun', claims: 55, risk: 35 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      const decodedToken = jwtDecode(token);
      setUsername(decodedToken.username);
      setOrganization(location.state?.name || 'Your Organization');
    } else {
      navigate('/login');
    }
    // Fetch initial data
    fetchFinancialMetrics();
    fetchYearlyReports();
    fetchProcessedDocuments();
    fetchAIInsights();
  }, []);

  const fetchFinancialMetrics = async () => {
    // TODO: Implement API call to fetch metrics
    setFinancialMetrics({
      totalRevenue: 150000,
      totalExpenses: 80000,
      profitLoss: 70000,
      pendingClaims: 25
    });
  };

  const fetchYearlyReports = async () => {
    // TODO: Implement API call to fetch yearly reports
    setYearlyReports([
      { year: 2024, count: 5 },
      { year: 2023, count: 8 },
      { year: 2022, count: 12 }
    ]);
  };

  const fetchProcessedDocuments = async () => {
    // TODO: Implement API call to fetch processed documents
    setProcessedDocuments([
      { id: 1, name: 'Balance Sheet 2024', type: 'BALANCE_SHEET', status: 'Processed' },
      { id: 2, name: 'Charge Sheet Q1', type: 'CHARGESHEET', status: 'Processing' }
    ]);
  };

  const fetchAIInsights = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/insights/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setAiInsights(response.data);
    } catch (error) {
      console.error('Error fetching AI insights:', error);
      // Set mock data for now
      setAiInsights({
        riskScore: 75,
        recommendations: [
          'Consider increasing reserve allocation based on current claim trends',
          'Review policy pricing strategy for high-risk segments',
          'Optimize claim processing workflow to reduce pending claims'
        ],
        trends: {
          claimFrequency: 'increasing',
          averageClaimAmount: 'stable',
          customerSatisfaction: 'improving'
        },
        predictedMetrics: {
          nextMonthClaims: 85,
          expectedRevenue: 160000,
          projectedExpenses: 85000
        }
      });
    }
  };

  const handleFileUpload = async (file, year) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('organization', organization);
      formData.append('year', year);
      formData.append('reportType', reportType);

      const token = localStorage.getItem('accessToken');
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/documents/upload/`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 201) {
        message.success('File uploaded successfully');
        await processDocuments();
        fetchProcessedDocuments();
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      message.error(error.message || 'Failed to upload file');
    } finally {
      setLoading(false);
      setFile(null);
    }
  };

  const processDocuments = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      await axios.post(
        `${API_BASE_URL}/api/v1/documents/process/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      message.success('Documents processed successfully');
    } catch (error) {
      console.error('Error processing documents:', error);
      message.error('Failed to process documents');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  const userMenu = (
    <Menu>
      <Menu.Item key="profile">
        <UserOutlined /> Profile
      </Menu.Item>
      <Menu.Item key="logout" onClick={handleLogout}>
        <LogoutOutlined /> Logout
      </Menu.Item>
    </Menu>
  );

  const renderAIInsights = () => (
    <div className="ai-insights-section">
      <Card title="AI-Powered Insights" className="mb-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <Statistic
              title="Risk Score"
              value={aiInsights.riskScore}
              suffix="/100"
              valueStyle={{ color: aiInsights.riskScore > 70 ? '#3f8600' : '#cf1322' }}
            />
          </Card>
          <Card>
            <h4 className="text-lg font-semibold mb-2">Key Recommendations</h4>
            <ul className="list-disc pl-4">
              {aiInsights.recommendations.map((rec, index) => (
                <li key={index} className="text-sm text-gray-600">{rec}</li>
              ))}
            </ul>
          </Card>
        </div>
      </Card>
      
      <Card title="Predictive Analytics" className="mb-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Statistic
            title="Predicted Claims Next Month"
            value={aiInsights.predictedMetrics.nextMonthClaims}
            prefix={<BarChartOutlined />}
          />
          <Statistic
            title="Expected Revenue"
            value={aiInsights.predictedMetrics.expectedRevenue}
            prefix="$"
          />
          <Statistic
            title="Projected Expenses"
            value={aiInsights.predictedMetrics.projectedExpenses}
            prefix="$"
          />
        </div>
      </Card>

      <Card title="Trend Analysis">
        <LineChart width={800} height={300} data={trendData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="claims" stroke="#8884d8" name="Claims" />
          <Line type="monotone" dataKey="risk" stroke="#82ca9d" name="Risk Score" />
        </LineChart>
      </Card>
    </div>
  );

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div className="logo p-4">
          <h2 className="text-white text-xl font-bold">InsureTech</h2>
        </div>
        <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
          <Menu.Item key="1" icon={<DashboardOutlined />}>
            Dashboard
          </Menu.Item>
          <Menu.Item key="2" icon={<UploadOutlined />}>
            Upload Reports
          </Menu.Item>
          <Menu.Item key="3" icon={<BarChartOutlined />}>
            Analytics
          </Menu.Item>
          <Menu.Item key="4" icon={<SettingOutlined />}>
            Settings
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header className="bg-white p-0 flex justify-between items-center">
          <div className="px-4">
            <h1 className="text-xl">{organization}</h1>
          </div>
          <div className="px-4">
            <Dropdown overlay={userMenu}>
              <Avatar icon={<UserOutlined />} /> 
            </Dropdown>
          </div>
        </Header>
        <Content className="m-4">
          <div className="site-layout-background p-6">
            {/* Financial Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              <Card>
                <Statistic
                  title="Total Revenue"
                  value={financialMetrics.totalRevenue}
                  prefix={<DollarOutlined />}
                  valueStyle={{ color: '#3f8600' }}
                />
              </Card>
              <Card>
                <Statistic
                  title="Total Expenses"
                  value={financialMetrics.totalExpenses}
                  prefix={<DollarOutlined />}
                  valueStyle={{ color: '#cf1322' }}
                />
              </Card>
              <Card>
                <Statistic
                  title="Profit/Loss"
                  value={financialMetrics.profitLoss}
                  prefix={financialMetrics.profitLoss >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
                  valueStyle={{ color: financialMetrics.profitLoss >= 0 ? '#3f8600' : '#cf1322' }}
                />
              </Card>
              <Card>
                <Statistic
                  title="Pending Claims"
                  value={financialMetrics.pendingClaims}
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </div>

            {/* File Upload Section */}
            <Card title="Upload Financial Documents" className="mb-8">
              <Form layout="vertical">
                <Form.Item label="Document Type">
                  <Select value={reportType} onChange={setReportType}>
                    <Option value="BALANCE_SHEET">Balance Sheet</Option>
                    <Option value="CHARGESHEET">Charge Sheet</Option>
                  </Select>
                </Form.Item>
                <Form.Item label="Year">
                  <Input type="number" value={year} onChange={e => setYear(e.target.value)} />
                </Form.Item>
                <Form.Item>
                  <Upload
                    beforeUpload={(file) => {
                      setFile(file);
                      return false;
                    }}
                    fileList={file ? [file] : []}
                  >
                    <Button icon={<UploadOutlined />}>Select File</Button>
                  </Upload>
                </Form.Item>
                <Button 
                  type="primary" 
                  onClick={() => handleFileUpload(file, year)}
                  loading={loading}
                  disabled={!file}
                >
                  Upload and Process
                </Button>
              </Form>
            </Card>

            {/* Charts Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              <Card title="Revenue vs Expenses">
                <BarChart width={500} height={300} data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="revenue" fill="#8884d8" />
                  <Bar dataKey="expenses" fill="#82ca9d" />
                </BarChart>
              </Card>
              <Card title="Claims Processing">
                <PieChart width={400} height={300}>
                  <Pie
                    data={claimsData}
                    cx={200}
                    cy={150}
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {claimsData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </Card>
            </div>

            {/* Processed Documents */}
            <Card title="Processed Documents">
              <Table
                dataSource={processedDocuments}
                columns={[
                  { title: 'Name', dataIndex: 'name', key: 'name' },
                  { title: 'Type', dataIndex: 'type', key: 'type' },
                  { title: 'Status', dataIndex: 'status', key: 'status' },
                  {
                    title: 'Action',
                    key: 'action',
                    render: (_, record) => (
                      <Button type="link">View Details</Button>
                    ),
                  },
                ]}
              />
            </Card>

            {/* AI Insights */}
            {renderAIInsights()}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default Dashboard;
