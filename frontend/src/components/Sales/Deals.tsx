import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridValueGetterParams,
  GridRenderCellParams,
} from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { salesAPI } from '../../services/api';
import { Deal } from '../../types';

const Deals: React.FC = () => {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchDeals();
  }, []);

  const fetchDeals = async () => {
    try {
      setLoading(true);
      const response = await salesAPI.getDeals();
      setDeals(response.data);
    } catch (error: any) {
      setError('Failed to load deals');
      console.error('Deals error:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: string | number) => {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num);
  };

  const getStatusChip = (status: string) => {
    const statusConfig = {
      open: { color: 'primary' as const, label: 'Open' },
      closed_won: { color: 'success' as const, label: 'Won' },
      closed_lost: { color: 'error' as const, label: 'Lost' },
    };

    const config = statusConfig[status as keyof typeof statusConfig] || {
      color: 'default' as const,
      label: status,
    };

    return <Chip label={config.label} color={config.color} size="small" />;
  };

  const getStageChip = (stage: string) => {
    const stageConfig = {
      prospecting: { color: 'default' as const },
      qualification: { color: 'primary' as const },
      proposal: { color: 'secondary' as const },
      negotiation: { color: 'warning' as const },
      closed: { color: 'success' as const },
    };

    const config = stageConfig[stage as keyof typeof stageConfig] || {
      color: 'default' as const,
    };

    return (
      <Chip
        label={stage.charAt(0).toUpperCase() + stage.slice(1)}
        color={config.color}
        size="small"
        variant="outlined"
      />
    );
  };

  const columns: GridColDef[] = [
    {
      field: 'name',
      headerName: 'Deal Name',
      width: 200,
      flex: 1,
    },
    {
      field: 'account_name',
      headerName: 'Account',
      width: 150,
      flex: 1,
    },
    {
      field: 'owner_name',
      headerName: 'Owner',
      width: 150,
    },
    {
      field: 'amount',
      headerName: 'Amount',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => 
        formatCurrency(params.row.amount),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 100,
      renderCell: (params: GridRenderCellParams) => 
        getStatusChip(params.value),
    },
    {
      field: 'stage',
      headerName: 'Stage',
      width: 130,
      renderCell: (params: GridRenderCellParams) => 
        getStageChip(params.value),
    },
    {
      field: 'probability',
      headerName: 'Probability',
      width: 100,
      valueGetter: (params: GridValueGetterParams) => `${params.row.probability}%`,
    },
    {
      field: 'close_date',
      headerName: 'Close Date',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => 
        new Date(params.row.close_date).toLocaleDateString(),
    },
    {
      field: 'days_since_created',
      headerName: 'Age (Days)',
      width: 100,
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      renderCell: (params: GridRenderCellParams) => (
        <Box>
          <Tooltip title="View">
            <IconButton
              size="small"
              onClick={() => handleView(params.row.id)}
            >
              <ViewIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Edit">
            <IconButton
              size="small"
              onClick={() => handleEdit(params.row.id)}
            >
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton
              size="small"
              onClick={() => handleDelete(params.row.id)}
              color="error"
            >
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  const handleView = (id: number) => {
    console.log('View deal:', id);
    // Implement view logic
  };

  const handleEdit = (id: number) => {
    console.log('Edit deal:', id);
    // Implement edit logic
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this deal?')) {
      try {
        await salesAPI.deleteDeal(id);
        fetchDeals(); // Refresh the list
      } catch (error) {
        console.error('Delete error:', error);
      }
    }
  };

  const handleAddDeal = () => {
    console.log('Add new deal');
    // Implement add logic
  };

  return (
    <Container maxWidth={false}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4">
          Deals Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddDeal}
        >
          Add Deal
        </Button>
      </Box>

      <Paper sx={{ width: '100%' }}>
        <DataGrid
          rows={deals}
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

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
    </Container>
  );
};

export default Deals;