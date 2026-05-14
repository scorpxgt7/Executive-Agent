import React, { useState, useEffect } from 'react';
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
  List,
  ListItem,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  ExpandMore as ExpandMoreIcon,
  Psychology as PsychologyIcon,
} from '@mui/icons-material';
import { apiService, GoalResponse, CreateGoalRequest } from '../services/api';

const GoalsPanel: React.FC = () => {
  const [goals, setGoals] = useState<GoalResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = async () => {
    try {
      setLoading(true);
      const response = await apiService.getGoals();
      setGoals(response.goals);
      setError(null);
    } catch (err) {
      setError('Failed to fetch goals');
      console.error('Error fetching goals:', err);
    } finally {
      setLoading(false);
    }
  };

  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newGoal, setNewGoal] = useState<{
    description: string;
    objectives: string[];
    constraints: Record<string, any>;
    deadline: string;
    priority: number;
  }>({
    description: '',
    objectives: [''],
    constraints: {},
    deadline: '',
    priority: 1,
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'executing':
        return 'success';
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority: number) => {
    if (priority >= 4) return 'error';
    if (priority >= 3) return 'warning';
    if (priority >= 2) return 'info';
    return 'default';
  };

  const handleCreateGoal = async () => {
    try {
      const goalRequest: CreateGoalRequest = {
        id: `goal-${Date.now()}`,
        description: newGoal.description,
        objectives: newGoal.objectives.filter(obj => obj.trim() !== ''),
        constraints: newGoal.constraints,
        deadline: newGoal.deadline || undefined,
        priority: newGoal.priority,
      };

      await apiService.createGoal(goalRequest);
      setCreateDialogOpen(false);
      setNewGoal({
        description: '',
        objectives: [''],
        constraints: {},
        deadline: '',
        priority: 1,
      });
      // Refresh goals list
      await fetchGoals();
    } catch (err) {
      setError('Failed to create goal');
      console.error('Error creating goal:', err);
    }
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

      {loading ? (
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <Typography>Loading goals...</Typography>
          </Box>
        </Grid>
      ) : error ? (
        <Grid item xs={12}>
          <Alert severity="error">{error}</Alert>
        </Grid>
      ) : goals.length === 0 ? (
        <Grid item xs={12}>
          <Box sx={{ textAlign: 'center', p: 4 }}>
            <Typography variant="h6" color="text.secondary">
              No goals found
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Create your first goal to get started
            </Typography>
          </Box>
        </Grid>
      ) : (
        goals.map((goal) => (
          <Grid item xs={12} md={6} lg={4} key={goal.goal_id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" sx={{ flexGrow: 1, mr: 1 }}>
                    Goal {goal.goal_id}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip
                      label={goal.status}
                      color={getStatusColor(goal.status) as any}
                      size="small"
                    />
                    <Chip
                      label={`Priority ${goal.learning_insights?.priority || 'N/A'}`}
                      color={getPriorityColor(goal.learning_insights?.priority || 1) as any}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Goal ID: {goal.goal_id}
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    Tasks: {goal.task_count}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={goal.status === 'completed' ? 100 : 50} // Placeholder progress
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>

                {goal.learning_insights && (
                  <Accordion sx={{ mt: 2 }}>
                    <AccordionSummary
                      expandIcon={<ExpandMoreIcon />}
                      aria-controls={`learning-insights-${goal.goal_id}-content`}
                      id={`learning-insights-${goal.goal_id}-header`}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <PsychologyIcon color="primary" />
                        <Typography variant="body2" fontWeight="bold">
                          Learning Insights
                        </Typography>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      {goal.learning_insights.strategy_adjustments && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" fontWeight="bold" sx={{ mb: 1 }}>
                            Strategy Adjustments:
                          </Typography>
                          <List dense>
                            {goal.learning_insights.strategy_adjustments.map((adjustment: string, index: number) => (
                              <ListItem key={index} sx={{ px: 0, py: 0.5 }}>
                                <ListItemText
                                  primary={`• ${adjustment}`}
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}

                      {goal.learning_insights.risk_mitigations && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" fontWeight="bold" sx={{ mb: 1 }}>
                            Risk Mitigations:
                          </Typography>
                          <List dense>
                            {goal.learning_insights.risk_mitigations.map((mitigation: string, index: number) => (
                              <ListItem key={index} sx={{ px: 0, py: 0.5 }}>
                                <ListItemText
                                  primary={`• ${mitigation}`}
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}

                      {goal.learning_insights.performance_improvements && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" fontWeight="bold" sx={{ mb: 1 }}>
                            Performance Improvements:
                          </Typography>
                          <List dense>
                            {goal.learning_insights.performance_improvements.map((improvement: string, index: number) => (
                              <ListItem key={index} sx={{ px: 0, py: 0.5 }}>
                                <ListItemText
                                  primary={`• ${improvement}`}
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}

                      {goal.learning_insights.feedback_loops && (
                        <Box>
                          <Typography variant="body2" fontWeight="bold" sx={{ mb: 1 }}>
                            Feedback Loops:
                          </Typography>
                          <List dense>
                            {goal.learning_insights.feedback_loops.map((loop: string, index: number) => (
                              <ListItem key={index} sx={{ px: 0, py: 0.5 }}>
                                <ListItemText
                                  primary={`• ${loop}`}
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}
                    </AccordionDetails>
                  </Accordion>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))
      )}

      {/* Create Goal Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Goal</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
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
            <TextField
              label="Priority (1-5)"
              type="number"
              inputProps={{ min: 1, max: 5 }}
              value={newGoal.priority}
              onChange={(e) => setNewGoal({ ...newGoal, priority: parseInt(e.target.value) || 1 })}
              sx={{ minWidth: 120 }}
            />
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