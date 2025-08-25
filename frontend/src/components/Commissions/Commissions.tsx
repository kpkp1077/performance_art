import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  Chip,
  Grid,
  Card,
  CardContent,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridValueGetterParams,
  GridRenderCellParams,
} from '@mui/x-data-grid';
import {
  Calculate as CalculateIcon,
  TrendingUp,
  AttachMoney,
  Assessment,
} from '@mui/icons-material';
import { commissionsAPI } from '../../services/api';
import { Commission, CommissionSummary } from '../../types';

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
          <Typography variant="h5" component="div">
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

const Commissions: React.FC = () => {
  const [commissions, setCommissions] = useState<Commission[]>([]);
  const [summary, setSummary] = useState<CommissionSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');

  useEffect(() => {
    fetchCommissionsData();
  }, []);

  const fetchCommissionsData = async () => {
    try {
      setLoading(true);
      const [commissionsResponse, summaryResponse] = await Promise.all([
        commissionsAPI.getCommissions(),
        commissionsAPI.getCommissionSummary(),
      ]);
      
      setCommissions(commissionsResponse.data);
      setSummary(summaryResponse.data);
    } catch (error: any) {
      setError('Failed to load commissions data');
      console.error('Commissions error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCalculateCommissions = async () => {
    try {
      setCalculating(true);
      const response = await commissionsAPI.calculateCommissions();
      setSuccessMessage(response.data.message);
      fetchCommissionsData(); // Refresh data
    } catch (error: any) {
      setError('Failed to calculate commissions');
      console.error('Calculate error:', error);
    } finally {
      setCalculating(false);
    }
  };

  const formatCurrency = (value: string | number) => {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(num);
  };

  const getStatusChip = (status: string) => {
    const statusConfig = {
      pending: { color: 'warning' as const, label: 'Pending' },
      calculated: { color: 'info' as const, label: 'Calculated' },
      paid: { color: 'success' as const, label: 'Paid' },
      disputed: { color: 'error' as const, label: 'Disputed' },
    };

    const config = statusConfig[status as keyof typeof statusConfig] || {
      color: 'default' as const,
      label: status,
    };

    return <Chip label={config.label} color={config.color} size="small" />;
  };

  const columns: GridColDef[] = [
    {
      field: 'user_name',
      headerName: 'Sales Rep',
      width: 150,
      flex: 1,
    },
    {
      field: 'deal_name',
      headerName: 'Deal',
      width: 200,
      flex: 1,
    },
    {
      field: 'plan_name',
      headerName: 'Plan',
      width: 150,
    },
    {
      field: 'deal_amount',
      headerName: 'Deal Amount',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => 
        formatCurrency(params.row.deal_amount),
    },
    {
      field: 'commission_rate',
      headerName: 'Rate',
      width: 80,
      valueGetter: (params: GridValueGetterParams) => `${params.row.commission_rate}%`,
    },
    {
      field: 'commission_amount',
      headerName: 'Commission',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => 
        formatCurrency(params.row.commission_amount),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params: GridRenderCellParams) => 
        getStatusChip(params.value),
    },
    {
      field: 'calculation_date',
      headerName: 'Calculated',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => 
        new Date(params.row.calculation_date).toLocaleDateString(),
    },
    {
      field: 'payment_date',
      headerName: 'Paid Date',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => 
        params.row.payment_date 
          ? new Date(params.row.payment_date).toLocaleDateString()
          : '-',
    },
  ];

  return (
    <Container maxWidth={false}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4">
          Commission Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<CalculateIcon />}
          onClick={handleCalculateCommissions}
          disabled={calculating}
        >
          {calculating ? 'Calculating...' : 'Calculate Commissions'}
        </Button>
      </Box>

      {/* Summary Cards */}
      {summary && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Total Commissions"
              value={formatCurrency(summary.total_commissions)}
              icon={<AttachMoney fontSize="large" />}
              color="#1976d2"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Pending Commissions"
              value={formatCurrency(summary.pending_commissions)}
              icon={<TrendingUp fontSize="large" />}
              color="#ed6c02"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Paid Commissions"
              value={formatCurrency(summary.paid_commissions)}
              icon={<AttachMoney fontSize="large" />}
              color="#2e7d32"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Average Commission"
              value={formatCurrency(summary.average_commission)}
              icon={<Assessment fontSize="large" />}
              color="#9c27b0"
            />
          </Grid>
        </Grid>
      )}

      {/* Commissions Data Grid */}
      <Paper sx={{ width: '100%' }}>
        <DataGrid
          rows={commissions}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 25 },
            },
          }}
          pageSizeOptions={[25, 50, 100]}
          loading={loading}
          sx={{ border: 0 }}
          autoHeight
          disableRowSelectionOnClick
        />
      </Paper>

      {/* Error Snackbar */}
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError('')}
      >
        <Alert onClose={() => setError('')} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      {/* Success Snackbar */}
      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage('')}
      >
        <Alert onClose={() => setSuccessMessage('')} severity="success" sx={{ width: '100%' }}>
          {successMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Commissions;