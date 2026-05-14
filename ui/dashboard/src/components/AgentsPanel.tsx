import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Avatar,
  Chip,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  LinearProgress,
} from '@mui/material';
import {
  Psychology as BrainIcon,
  Search as SearchIcon,
  Campaign as CampaignIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';

const AgentsPanel: React.FC = () => {
  const agents = [
    {
      id: 'planner',
      name: 'Strategic Planner',
      type: 'Planning',
      status: 'active',
      tasksCompleted: 45,
      currentTask: 'Analyzing market opportunities',
      icon: <BrainIcon />,
      color: '#00ff88'
    },
    {
      id: 'research',
      name: 'Market Researcher',
      type: 'Research',
      status: 'active',
      tasksCompleted: 32,
      currentTask: 'Gathering competitive intelligence',
      icon: <SearchIcon />,
      color: '#ff4081'
    },
    {
      id: 'marketing',
      name: 'Content Marketer',
      type: 'Marketing',
      status: 'idle',
      tasksCompleted: 28,
      currentTask: 'Waiting for content requests',
      icon: <CampaignIcon />,
      color: '#2196f3'
    },
    {
      id: 'analytics',
      name: 'Performance Analyst',
      type: 'Analytics',
      status: 'active',
      tasksCompleted: 19,
      currentTask: 'Generating performance reports',
      icon: <AnalyticsIcon />,
      color: '#ff9800'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'idle':
        return 'default';
      case 'busy':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Agent Status
        </Typography>
      </Grid>

      {agents.map((agent) => (
        <Grid item xs={12} md={6} lg={3} key={agent.id}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: agent.color, mr: 2 }}>
                  {agent.icon}
                </Avatar>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h6">{agent.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {agent.type}
                  </Typography>
                </Box>
                <Chip
                  label={agent.status}
                  color={getStatusColor(agent.status) as any}
                  size="small"
                />
              </Box>

              <Typography variant="body2" sx={{ mb: 1 }}>
                Tasks Completed: {agent.tasksCompleted}
              </Typography>

              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Current: {agent.currentTask}
              </Typography>

              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography variant="body2" sx={{ mr: 1 }}>
                  Activity
                </Typography>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={agent.status === 'active' ? 75 : agent.status === 'idle' ? 25 : 100}
                    sx={{ height: 6, borderRadius: 3 }}
                  />
                </Box>
                <Typography variant="caption">
                  {agent.status === 'active' ? '75%' : agent.status === 'idle' ? '25%' : '100%'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}

      <Grid item xs={12}>
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Agent Activity Log
          </Typography>
          <List>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: '#00ff88' }}>
                  <BrainIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary="Strategic Planner completed goal analysis"
                secondary="2 minutes ago"
              />
            </ListItem>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: '#ff4081' }}>
                  <SearchIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary="Market Researcher started competitor analysis"
                secondary="5 minutes ago"
              />
            </ListItem>
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: '#2196f3' }}>
                  <CampaignIcon />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary="Content Marketer published blog post"
                secondary="12 minutes ago"
              />
            </ListItem>
          </List>
        </Paper>
      </Grid>
    </>
  );
};

export default AgentsPanel;