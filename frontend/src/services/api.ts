import axios, { AxiosResponse } from 'axios';
import {
  User,
  Deal,
  Quota,
  Commission,
  CompensationPlan,
  DashboardStats,
  PipelineData,
  CommissionSummary,
  LoginCredentials,
  AuthResponse,
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: LoginCredentials): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/login/', credentials),
  
  logout: (): Promise<AxiosResponse<{ message: string }>> =>
    api.post('/auth/logout/'),
  
  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    api.get('/auth/me/'),
};

// Users API
export const usersAPI = {
  getUsers: (): Promise<AxiosResponse<User[]>> =>
    api.get('/auth/users/'),
  
  getUser: (id: number): Promise<AxiosResponse<User>> =>
    api.get(`/auth/users/${id}/`),
  
  createUser: (userData: Partial<User>): Promise<AxiosResponse<User>> =>
    api.post('/auth/users/', userData),
  
  updateUser: (id: number, userData: Partial<User>): Promise<AxiosResponse<User>> =>
    api.patch(`/auth/users/${id}/`, userData),
};

// Sales API
export const salesAPI = {
  getDeals: (params?: Record<string, any>): Promise<AxiosResponse<Deal[]>> =>
    api.get('/sales/deals/', { params }),
  
  getDeal: (id: number): Promise<AxiosResponse<Deal>> =>
    api.get(`/sales/deals/${id}/`),
  
  createDeal: (dealData: Partial<Deal>): Promise<AxiosResponse<Deal>> =>
    api.post('/sales/deals/', dealData),
  
  updateDeal: (id: number, dealData: Partial<Deal>): Promise<AxiosResponse<Deal>> =>
    api.patch(`/sales/deals/${id}/`, dealData),
  
  deleteDeal: (id: number): Promise<AxiosResponse<void>> =>
    api.delete(`/sales/deals/${id}/`),
  
  getQuotas: (): Promise<AxiosResponse<Quota[]>> =>
    api.get('/sales/quotas/'),
  
  createQuota: (quotaData: Partial<Quota>): Promise<AxiosResponse<Quota>> =>
    api.post('/sales/quotas/', quotaData),
  
  getDashboardStats: (): Promise<AxiosResponse<DashboardStats>> =>
    api.get('/sales/dashboard-stats/'),
  
  getPipelineAnalysis: (): Promise<AxiosResponse<PipelineData[]>> =>
    api.get('/sales/pipeline-analysis/'),
  
  getQuotaPerformance: (): Promise<AxiosResponse<any[]>> =>
    api.get('/sales/quota-performance/'),
};

// Commissions API
export const commissionsAPI = {
  getCompensationPlans: (): Promise<AxiosResponse<CompensationPlan[]>> =>
    api.get('/commissions/plans/'),
  
  getCompensationPlan: (id: number): Promise<AxiosResponse<CompensationPlan>> =>
    api.get(`/commissions/plans/${id}/`),
  
  createCompensationPlan: (planData: Partial<CompensationPlan>): Promise<AxiosResponse<CompensationPlan>> =>
    api.post('/commissions/plans/', planData),
  
  getCommissions: (params?: Record<string, any>): Promise<AxiosResponse<Commission[]>> =>
    api.get('/commissions/commissions/', { params }),
  
  getCommission: (id: number): Promise<AxiosResponse<Commission>> =>
    api.get(`/commissions/commissions/${id}/`),
  
  updateCommission: (id: number, commissionData: Partial<Commission>): Promise<AxiosResponse<Commission>> =>
    api.patch(`/commissions/commissions/${id}/`, commissionData),
  
  calculateCommissions: (dealIds?: number[]): Promise<AxiosResponse<{ message: string; commission_ids: number[] }>> =>
    api.post('/commissions/calculate/', { deal_ids: dealIds }),
  
  getCommissionSummary: (): Promise<AxiosResponse<CommissionSummary>> =>
    api.get('/commissions/summary/'),
  
  getCommissionAnalytics: (params?: Record<string, any>): Promise<AxiosResponse<any>> =>
    api.get('/commissions/analytics/', { params }),
  
  getCommissionProjections: (params?: Record<string, any>): Promise<AxiosResponse<any>> =>
    api.get('/commissions/projections/', { params }),
  
  getCommissionTrends: (params?: Record<string, any>): Promise<AxiosResponse<any>> =>
    api.get('/commissions/trends/', { params }),
};

export default api;