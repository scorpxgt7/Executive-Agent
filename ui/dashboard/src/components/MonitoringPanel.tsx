import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Error as ErrorIcon,
  CheckCircle as SuccessIcon,
} from '@mui/icons-material';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

const MonitoringPanel: React.FC = () => {
  const systemMetrics = [
    { time: '00:00', cpu: 45, memory: 62, network: 120, disk: 45 },
    { time: '04:00', cpu: 32, memory: 58, network: 95, disk: 48 },
    { time: '08:00', cpu: 78, memory: 75, network: 180, disk: 52 },
    { time: '12:00', cpu: 65, memory: 68, network: 150, disk: 55 },
    { time: '16:00', cpu: 52, memory: 64, network: 130, disk: 50 },
    { time: '20:00', cpu: 38, memory: 60, network: 110, disk: 47 },
  ];

  const services = [
    { name: 'Orchestrator', status: 'healthy', uptime: '99.9%', responseTime: '45ms' },
    { name: 'API Gateway', status: 'healthy', uptime: '99.8%', responseTime: '32ms' },
    { name: 'Database', status: 'healthy', uptime: '99.9%', responseTime: '12ms' },
    { name: 'Cache (Redis)', status: 'healthy', uptime: '99.7%', responseTime: '5ms' },
    { name: 'Message Queue', status: 'warning', uptime: '98.5%', responseTime: '89ms' },
    { name: 'Browser Worker', status: 'healthy', uptime: '97.2%', responseTime: '2.1s' },
  ];

  const alerts = [
    { level: 'warning', message: 'High memory usage on worker node', time: '5 min ago' },
    { level: 'info', message: 'Scheduled maintenance completed', time: '1 hour ago' },
    { level: 'error', message: 'Failed login attempts detected', time: '2 hours ago' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'warning':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'error';
      case 'warning':
        return 'warning';
      case 'info':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          System Monitoring
        </Typography>
      </Grid>

      {/* System Metrics */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            System Performance (24h)
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={systemMetrics}>
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
              <Area
                type="monotone"
                dataKey="cpu"
                stackId="1"
                stroke="#00ff88"
                fill="#00ff88"
                fillOpacity={0.6}
                name="CPU %"
              />
              <Area
                type="monotone"
                dataKey="memory"
                stackId="2"
                stroke="#ff4081"
                fill="#ff4081"
                fillOpacity={0.6}
                name="Memory %"
              />
            </AreaChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* Service Health */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Service Health
          </Typography>
          <List>
            {services.map((service) => (
              <ListItem key={service.name}>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {service.status === 'healthy' ? (
                        <SuccessIcon sx={{ color: 'success.main' }} />
                      ) : service.status === 'warning' ? (
                        <ErrorIcon sx={{ color: 'warning.main' }} />
                      ) : (
                        <ErrorIcon sx={{ color: 'error.main' }} />
                      )}
                      <Typography variant="body1">{service.name}</Typography>
                    </Box>
                  }
                  secondary={`Uptime: ${service.uptime} • Response: ${service.responseTime}`}
                />
                <ListItemSecondaryAction>
                  <Chip
                    label={service.status}
                    color={getStatusColor(service.status) as any}
                    size="small"
                  />
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      </Grid>

      {/* Resource Usage */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Resource Usage
          </Typography>
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">CPU Usage</Typography>
              <Typography variant="body2">65%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={65} sx={{ height: 8, borderRadius: 4 }} />
          </Box>

          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Memory Usage</Typography>
              <Typography variant="body2">72%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={72} color="secondary" sx={{ height: 8, borderRadius: 4 }} />
          </Box>

          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Disk Usage</Typography>
              <Typography variant="body2">45%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={45} color="success" sx={{ height: 8, borderRadius: 4 }} />
          </Box>

          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Network I/O</Typography>
              <Typography variant="body2">120 Mbps</Typography>
            </Box>
            <LinearProgress variant="determinate" value={60} color="warning" sx={{ height: 8, borderRadius: 4 }} />
          </Box>
        </Paper>
      </Grid>

      {/* Alerts */}
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            System Alerts
          </Typography>
          <List>
            {alerts.map((alert, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={alert.message}
                  secondary={alert.time}
                />
                <ListItemSecondaryAction>
                  <Chip
                    label={alert.level}
                    color={getAlertColor(alert.level) as any}
                    size="small"
                  />
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      </Grid>
    </>
  );
};

export default MonitoringPanel;