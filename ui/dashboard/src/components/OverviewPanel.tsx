import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  People as PeopleIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface SystemStatus {
  status: 'online' | 'offline' | 'degraded';
  uptime: number;
  activeGoals: number;
  activeTasks: number;
  activeAgents: number;
  pendingApprovals: number;
}

interface OverviewPanelProps {
  systemStatus: SystemStatus;
}

const OverviewPanel: React.FC<OverviewPanelProps> = ({ systemStatus }) => {
  // Mock data for charts
  const performanceData = [
    { time: '00:00', tasks: 12, goals: 2 },
    { time: '04:00', tasks: 19, goals: 3 },
    { time: '08:00', tasks: 25, goals: 4 },
    { time: '12:00', tasks: 32, goals: 5 },
    { time: '16:00', tasks: 28, goals: 4 },
    { time: '20:00', tasks: 22, goals: 3 },
  ];

  const agentDistribution = [
    { name: 'Planner', value: 35, color: '#00ff88' },
    { name: 'Research', value: 25, color: '#ff4081' },
    { name: 'Marketing', value: 20, color: '#2196f3' },
    { name: 'Analytics', value: 20, color: '#ff9800' },
  ];

  const recentActivities = [
    { id: 1, type: 'goal', message: 'New goal created: "Increase website traffic"', time: '2 min ago', status: 'active' },
    { id: 2, type: 'task', message: 'Browser automation task completed', time: '5 min ago', status: 'completed' },
    { id: 3, type: 'approval', message: 'Deployment approval required', time: '10 min ago', status: 'pending' },
    { id: 4, type: 'agent', message: 'Research agent started analysis', time: '15 min ago', status: 'active' },
  ];

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'goal':
        return <AssignmentIcon />;
      case 'task':
        return <CheckCircleIcon />;
      case 'approval':
        return <ScheduleIcon />;
      case 'agent':
        return <PeopleIcon />;
      default:
        return <AssignmentIcon />;
    }
  };

  const getActivityColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'active':
        return 'primary';
      case 'pending':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <>
      {/* Key Metrics Row */}
      <Grid item xs={12}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: 'background.paper' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <AssignmentIcon sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6">Active Goals</Typography>
                </Box>
                <Typography variant="h3" sx={{ color: 'primary.main', fontWeight: 'bold' }}>
                  {systemStatus.activeGoals}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  +2 from yesterday
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: 'background.paper' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <ScheduleIcon sx={{ mr: 1, color: 'secondary.main' }} />
                  <Typography variant="h6">Active Tasks</Typography>
                </Box>
                <Typography variant="h3" sx={{ color: 'secondary.main', fontWeight: 'bold' }}>
                  {systemStatus.activeTasks}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  8 completed today
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: 'background.paper' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <PeopleIcon sx={{ mr: 1, color: 'success.main' }} />
                  <Typography variant="h6">Active Agents</Typography>
                </Box>
                <Typography variant="h3" sx={{ color: 'success.main', fontWeight: 'bold' }}>
                  {systemStatus.activeAgents}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  All systems operational
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ bgcolor: 'background.paper' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <ErrorIcon sx={{ mr: 1, color: systemStatus.pendingApprovals > 0 ? 'warning.main' : 'success.main' }} />
                  <Typography variant="h6">Pending Approvals</Typography>
                </Box>
                <Typography variant="h3" sx={{
                  color: systemStatus.pendingApprovals > 0 ? 'warning.main' : 'success.main',
                  fontWeight: 'bold'
                }}>
                  {systemStatus.pendingApprovals}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Requires attention
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Grid>

      {/* Charts Row */}
      <Grid item xs={12} md={8}>
        <Paper sx={{ p: 3, height: 400 }}>
          <Typography variant="h6" gutterBottom>
            System Performance (24h)
          </Typography>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="time" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px'
                }}
              />
              <Line
                type="monotone"
                dataKey="tasks"
                stroke="#00ff88"
                strokeWidth={2}
                name="Active Tasks"
              />
              <Line
                type="monotone"
                dataKey="goals"
                stroke="#ff4081"
                strokeWidth={2}
                name="Active Goals"
              />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 3, height: 400 }}>
          <Typography variant="h6" gutterBottom>
            Agent Distribution
          </Typography>
          <ResponsiveContainer width="100%" height="90%">
            <PieChart>
              <Pie
                data={agentDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {agentDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <Box sx={{ mt: 2 }}>
            {agentDistribution.map((item) => (
              <Box key={item.name} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    backgroundColor: item.color,
                    mr: 1
                  }}
                />
                <Typography variant="body2">
                  {item.name}: {item.value}%
                </Typography>
              </Box>
            ))}
          </Box>
        </Paper>
      </Grid>

      {/* Recent Activity */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Recent Activity
          </Typography>
          <List>
            {recentActivities.map((activity, index) => (
              <React.Fragment key={activity.id}>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'background.paper' }}>
                      {getActivityIcon(activity.type)}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={activity.message}
                    secondary={activity.time}
                  />
                  <Chip
                    label={activity.status}
                    color={getActivityColor(activity.status) as any}
                    size="small"
                  />
                </ListItem>
                {index < recentActivities.length - 1 && <Divider variant="inset" />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      </Grid>
    </>
  );
};

export default OverviewPanel;