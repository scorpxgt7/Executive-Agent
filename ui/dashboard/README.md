# Executive Agent Dashboard

A real-time monitoring and control dashboard for the Executive Agent autonomous operations platform.

## Features

- **Real-time Monitoring**: Live updates of system status, agent activities, and task execution
- **Goal Management**: Create, track, and manage operational goals with priority levels
- **Agent Oversight**: Monitor agent performance, status, and activity logs
- **Task Execution**: View task queues, execution status, and control operations
- **Approval Workflow**: Review and approve high-risk operations with governance controls
- **Performance Analytics**: Charts and metrics for system performance and efficiency

## Technology Stack

- **React 18** with TypeScript for type-safe development
- **Material-UI (MUI)** for modern, responsive UI components
- **Recharts** for data visualization and performance charts
- **Socket.io** for real-time WebSocket communication
- **Axios** for HTTP API integrations

## Getting Started

### Prerequisites

- Node.js 18 or Node.js 20 and npm
- Backend API server running (Executive Agent platform)

If you are using `nvm`, run:

```bash
nvm install 20
nvm use 20
```

### Installation

```bash
cd ui/dashboard
npm install
```

### Development

```bash
npm start
```

Runs the app in development mode on [http://localhost:3000](http://localhost:3000).

### Production Build

```bash
npm run build
```

Builds the app for production to the `build` folder.

## Project Structure

```
src/
├── components/          # React components
│   ├── Dashboard.tsx    # Main dashboard layout
│   ├── OverviewPanel.tsx # System overview
│   ├── GoalsPanel.tsx   # Goal management
│   ├── AgentsPanel.tsx  # Agent monitoring
│   ├── TasksPanel.tsx   # Task execution
│   ├── ApprovalsPanel.tsx # Approval workflow
│   └── MonitoringPanel.tsx # System monitoring
├── App.tsx             # Main app component
├── index.tsx           # App entry point
└── index.css           # Global styles
```

## API Integration

The dashboard connects to the Executive Agent backend via:
- WebSocket (Socket.io) for real-time updates
- REST API endpoints for data operations

Configure the backend URL in the environment variables or component configuration.