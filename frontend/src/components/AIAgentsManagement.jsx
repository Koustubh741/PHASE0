import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  Typography,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  AlertTitle,
  Tabs,
  Tab,
  Box,
  Grid,
  Paper,
  Switch,
  FormControlLabel,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Refresh,
  CheckCircle,
  Error,
  Warning,
  Info,
  Security,
  Assessment,
  Policy,
  AccountTree
} from '@mui/icons-material';
import { aiAgentsService } from '../services/aiAgentsService';
import LoadingSpinner from './Common/LoadingSpinner';
import ErrorBoundary from './Common/ErrorBoundary';

const AIAgentsManagement = () => {
  // State management
  const [agentsStatus, setAgentsStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState({});
  const [activeTab, setActiveTab] = useState(0);
  const [agentActivity, setAgentActivity] = useState([]);
  const [autoRefresh, setAutoRefresh] = useState(true);
  
  // Form states
  const [riskAssessment, setRiskAssessment] = useState({
    businessUnit: '',
    riskScope: '',
    industryType: '',
    context: ''
  });

  // Load agents status on component mount
  useEffect(() => {
    loadAgentsStatus();
  }, []);

  // Auto-refresh functionality
  useEffect(() => {
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        loadAgentsStatus();
        updateAgentActivity();
      }, 5000); // Refresh every 5 seconds
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const loadAgentsStatus = async () => {
    try {
      setLoading(true);
      const status = await aiAgentsService.getAgentsStatus();
      setAgentsStatus(status);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateAgentActivity = () => {
    const now = new Date();
    const newActivity = {
      id: Date.now(),
      timestamp: now.toLocaleTimeString(),
      message: `System check at ${now.toLocaleTimeString()}`,
      type: 'info'
    };
    
    setAgentActivity(prev => [newActivity, ...prev.slice(0, 9)]); // Keep last 10 activities
  };

  const getAgentIcon = (agentType) => {
    const icons = {
      'bfsi': <Security />,
      'telecom': <Assessment />,
      'manufacturing': <AccountTree />,
      'healthcare': <Policy />,
      'risk_agent': <Assessment />,
      'document_agent': <Policy />,
      'communication_agent': <AccountTree />,
      'compliance_agent': <Security />
    };
    return icons[agentType] || <Info />;
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'ready':
      case 'healthy':
        return <CheckCircle color="success" />;
      case 'error':
        return <Error color="error" />;
      case 'loading':
        return <Warning color="warning" />;
      default:
        return <Info color="info" />;
    }
  };

  const handleRiskAssessment = async () => {
    try {
      setLoading(true);
      
      // Add activity log
      const activity = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        message: `Starting risk assessment for ${riskAssessment.businessUnit}`,
        type: 'info'
      };
      setAgentActivity(prev => [activity, ...prev.slice(0, 9)]);
      
      const result = await aiAgentsService.assessRisk(riskAssessment);
      setResults(prev => ({ ...prev, riskAssessment: result }));
      
      // Add success activity
      const successActivity = {
        id: Date.now() + 1,
        timestamp: new Date().toLocaleTimeString(),
        message: `Risk assessment completed for ${riskAssessment.businessUnit}`,
        type: 'success'
      };
      setAgentActivity(prev => [successActivity, ...prev.slice(0, 9)]);
      
      setError(null);
    } catch (err) {
      setError(err.message);
      
      // Add error activity
      const errorActivity = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        message: `Risk assessment failed: ${err.message}`,
        type: 'error'
      };
      setAgentActivity(prev => [errorActivity, ...prev.slice(0, 9)]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const colors = {
      ready: 'success',
      healthy: 'success',
      error: 'error',
      loading: 'warning'
    };
    return <Chip label={status} color={colors[status] || 'default'} size="small" />;
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  if (loading && !agentsStatus) {
    return <LoadingSpinner />;
  }

  return (
    <ErrorBoundary>
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
            AI Agents Management
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                  color="primary"
                />
              }
              label="Auto Refresh"
            />
            <Tooltip title="Refresh Status">
              <IconButton onClick={loadAgentsStatus} color="primary">
                <Refresh />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            <AlertTitle>Error</AlertTitle>
            {error}
          </Alert>
        )}

        {/* Agents Status */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardHeader>
                <Typography variant="h6" component="h2">AI Agents Status</Typography>
              </CardHeader>
              <CardContent>
                {agentsStatus ? (
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'medium' }}>Industry Agents</Typography>
                      <List dense>
                        {Object.entries(agentsStatus.industry_agents || {}).map(([industry, agent]) => (
                          <ListItem key={industry} sx={{ border: 1, borderColor: 'divider', borderRadius: 1, mb: 1 }}>
                            <ListItemIcon>
                              <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                                {getAgentIcon(industry)}
                              </Avatar>
                            </ListItemIcon>
                            <ListItemText
                              primary={industry.toUpperCase()}
                              secondary={agent.name}
                            />
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              {getStatusIcon(agent.status)}
                              {getStatusBadge(agent.status)}
                            </Box>
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'medium' }}>Specialized Agents</Typography>
                      <List dense>
                        {Object.entries(agentsStatus.specialized_agents || {}).map(([agent, info]) => (
                          <ListItem key={agent} sx={{ border: 1, borderColor: 'divider', borderRadius: 1, mb: 1 }}>
                            <ListItemIcon>
                              <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
                                {getAgentIcon(agent)}
                              </Avatar>
                            </ListItemIcon>
                            <ListItemText
                              primary={agent.replace('_', ' ').toUpperCase()}
                              secondary={info.name}
                            />
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              {getStatusIcon(info.status)}
                              {getStatusBadge(info.status)}
                            </Box>
                          </ListItem>
                        ))}
                      </List>
                    </Grid>
                  </Grid>
                ) : (
                  <Typography>No agents status available</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          
          {/* Agent Activity Log */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader>
                <Typography variant="h6" component="h2">Agent Activity</Typography>
              </CardHeader>
              <CardContent>
                <List dense sx={{ maxHeight: 400, overflow: 'auto' }}>
                  {agentActivity.length > 0 ? (
                    agentActivity.map((activity) => (
                      <ListItem key={activity.id} sx={{ py: 0.5 }}>
                        <ListItemIcon>
                          {activity.type === 'success' && <CheckCircle color="success" />}
                          {activity.type === 'error' && <Error color="error" />}
                          {activity.type === 'info' && <Info color="info" />}
                        </ListItemIcon>
                        <ListItemText
                          primary={activity.message}
                          secondary={activity.timestamp}
                          primaryTypographyProps={{ fontSize: '0.875rem' }}
                          secondaryTypographyProps={{ fontSize: '0.75rem' }}
                        />
                      </ListItem>
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No recent activity
                    </Typography>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Loading Indicator */}
        {loading && (
          <Box sx={{ mb: 2 }}>
            <LinearProgress />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              AI Agents are working...
            </Typography>
          </Box>
        )}

        {/* AI Operations */}
        <Box sx={{ width: '100%' }}>
          <Tabs value={activeTab} onChange={handleTabChange} sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tab label="Risk Assessment" />
            <Tab label="Compliance Check" />
            <Tab label="Policy Review" />
            <Tab label="Cross-Domain Analysis" />
          </Tabs>

          {/* Risk Assessment Tab */}
          {activeTab === 0 && (
            <Card>
              <CardHeader>
                <Typography variant="h6" component="h2">Risk Assessment</Typography>
              </CardHeader>
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Business Unit"
                      value={riskAssessment.businessUnit}
                      onChange={(e) => setRiskAssessment(prev => ({ ...prev, businessUnit: e.target.value }))}
                      placeholder="Enter business unit"
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Risk Scope"
                      value={riskAssessment.riskScope}
                      onChange={(e) => setRiskAssessment(prev => ({ ...prev, riskScope: e.target.value }))}
                      placeholder="Enter risk scope"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <FormControl fullWidth>
                      <InputLabel>Industry Type</InputLabel>
                      <Select
                        value={riskAssessment.industryType}
                        onChange={(e) => setRiskAssessment(prev => ({ ...prev, industryType: e.target.value }))}
                        label="Industry Type"
                      >
                        {aiAgentsService.getAvailableIndustries().map(industry => (
                          <MenuItem key={industry.value} value={industry.value}>
                            {industry.label}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      label="Context (JSON)"
                      value={riskAssessment.context}
                      onChange={(e) => setRiskAssessment(prev => ({ ...prev, context: e.target.value }))}
                      placeholder="Enter additional context as JSON"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Button 
                      onClick={handleRiskAssessment} 
                      disabled={loading}
                      variant="contained"
                      size="large"
                    >
                      {loading ? 'Assessing...' : 'Assess Risk'}
                    </Button>
                  </Grid>
                </Grid>
                
                {results.riskAssessment && (
                  <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>Risk Assessment Result:</Typography>
                    <Paper sx={{ p: 2, bgcolor: 'white' }}>
                      <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                        {JSON.stringify(results.riskAssessment, null, 2)}
                      </pre>
                    </Paper>
                  </Box>
                )}
              </CardContent>
            </Card>
          )}

          {/* Other tabs placeholder */}
          {activeTab === 1 && (
            <Card>
              <CardContent>
                <Typography variant="h6">Compliance Check</Typography>
                <Typography color="text.secondary">This feature will be implemented soon.</Typography>
              </CardContent>
            </Card>
          )}

          {activeTab === 2 && (
            <Card>
              <CardContent>
                <Typography variant="h6">Policy Review</Typography>
                <Typography color="text.secondary">This feature will be implemented soon.</Typography>
              </CardContent>
            </Card>
          )}

          {activeTab === 3 && (
            <Card>
              <CardContent>
                <Typography variant="h6">Cross-Domain Analysis</Typography>
                <Typography color="text.secondary">This feature will be implemented soon.</Typography>
              </CardContent>
            </Card>
          )}
        </Box>
      </Box>
    </ErrorBoundary>
  );
};

export default AIAgentsManagement; 