import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Alert,
} from '@mui/material';
import {
  CheckCircle as ApproveIcon,
  Cancel as RejectIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';

const ApprovalsPanel: React.FC = () => {
  const approvals = [
    {
      id: '1',
      title: 'Deploy to production environment',
      description: 'Automated deployment of version 2.1.4 to production servers',
      type: 'deployment',
      risk: 'high',
      requestedBy: 'Deployment Worker',
      requestedAt: '15 min ago',
      deadline: '2 hours'
    },
    {
      id: '2',
      title: 'Access sensitive customer data',
      description: 'Research agent requesting access to customer analytics database',
      type: 'data_access',
      risk: 'medium',
      requestedBy: 'Research Agent',
      requestedAt: '1 hour ago',
      deadline: '24 hours'
    },
    {
      id: '3',
      title: 'Execute high-value transaction',
      description: 'Automated payment processing for marketing campaign budget',
      type: 'financial',
      risk: 'critical',
      requestedBy: 'Marketing Agent',
      requestedAt: '2 hours ago',
      deadline: '6 hours'
    }
  ];

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low':
        return 'success';
      case 'medium':
        return 'warning';
      case 'high':
        return 'error';
      case 'critical':
        return 'error';
      default:
        return 'default';
    }
  };

  const handleApprove = (id: string) => {
    console.log('Approved:', id);
  };

  const handleReject = (id: string) => {
    console.log('Rejected:', id);
  };

  return (
    <>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Approval Requests
        </Typography>
        <Alert severity="info" sx={{ mb: 3 }}>
          <Typography variant="body2">
            {approvals.length} approval requests require your attention
          </Typography>
        </Alert>
      </Grid>

      {approvals.map((approval) => (
        <Grid item xs={12} key={approval.id}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" sx={{ mb: 1 }}>
                    {approval.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {approval.description}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                    <Chip
                      label={approval.type.replace('_', ' ')}
                      variant="outlined"
                      size="small"
                    />
                    <Chip
                      label={`${approval.risk} risk`}
                      color={getRiskColor(approval.risk) as any}
                      size="small"
                    />
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    Requested by {approval.requestedBy} • {approval.requestedAt} • Deadline: {approval.deadline}
                  </Typography>
                </Box>
                <SecurityIcon sx={{ color: 'warning.main', fontSize: 40, opacity: 0.7 }} />
              </Box>

              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="contained"
                  color="success"
                  startIcon={<ApproveIcon />}
                  onClick={() => handleApprove(approval.id)}
                >
                  Approve
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<RejectIcon />}
                  onClick={() => handleReject(approval.id)}
                >
                  Reject
                </Button>
                <Button variant="outlined">
                  Review Details
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}

      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Approval History
          </Typography>
          <List>
            <ListItem>
              <ListItemText
                primary="Content publishing approval"
                secondary="Approved by admin • 2 hours ago"
              />
              <ListItemSecondaryAction>
                <Chip label="Approved" color="success" size="small" />
              </ListItemSecondaryAction>
            </ListItem>
            <ListItem>
              <ListItemText
                primary="API rate limit increase"
                secondary="Rejected by admin • 1 day ago"
              />
              <ListItemSecondaryAction>
                <Chip label="Rejected" color="error" size="small" />
              </ListItemSecondaryAction>
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Database schema change"
                secondary="Approved by admin • 2 days ago"
              />
              <ListItemSecondaryAction>
                <Chip label="Approved" color="success" size="small" />
              </ListItemSecondaryAction>
            </ListItem>
          </List>
        </Paper>
      </Grid>
    </>
  );
};

export default ApprovalsPanel;