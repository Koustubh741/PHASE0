import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Chip,
  Button,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  Description as Policy,
  Security,
  Assignment as Compliance,
  AccountTree as Workflow,
  Refresh
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const Dashboard = ({ apiCall, onSuccess, loading }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    try {
      setRefreshing(true);
      setError(null);
      
      const data = await apiCall('/grc/dashboard');
      setDashboardData(data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Handle refresh
  const handleRefresh = () => {
    fetchDashboardData();
  };

  // Mock data for charts (replace with real data)
  const riskTrendData = [
    { month: 'Jan', risks: 12, resolved: 8 },
    { month: 'Feb', risks: 15, resolved: 10 },
    { month: 'Mar', risks: 18, resolved: 12 },
    { month: 'Apr', risks: 14, resolved: 11 },
    { month: 'May', risks: 16, resolved: 13 },
    { month: 'Jun', risks: 13, resolved: 9 },
  ];

  const complianceData = [
    { name: 'Compliant', value: 75, color: '#4caf50' },
    { name: 'Non-Compliant', value: 15, color: '#f44336' },
    { name: 'In Progress', value: 10, color: '#ff9800' },
  ];

  const policyStatusData = [
    { name: 'Active', value: 45, color: '#2196f3' },
    { name: 'Under Review', value: 12, color: '#ff9800' },
    { name: 'Draft', value: 8, color: '#9e9e9e' },
    { name: 'Archived', value: 5, color: '#607d8b' },
  ];

  if (loading && !dashboardData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          GRC Dashboard
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
          disabled={refreshing}
        >
          {refreshing ? 'Refreshing...' : 'Refresh'}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Key Metrics */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Policies
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.services?.policies?.total_policies || 0}
                  </Typography>
                </Box>
                <Policy color="primary" sx={{ fontSize: 40 }} />
              </Box>
              <Box mt={2}>
                <Chip
                  label={`${dashboardData?.services?.policies?.policies_by_status?.PUBLISHED || 0} Active`}
                  color="success"
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Risks
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.services?.risks?.total_risks || 0}
                  </Typography>
                </Box>
                <Security color="warning" sx={{ fontSize: 40 }} />
              </Box>
              <Box mt={2}>
                <Chip
                  label={`${dashboardData?.services?.risks?.high_risks || 0} High Risk`}
                  color="error"
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Compliance Score
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.services?.compliance?.average_compliance_score || 0}%
                  </Typography>
                </Box>
                <Compliance color="success" sx={{ fontSize: 40 }} />
              </Box>
              <Box mt={2}>
                <LinearProgress
                  variant="determinate"
                  value={dashboardData?.services?.compliance?.average_compliance_score || 0}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Active Workflows
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.services?.workflows?.total_workflows || 0}
                  </Typography>
                </Box>
                <Workflow color="info" sx={{ fontSize: 40 }} />
              </Box>
              <Box mt={2}>
                <Chip
                  label={`${dashboardData?.services?.workflows?.my_pending_assignments || 0} Pending`}
                  color="warning"
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} mb={3}>
        {/* Risk Trends */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Risk Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={riskTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="risks"
                    stackId="1"
                    stroke="#f44336"
                    fill="#f44336"
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="resolved"
                    stackId="1"
                    stroke="#4caf50"
                    fill="#4caf50"
                    fillOpacity={0.6}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Compliance Status */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Compliance Status
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={complianceData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {complianceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box mt={2}>
                {complianceData.map((item) => (
                  <Box key={item.name} display="flex" alignItems="center" mb={1}>
                    <Box
                      width={16}
                      height={16}
                      bgcolor={item.color}
                      borderRadius="50%"
                      mr={1}
                    />
                    <Typography variant="body2">
                      {item.name}: {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activity and Alerts */}
      <Grid container spacing={3}>
        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Policy 'Data Protection' approved"
                    secondary="2 hours ago"
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemIcon>
                    <Warning color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="High risk identified in IT Operations"
                    secondary="4 hours ago"
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemIcon>
                    <Compliance color="info" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Compliance assessment completed"
                    secondary="1 day ago"
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemIcon>
                    <Workflow color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="New workflow 'Vendor Assessment' started"
                    secondary="2 days ago"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Agent Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                AI Agent Status
              </Typography>
              {dashboardData?.services?.ai_agents ? (
                <Box>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Platform Status: {dashboardData.services.ai_agents.platform_status}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Total Documents: {dashboardData.services.ai_agents.total_documents}
                  </Typography>
                  <Box mt={2}>
                    <Typography variant="subtitle2" gutterBottom>
                      Active Agents:
                    </Typography>
                    {Object.entries(dashboardData.services.ai_agents.agents || {}).map(([agentId, agent]) => (
                      <Box key={agentId} display="flex" alignItems="center" mb={1}>
                        <Chip
                          label={agentId.replace('_', ' ').toUpperCase()}
                          color={agent.status === 'active' ? 'success' : 'default'}
                          size="small"
                          sx={{ mr: 1 }}
                        />
                        <Typography variant="body2" color="textSecondary">
                          {agent.type}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  AI agents status not available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
