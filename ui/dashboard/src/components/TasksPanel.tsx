import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Chip,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

const TasksPanel: React.FC = () => {
  const tasks = [
    {
      id: '1',
      title: 'Scrape competitor pricing data',
      status: 'running',
      agent: 'Browser Worker',
      progress: 65,
      started: '10 min ago'
    },
    {
      id: '2',
      title: 'Send marketing emails',
      status: 'completed',
      agent: 'Email Worker',
      progress: 100,
      started: '1 hour ago'
    },
    {
      id: '3',
      title: 'Generate performance report',
      status: 'queued',
      agent: 'Analytics Agent',
      progress: 0,
      started: 'Pending'
    },
    {
      id: '4',
      title: 'Deploy application update',
      status: 'failed',
      agent: 'Deployment Worker',
      progress: 30,
      started: '2 hours ago'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'primary';
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'queued':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <PlayIcon />;
      case 'completed':
        return <CheckCircleIcon />;
      case 'failed':
        return <ErrorIcon />;
      case 'queued':
        return <ScheduleIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  return (
    <>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Task Execution Monitor
        </Typography>
      </Grid>

      {tasks.map((task) => (
        <Grid item xs={12} md={6} key={task.id}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Typography variant="h6" sx={{ flexGrow: 1, mr: 1 }}>
                  {task.title}
                </Typography>
                <Chip
                  label={task.status}
                  color={getStatusColor(task.status) as any}
                  size="small"
                  icon={getStatusIcon(task.status)}
                />
              </Box>

              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Agent: {task.agent}
              </Typography>

              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Started: {task.started}
              </Typography>

              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Button
                  size="small"
                  variant="outlined"
                  disabled={task.status === 'completed'}
                >
                  View Details
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  color="error"
                  disabled={task.status === 'completed'}
                >
                  Stop Task
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}

      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Task Queue
          </Typography>
          <List>
            <ListItem>
              <ListItemText
                primary="Analyze user engagement metrics"
                secondary="Queued - Analytics Agent"
              />
              <ListItemSecondaryAction>
                <Chip label="Queued" color="warning" size="small" />
              </ListItemSecondaryAction>
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Update social media posts"
                secondary="Queued - Marketing Agent"
              />
              <ListItemSecondaryAction>
                <Chip label="Queued" color="warning" size="small" />
              </ListItemSecondaryAction>
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Backup database"
                secondary="Queued - Deployment Worker"
              />
              <ListItemSecondaryAction>
                <Chip label="Queued" color="warning" size="small" />
              </ListItemSecondaryAction>
            </ListItem>
          </List>
        </Paper>
      </Grid>
    </>
  );
};

export default TasksPanel;