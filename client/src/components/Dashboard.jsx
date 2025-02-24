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
  
  // Financial Data States
  const [financialData, setFinancialData] = useState({
    chargesheet_data: [],
    balance_sheet_data: [],
    revenue_trend: [],
    expense_trend: [],
    anomalies: [],
    revenue_forecast: [],
    summary_metrics: {
      total_documents: 0,
      total_revenue: 0,
      total_expense: 0,
      total_profit: 0,
      latest_update: null,
      profit_margin: 0,
      current_ratio: 0,
      debt_equity_ratio: 0,
      revenue_growth: 0
    }
  });
  
  const [processedDocuments, setProcessedDocuments] = useState([]);
  const [username, setUsername] = useState('');
  const [organization, setOrganization] = useState('');

  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: 'Dashboard'
    },
    {
      key: '2',
      icon: <UploadOutlined />,
      label: 'Upload Reports'
    },
    {
      key: '3',
      icon: <BarChartOutlined />,
      label: 'Analytics'
    },
    {
      key: '4',
      icon: <SettingOutlined />,
      label: 'Settings'
    }
  ];

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile'
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: () => {
        localStorage.removeItem('accessToken');
        navigate('/login');
      }
    }
  ];

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      const decodedToken = jwtDecode(token);
      setUsername(decodedToken.username);
      setOrganization(location.state?.name || 'Your Organization');
      fetchAllFinancialData();
    } else {
      navigate('/login');
    }
  }, []);

  const fetchAllFinancialData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('accessToken');
      
      // Add error handling for missing token
      if (!token) {
        message.error('Authentication token not found. Please login again.');
        navigate('/login');
        return;
      }

      const response = await axios.get(
        `${API_BASE_URL}/api/v1/financial-data/`, // updated endpoint
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          timeout: 10000 // 10 second timeout
        }
      );
      
      // Add response validation
      if (!response.data) {
        throw new Error('No data received from server');
      }

      const data = response.data;
      const totalRevenue = data.summary_metrics.total_revenue;
      const totalExpense = data.summary_metrics.total_expense;
      
      data.summary_metrics = {
        ...data.summary_metrics,
        profit_margin: totalRevenue ? ((totalRevenue - totalExpense) / totalRevenue) * 100 : 0,
        current_ratio: data.balance_sheet_data.length > 0 ? 
          data.balance_sheet_data[data.balance_sheet_data.length - 1].current_assets / 
          data.balance_sheet_data[data.balance_sheet_data.length - 1].current_liabilities : 0,
        debt_equity_ratio: data.balance_sheet_data.length > 0 ?
          data.balance_sheet_data[data.balance_sheet_data.length - 1].total_liabilities /
          data.balance_sheet_data[data.balance_sheet_data.length - 1].total_equity : 0,
        revenue_growth: data.revenue_trend.length > 1 ?
          ((data.revenue_trend[data.revenue_trend.length - 1].total_revenue -
            data.revenue_trend[data.revenue_trend.length - 2].total_revenue) /
            data.revenue_trend[data.revenue_trend.length - 2].total_revenue) * 100 : 0
      };
      
      setFinancialData(data);
      setProcessedDocuments([
        ...data.chargesheet_data.map(doc => ({
          id: doc.id,
          name: doc.document__file_name,
          type: 'CHARGESHEET',
          status: 'Processed',
          date: doc.date
        })),
        ...data.balance_sheet_data.map(doc => ({
          id: doc.id,
          name: doc.document__file_name,
          type: 'BALANCE_SHEET',
          status: 'Processed',
          date: doc.document__uploaded_at
        }))
      ]);
    } catch (error) {
      console.error('Error fetching financial data:', error);
      message.error('Failed to fetch financial data');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('organization', organization);
      formData.append('year', year);
      formData.append('reportType', reportType);

      const token = localStorage.getItem('accessToken');
      const response = await axios.post(
        `${API_BASE_URL}/documents/upload/`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 201) {
        message.success('File uploaded successfully');
        // Refresh financial data after upload
        fetchAllFinancialData();
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      message.error(error.message || 'Failed to upload file');
    } finally {
      setLoading(false);
      setFile(null);
    }
  };

  const renderFinancialMetrics = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <Card>
        <Statistic
          title="Total Revenue"
          value={financialData.summary_metrics.total_revenue}
          prefix="$"
          valueStyle={{ color: '#3f8600' }}
        />
      </Card>
      <Card>
        <Statistic
          title="Total Expenses"
          value={financialData.summary_metrics.total_expense}
          prefix="$"
          valueStyle={{ color: '#cf1322' }}
        />
      </Card>
      <Card>
        <Statistic
          title="Net Profit"
          value={financialData.summary_metrics.total_profit}
          prefix="$"
          valueStyle={{ color: financialData.summary_metrics.total_profit >= 0 ? '#3f8600' : '#cf1322' }}
          suffix={
            <small style={{ fontSize: '14px' }}>
              ({financialData.summary_metrics.profit_margin.toFixed(2)}% margin)
            </small>
          }
        />
      </Card>
      <Card>
        <Statistic
          title="Revenue Growth"
          value={financialData.summary_metrics.revenue_growth}
          suffix="%"
          prefix={financialData.summary_metrics.revenue_growth >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          valueStyle={{ color: financialData.summary_metrics.revenue_growth >= 0 ? '#3f8600' : '#cf1322' }}
        />
      </Card>
      <Card>
        <Statistic
          title="Current Ratio"
          value={financialData.summary_metrics.current_ratio.toFixed(2)}
          valueStyle={{ color: financialData.summary_metrics.current_ratio >= 1 ? '#3f8600' : '#cf1322' }}
        />
      </Card>
      <Card>
        <Statistic
          title="Debt to Equity"
          value={financialData.summary_metrics.debt_equity_ratio.toFixed(2)}
          valueStyle={{ color: financialData.summary_metrics.debt_equity_ratio <= 2 ? '#3f8600' : '#cf1322' }}
        />
      </Card>
      <Card>
        <Statistic
          title="Total Documents"
          value={financialData.summary_metrics.total_documents}
          prefix={<FileTextOutlined />}
        />
      </Card>
      <Card>
        <Statistic
          title="Last Update"
          value={financialData.summary_metrics.latest_update ? 
            new Date(financialData.summary_metrics.latest_update).toLocaleDateString() :
            'No data'
          }
        />
      </Card>
    </div>
  );

  const renderRevenueTrend = () => {
    const chartData = financialData.revenue_trend.map(item => ({
      year: item.document__year,
      revenue: item.total_revenue,
      expenses: financialData.expense_trend.find(
        exp => exp.document__year === item.document__year
      )?.total_expense || 0,
      profit: item.total_revenue - (financialData.expense_trend.find(
        exp => exp.document__year === item.document__year
      )?.total_expense || 0)
    }));

    return (
      <Card title="Financial Performance Trend" className="mb-4">
        <div style={{ overflowX: 'auto' }}>
          <LineChart width={800} height={400} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="revenue" 
              stroke="#3f8600" 
              name="Revenue"
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="expenses" 
              stroke="#cf1322" 
              name="Expenses"
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="profit" 
              stroke="#8884d8" 
              name="Profit"
              strokeWidth={2}
            />
          </LineChart>
        </div>
      </Card>
    );
  };

  const renderAnomalies = () => (
    <Card title="Detected Anomalies" className="mb-4">
      <Table
        dataSource={financialData.anomalies}
        columns={[
          {
            title: 'Year',
            dataKey: 'document__year',
            key: 'year',
          },
          {
            title: 'Revenue',
            dataKey: 'total_revenue',
            key: 'revenue',
            render: (value) => `$${value.toLocaleString()}`,
          },
          {
            title: 'Expenses',
            dataKey: 'total_expense',
            key: 'expenses',
            render: (value) => `$${value.toLocaleString()}`,
          },
          {
            title: 'Net Profit',
            dataKey: 'net_profit',
            key: 'profit',
            render: (value) => `$${value.toLocaleString()}`,
          }
        ]}
      />
    </Card>
  );

  const renderForecast = () => {
    const forecastData = financialData.revenue_forecast.map(([year, value]) => ({
      year,
      forecast: value
    }));

    return (
      <Card title="Revenue Forecast" className="mb-4">
        <LineChart width={800} height={300} data={forecastData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="forecast" stroke="#8884d8" name="Forecasted Revenue" />
        </LineChart>
      </Card>
    );
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div className="logo p-4">
          <h2 className="text-white text-xl font-bold">InsureTech</h2>
        </div>
        <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={menuItems} />
      </Sider>
      <Layout>
        <Header className="bg-white p-0 flex justify-between items-center">
          <div className="px-4">
            <h1 className="text-xl">{organization}</h1>
          </div>
          <div className="px-4">
            <Dropdown menu={{ items: userMenuItems }}>
              <Avatar icon={<UserOutlined />} /> 
            </Dropdown>
          </div>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, minHeight: 280 }}>
          {loading ? (
            <div className="flex justify-center items-center h-full">
              <Spin size="large" />
            </div>
          ) : (
            <>
              {renderFinancialMetrics()}
              {renderRevenueTrend()}
              {renderAnomalies()}
              {renderForecast()}
              
              <Card title="Document Upload" className="mb-4">
                <Form layout="vertical">
                  <Form.Item label="Report Type">
                    <Select value={reportType} onChange={setReportType}>
                      <Option value="BALANCE_SHEET">Balance Sheet</Option>
                      <Option value="CHARGESHEET">Charge Sheet</Option>
                    </Select>
                  </Form.Item>
                  <Form.Item label="Year">
                    <Input type="number" value={year} onChange={e => setYear(e.target.value)} />
                  </Form.Item>
                  <Upload
                    beforeUpload={(file) => {
                      setFile(file);
                      return false;
                    }}
                    fileList={file ? [file] : []}
                  >
                    <Button icon={<UploadOutlined />}>Select File</Button>
                  </Upload>
                  {file && (
                    <Button
                      type="primary"
                      onClick={() => handleFileUpload(file)}
                      style={{ marginTop: 16 }}
                      loading={loading}
                    >
                      Upload
                    </Button>
                  )}
                </Form>
              </Card>

              <Card title="Processed Documents">
                <Table
                  dataSource={processedDocuments}
                  columns={[
                    {
                      title: 'Document Name',
                      dataIndex: 'name',
                      key: 'name',
                    },
                    {
                      title: 'Type',
                      dataIndex: 'type',
                      key: 'type',
                    },
                    {
                      title: 'Status',
                      dataIndex: 'status',
                      key: 'status',
                    },
                    {
                      title: 'Date',
                      dataIndex: 'date',
                      key: 'date',
                      render: (date) => new Date(date).toLocaleDateString(),
                    },
                  ]}
                />
              </Card>
            </>
          )}
        </Content>
      </Layout>
    </Layout>
  );
};

export default Dashboard;
