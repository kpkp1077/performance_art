import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  AttachMoney,
  Assessment,
  CheckCircle,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';
import { salesAPI, commissionsAPI } from '../../services/api';
import { DashboardStats, PipelineData, CommissionSummary } from '../../types';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Typography color="textSecondary" gutterBottom variant="body2">
            {title}
          </Typography>
          <Typography variant="h4" component="div">
            {value}
          </Typography>
        </Box>
        <Box sx={{ color: color }}>
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard: React.FC = () => {
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [pipelineData, setPipelineData] = useState<PipelineData[]>([]);
  const [commissionSummary, setCommissionSummary] = useState<CommissionSummary | null>(null);
  const [quotaPerformance, setQuotaPerformance] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        const [statsResponse, pipelineResponse, commissionResponse, quotaResponse] = await Promise.all([
          salesAPI.getDashboardStats(),
          salesAPI.getPipelineAnalysis(),
          commissionsAPI.getCommissionSummary(),
          salesAPI.getQuotaPerformance(),
        ]);

        setDashboardStats(statsResponse.data);
        setPipelineData(pipelineResponse.data);
        setCommissionSummary(commissionResponse.data);
        setQuotaPerformance(quotaResponse.data);
      } catch (error: any) {
        setError('Failed to load dashboard data');
        console.error('Dashboard error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  const formatCurrency = (value: string | number) => {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num);
  };

  const formatPercentage = (value: string | number) => {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return `${num.toFixed(1)}%`;
  };

  const pipelineChartData = pipelineData.map(item => ({
    stage: item.stage.charAt(0).toUpperCase() + item.stage.slice(1),
    deals: item.count,
    value: parseFloat(item.total_value),
    probability: item.avg_probability,
  }));

  const quotaChartData = quotaPerformance.slice(0, 10).map(item => ({
    name: item.user_name.split(' ')[0],
    quota: parseFloat(item.quota_amount),
    achieved: parseFloat(item.achieved_amount),
    attainment: parseFloat(item.attainment_percentage),
  }));

  return (
    <Container maxWidth={false}>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Sales Dashboard
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total Deals"
            value={dashboardStats?.total_deals || 0}
            icon={<Assessment fontSize="large" />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total Revenue"
            value={formatCurrency(dashboardStats?.total_value || 0)}
            icon={<AttachMoney fontSize="large" />}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Win Rate"
            value={formatPercentage(dashboardStats?.win_rate || 0)}
            icon={<TrendingUp fontSize="large" />}
            color="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Deals Won"
            value={dashboardStats?.won_deals || 0}
            icon={<CheckCircle fontSize="large" />}
            color="#2e7d32"
          />
        </Grid>
      </Grid>

      {/* Commission Metrics */}
      {commissionSummary && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Total Commissions"
              value={formatCurrency(commissionSummary.total_commissions)}
              icon={<AttachMoney fontSize="large" />}
              color="#1976d2"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Pending Commissions"
              value={formatCurrency(commissionSummary.pending_commissions)}
              icon={<AttachMoney fontSize="large" />}
              color="#ed6c02"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Paid Commissions"
              value={formatCurrency(commissionSummary.paid_commissions)}
              icon={<CheckCircle fontSize="large" />}
              color="#2e7d32"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Avg Commission"
              value={formatCurrency(commissionSummary.average_commission)}
              icon={<Assessment fontSize="large" />}
              color="#9c27b0"
            />
          </Grid>
        </Grid>
      )}

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Sales Pipeline Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Sales Pipeline by Stage
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pipelineChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="stage" />
                <YAxis />
                <Tooltip formatter={(value, name) => [
                  name === 'value' ? formatCurrency(value as number) : value,
                  name === 'deals' ? 'Deals' : name === 'value' ? 'Value' : 'Avg Probability'
                ]} />
                <Legend />
                <Bar dataKey="deals" fill="#8884d8" name="Deals" />
                <Bar dataKey="value" fill="#82ca9d" name="Value" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Quota Performance Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Quota Attainment (Top 10)
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={quotaChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value, name) => [
                  name === 'attainment' ? formatPercentage(value as number) : formatCurrency(value as number),
                  name === 'quota' ? 'Quota' : name === 'achieved' ? 'Achieved' : 'Attainment %'
                ]} />
                <Legend />
                <Bar dataKey="quota" fill="#ff7300" name="Quota" />
                <Bar dataKey="achieved" fill="#387908" name="Achieved" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Deal Status Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Deal Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={[
                    { name: 'Open', value: dashboardStats?.open_deals || 0 },
                    { name: 'Won', value: dashboardStats?.won_deals || 0 },
                    { name: 'Lost', value: dashboardStats?.lost_deals || 0 },
                  ]}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {[{ name: 'Open' }, { name: 'Won' }, { name: 'Lost' }].map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Revenue Trend (Mock data for demo) */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Revenue Trend (Last 6 Months)
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={[
                  { month: 'Jan', revenue: 65000 },
                  { month: 'Feb', revenue: 59000 },
                  { month: 'Mar', revenue: 80000 },
                  { month: 'Apr', revenue: 81000 },
                  { month: 'May', revenue: 56000 },
                  { month: 'Jun', revenue: 95000 },
                ]}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
                <Legend />
                <Line type="monotone" dataKey="revenue" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;