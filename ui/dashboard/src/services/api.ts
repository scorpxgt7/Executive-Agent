import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface Goal {
  id: string;
  description: string;
  objectives: string[];
  constraints?: Record<string, any>;
  deadline?: string;
  priority: number;
  status: string;
  created_at: string;
}

export interface ExecutionPlan {
  id: string;
  goal_id: string;
  tasks: Task[];
  approval_required: boolean;
  approved: boolean;
  learning_insights?: Record<string, any>;
  created_at: string;
}

export interface Task {
  id: string;
  goal_id: string;
  description: string;
  type: string;
  parameters: Record<string, any>;
  assigned_agent?: string;
  status: string;
  dependencies: string[];
  created_at: string;
  completed_at?: string;
}

export interface GoalResponse {
  goal_id: string;
  plan_id: string;
  status: string;
  learning_insights?: Record<string, any>;
  task_count: number;
}

export interface GoalsListResponse {
  goals: GoalResponse[];
}

export interface CreateGoalRequest {
  id: string;
  description: string;
  objectives: string[];
  constraints?: Record<string, any>;
  deadline?: string;
  priority?: number;
}

class ApiService {
  private axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async createGoal(goal: CreateGoalRequest): Promise<{ plan_id: string; status: string; learning_insights?: Record<string, any> }> {
    const response = await this.axiosInstance.post('/api/v1/goals/', goal);
    return response.data;
  }

  async getGoals(): Promise<GoalsListResponse> {
    const response = await this.axiosInstance.get('/api/v1/goals/');
    return response.data;
  }

  async getGoal(goalId: string): Promise<GoalResponse> {
    const response = await this.axiosInstance.get(`/api/v1/goals/${goalId}`);
    return response.data;
  }

  async getTasks(): Promise<Task[]> {
    const response = await this.axiosInstance.get('/api/v1/tasks/');
    return response.data.tasks || [];
  }

  async getAgents(): Promise<any[]> {
    const response = await this.axiosInstance.get('/api/v1/agents/');
    return response.data.agents || [];
  }

  async getApprovals(): Promise<any[]> {
    const response = await this.axiosInstance.get('/api/v1/approvals/');
    return response.data.approvals || [];
  }

  async approveApproval(approvalId: string): Promise<void> {
    await this.axiosInstance.post(`/api/v1/approvals/${approvalId}/approve`);
  }

  async getHealth(): Promise<{ status: string }> {
    const response = await this.axiosInstance.get('/health');
    return response.data;
  }
}

export const apiService = new ApiService();