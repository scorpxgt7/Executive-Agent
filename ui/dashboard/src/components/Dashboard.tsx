import React, { useState, useEffect } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Grid,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  PlayArrow as PlayIcon,
  Schedule as ScheduleIcon,
  Assessment as AssessmentIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { io } from 'socket.io-client';
import OverviewPanel from './OverviewPanel';
import GoalsPanel from './GoalsPanel';
import AgentsPanel from './AgentsPanel';
import TasksPanel from './TasksPanel';
import ApprovalsPanel from './ApprovalsPanel';
import MonitoringPanel from './MonitoringPanel';

const drawerWidth = 280;

interface SystemStatus {
  status: 'online' | 'offline' | 'degraded';
  uptime: number;
  activeGoals: number;
  activeTasks: number;
  activeAgents: number;
  pendingApprovals: number;
}

const Dashboard: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [activeView, setActiveView] = useState('overview');
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    status: 'online',
    uptime: 0,
    activeGoals: 0,
    activeTasks: 0,
    activeAgents: 0,
    pendingApprovals: 0,
  });

  useEffect(() => {
    // Initialize WebSocket connection
    const socket = io('http://localhost:8000');

    socket.on('system_status', (data: SystemStatus) => {
      setSystemStatus(data);
    });

    socket.on('goal_update', (data: unknown) => {
      console.log('Goal update:', data);
    });

    socket.on('task_update', (data: unknown) => {
      console.log('Task update:', data);
    });

    return () => {
      socket.close();
    };
  }, []);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const menuItems = [
    { id: 'overview', label: 'Overview', icon: <DashboardIcon /> },
    { id: 'goals', label: 'Goals', icon: <PlayIcon /> },
    { id: 'agents', label: 'Agents', icon: <AssessmentIcon /> },
    { id: 'tasks', label: 'Tasks', icon: <ScheduleIcon /> },
    { id: 'approvals', label: 'Approvals', icon: <SecurityIcon /> },
    { id: 'monitoring', label: 'Monitoring', icon: <AssessmentIcon /> },
  ];

  const renderContent = () => {
    switch (activeView) {
      case 'overview':
        return <OverviewPanel systemStatus={systemStatus} />;
      case 'goals':
        return <GoalsPanel />;
      case 'agents':
        return <AgentsPanel />;
      case 'tasks':
        return <TasksPanel />;
      case 'approvals':
        return <ApprovalsPanel />;
      case 'monitoring':
        return <MonitoringPanel />;
      default:
        return <OverviewPanel systemStatus={systemStatus} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'success';
      case 'degraded':
        return 'warning';
      case 'offline':
        return 'error';
      default:
        return 'default';
    }
  };

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div" sx={{ color: 'primary.main' }}>
          Executive Agent
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.id} disablePadding>
            <ListItemButton
              selected={activeView === item.id}
              onClick={() => setActiveView(item.id)}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: 'rgba(0, 255, 136, 0.1)',
                  '&:hover': {
                    backgroundColor: 'rgba(0, 255, 136, 0.2)',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ color: activeView === item.id ? 'primary.main' : 'inherit' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <Box sx={{ p: 2 }}>
        <Typography variant="subtitle2" gutterBottom>
          System Status
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Chip
            label={systemStatus.status.toUpperCase()}
            color={getStatusColor(systemStatus.status) as any}
            size="small"
            sx={{ mr: 1 }}
          />
          <Typography variant="caption">
            {Math.floor(systemStatus.uptime / 3600)}h uptime
          </Typography>
        </Box>
        <LinearProgress
          variant="determinate"
          value={75}
          sx={{ height: 4, borderRadius: 2 }}
        />
      </Box>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: 'background.paper',
          color: 'text.primary',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Autonomous Operations Dashboard
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip
              label={`${systemStatus.activeTasks} Active Tasks`}
              variant="outlined"
              size="small"
            />
            <Chip
              label={`${systemStatus.pendingApprovals} Pending Approvals`}
              variant="outlined"
              size="small"
              color={systemStatus.pendingApprovals > 0 ? 'warning' : 'default'}
            />
          </Box>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="navigation menu"
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: '64px',
        }}
      >
        <Grid container spacing={3}>
          {renderContent()}
        </Grid>
      </Box>
    </Box>
  );
};

export default Dashboard;