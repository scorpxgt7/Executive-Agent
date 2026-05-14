import React, { useState } from 'react';
import {
  Grid,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  IconButton,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  CheckCircle as CheckCircleIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';

interface Goal {
  id: string;
  title: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed' | 'failed';
  progress: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
  createdAt: string;
  deadline?: string;
  objectives: string[];
}

const GoalsPanel: React.FC = () => {
  const [goals, setGoals] = useState<Goal[]>([
    {
      id: '1',
      title: 'Increase Website Traffic',
      description: 'Grow organic traffic by 50% through content marketing and SEO',
      status: 'active',
      progress: 65,
      priority: 'high',
      createdAt: '2024-01-15',
      deadline: '2024-03-15',
      objectives: [
        'Create 20 blog posts',
        'Optimize SEO performance',
        'Build backlink profile',
        'Improve social media presence'
      ]
    },
    {
      id: '2',
      title: 'Launch Mobile App',
      description: 'Develop and launch iOS and Android mobile applications',
      status: 'active',
      progress: 30,
      priority: 'critical',
      createdAt: '2024-01-20',
      deadline: '2024-06-01',
      objectives: [
        'Design app wireframes',
        'Develop iOS app',
        'Develop Android app',
        'Setup app store accounts'
      ]
    },
    {
      id: '3',
      title: 'Optimize Conversion Rate',
      description: 'Improve website conversion rate from 2% to 5%',
      status: 'paused',
      progress: 15,
      priority: 'medium',
      createdAt: '2024-01-10',
      objectives: [
        'A/B test landing pages',
        'Improve call-to-action buttons',
        'Reduce form friction',
        'Implement conversion tracking'
      ]
    }
  ]);

  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newGoal, setNewGoal] = useState<{
    title: string;
    description: string;
    priority: Goal['priority'];
    deadline: string;
    objectives: string[];
  }>({
    title: '',
    description: '',
    priority: 'medium',
    deadline: '',
    objectives: ['']
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'paused':
        return 'warning';
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'draft':
        return 'default';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'default';
      default:
        return 'default';
    }
  };

  const handleCreateGoal = () => {
    const goal: Goal = {
      id: Date.now().toString(),
      title: newGoal.title,
      description: newGoal.description,
      status: 'draft',
      progress: 0,
      priority: newGoal.priority,
      createdAt: new Date().toISOString().split('T')[0],
      deadline: newGoal.deadline,
      objectives: newGoal.objectives.filter(obj => obj.trim() !== '')
    };

    setGoals([...goals, goal]);
    setCreateDialogOpen(false);
    setNewGoal({
      title: '',
      description: '',
      priority: 'medium',
      deadline: '',
      objectives: ['']
    });
  };

  const handleStatusChange = (goalId: string, newStatus: Goal['status']) => {
    setGoals(goals.map(goal =>
      goal.id === goalId ? { ...goal, status: newStatus } : goal
    ));
  };

  const handleDeleteGoal = (goalId: string) => {
    setGoals(goals.filter(goal => goal.id !== goalId));
  };

  const addObjective = () => {
    setNewGoal({
      ...newGoal,
      objectives: [...newGoal.objectives, '']
    });
  };

  const updateObjective = (index: number, value: string) => {
    const updatedObjectives = [...newGoal.objectives];
    updatedObjectives[index] = value;
    setNewGoal({
      ...newGoal,
      objectives: updatedObjectives
    });
  };

  return (
    <>
      <Grid item xs={12}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">Goals Management</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
            sx={{ bgcolor: 'primary.main' }}
          >
            Create Goal
          </Button>
        </Box>
      </Grid>

      {goals.map((goal) => (
        <Grid item xs={12} md={6} lg={4} key={goal.id}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Typography variant="h6" sx={{ flexGrow: 1, mr: 1 }}>
                  {goal.title}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip
                    label={goal.status}
                    color={getStatusColor(goal.status) as any}
                    size="small"
                  />
                  <Chip
                    label={goal.priority}
                    color={getPriorityColor(goal.priority) as any}
                    size="small"
                    variant="outlined"
                  />
                </Box>
              </Box>

              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {goal.description}
              </Typography>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Progress</Typography>
                  <Typography variant="body2">{goal.progress}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={goal.progress}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Typography variant="body2" sx={{ mb: 1, fontWeight: 'bold' }}>
                Objectives:
              </Typography>
              <List dense>
                {goal.objectives.slice(0, 3).map((objective, index) => (
                  <ListItem key={index} sx={{ px: 0, py: 0.5 }}>
                    <ListItemText
                      primary={objective}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                ))}
                {goal.objectives.length > 3 && (
                  <ListItem sx={{ px: 0, py: 0.5 }}>
                    <ListItemText
                      primary={`+${goal.objectives.length - 3} more objectives`}
                      primaryTypographyProps={{ variant: 'body2', color: 'text.secondary' }}
                    />
                  </ListItem>
                )}
              </List>

              {goal.deadline && (
                <Typography variant="caption" color="text.secondary">
                  Deadline: {goal.deadline}
                </Typography>
              )}
            </CardContent>

            <Box sx={{ p: 2, pt: 0 }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                {goal.status === 'active' && (
                  <Button
                    size="small"
                    startIcon={<PauseIcon />}
                    onClick={() => handleStatusChange(goal.id, 'paused')}
                  >
                    Pause
                  </Button>
                )}
                {goal.status === 'paused' && (
                  <Button
                    size="small"
                    startIcon={<PlayIcon />}
                    onClick={() => handleStatusChange(goal.id, 'active')}
                  >
                    Resume
                  </Button>
                )}
                {goal.status !== 'completed' && (
                  <Button
                    size="small"
                    startIcon={<CheckCircleIcon />}
                    onClick={() => handleStatusChange(goal.id, 'completed')}
                  >
                    Complete
                  </Button>
                )}
                <IconButton
                  size="small"
                  onClick={() => handleDeleteGoal(goal.id)}
                  sx={{ ml: 'auto' }}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            </Box>
          </Card>
        </Grid>
      ))}

      {/* Create Goal Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Goal</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Goal Title"
            fullWidth
            variant="outlined"
            value={newGoal.title}
            onChange={(e) => setNewGoal({ ...newGoal, title: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={newGoal.description}
            onChange={(e) => setNewGoal({ ...newGoal, description: e.target.value })}
            sx={{ mb: 2 }}
          />
          <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
            <FormControl sx={{ minWidth: 120 }}>
              <InputLabel>Priority</InputLabel>
              <Select
                value={newGoal.priority}
                label="Priority"
                onChange={(e) => setNewGoal({ ...newGoal, priority: e.target.value as Goal['priority'] })}
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="critical">Critical</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Deadline"
              type="date"
              value={newGoal.deadline}
              onChange={(e) => setNewGoal({ ...newGoal, deadline: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Box>
          <Typography variant="h6" sx={{ mb: 1 }}>Objectives</Typography>
          {newGoal.objectives.map((objective, index) => (
            <TextField
              key={index}
              margin="dense"
              label={`Objective ${index + 1}`}
              fullWidth
              variant="outlined"
              value={objective}
              onChange={(e) => updateObjective(index, e.target.value)}
              sx={{ mb: 1 }}
            />
          ))}
          <Button onClick={addObjective} sx={{ mt: 1 }}>
            Add Objective
          </Button>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateGoal} variant="contained">Create Goal</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default GoalsPanel;