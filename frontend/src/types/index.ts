export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'manager' | 'rep';
  employee_id?: string;
  phone?: string;
  hire_date?: string;
  is_active_sales: boolean;
  created_at: string;
  updated_at: string;
}

export interface Deal {
  id: number;
  name: string;
  account_name: string;
  owner: number;
  owner_name: string;
  amount: string;
  status: 'open' | 'closed_won' | 'closed_lost';
  stage: 'prospecting' | 'qualification' | 'proposal' | 'negotiation' | 'closed';
  probability: number;
  close_date: string;
  created_date: string;
  last_activity: string;
  description?: string;
  days_since_created: number;
}

export interface Quota {
  id: number;
  user: number;
  user_name: string;
  amount: string;
  period: 'monthly' | 'quarterly' | 'annual';
  start_date: string;
  end_date: string;
  created_at: string;
  attainment_percentage: number;
}

export interface CompensationPlan {
  id: number;
  name: string;
  plan_type: 'flat_rate' | 'percentage' | 'tiered' | 'quota_based';
  base_rate: string;
  threshold_amount?: string;
  accelerator_rate?: string;
  is_active: boolean;
  description?: string;
  created_at: string;
  updated_at: string;
  rules: CommissionRule[];
}

export interface CommissionRule {
  id: number;
  min_amount?: string;
  max_amount?: string;
  commission_rate: string;
  order: number;
}

export interface Commission {
  id: number;
  user: number;
  user_name: string;
  deal: number;
  deal_name: string;
  compensation_plan: number;
  plan_name: string;
  commission_amount: string;
  commission_rate: string;
  deal_amount: string;
  status: 'pending' | 'calculated' | 'paid' | 'disputed';
  calculation_date: string;
  payment_date?: string;
  notes?: string;
}

export interface DashboardStats {
  total_deals: number;
  total_value: string;
  won_deals: number;
  won_value: string;
  lost_deals: number;
  open_deals: number;
  average_deal_size: string;
  win_rate: string;
}

export interface PipelineData {
  stage: string;
  count: number;
  total_value: string;
  avg_probability: number;
}

export interface CommissionSummary {
  total_commissions: string;
  pending_commissions: string;
  paid_commissions: string;
  commission_count: number;
  average_commission: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}