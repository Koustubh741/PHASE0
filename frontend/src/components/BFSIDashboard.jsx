import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Alert,
  CircularProgress,
  Chip,
  Button,
  Paper,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Policy as PolicyIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { bfsiService } from '../services/bfsiService';

const BFSIDashboard = ({ apiCall, onSuccess, loading }) => {
  const [dashboardData, setDashboardData] = useState({
    agentStatus: null,
    complianceStatus: null,
    riskStatus: null,
    recentActivities: [],
    keyMetrics: {}
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Load BFSI agent status
      const agentStatus = await bfsiService.getAgentStatus();
      
      // Load BFSI industry status
      const industryStatus = await bfsiService.getBFSIStatus();

      setDashboardData({
        agentStatus,
        complianceStatus: industryStatus,
        riskStatus: null, // Will be loaded separately
        recentActivities: [
          {
            id: 1,
            type: 'compliance_check',
            description: 'Basel III compliance check completed',
            status: 'completed',
            timestamp: new Date().toISOString()
          },
          {
            id: 2,
            type: 'risk_assessment',
            description: 'Credit risk assessment in progress',
            status: 'in_progress',
            timestamp: new Date(Date.now() - 3600000).toISOString()
          },
          {
            id: 3,
            type: 'policy_update',
            description: 'AML/KYC policy updated',
            status: 'completed',
            timestamp: new Date(Date.now() - 7200000).toISOString()
          }
        ],
        keyMetrics: {
          totalOperations: agentStatus?.total_operations || 0,
          successRate: agentStatus?.success_rate || 0,
          complianceScore: industryStatus?.compliance_score || 0,
          riskScore: industryStatus?.risk_score || 0,
          uptime: agentStatus?.uptime_percentage || 0
        }
      });

    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setError(`Failed to load dashboard data: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = () => {
    loadDashboardData();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
      case 'completed':
      case 'healthy':
        return 'success';
      case 'warning':
      case 'in_progress':
        return 'warning';
      case 'error':
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
      case 'completed':
      case 'healthy':
        return <CheckCircleIcon color="success" />;
      case 'warning':
      case 'in_progress':
        return <WarningIcon color="warning" />;
      case 'error':
      case 'failed':
        return <ErrorIcon color="error" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          BFSI GRC Dashboard
        </Typography>
        <Button variant="contained" onClick={handleRefresh}>
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Key Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon color="primary" sx={{ mr: 1 }} />
                <Box>
                  <Typography variant="h6">{dashboardData.keyMetrics.totalOperations}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Operations</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                <Box>
                  <Typography variant="h6">{dashboardData.keyMetrics.successRate}%</Typography>
                  <Typography variant="body2" color="text.secondary">Success Rate</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <SecurityIcon color="info" sx={{ mr: 1 }} />
                <Box>
                  <Typography variant="h6">{dashboardData.keyMetrics.complianceScore}%</Typography>
                  <Typography variant="body2" color="text.secondary">Compliance Score</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <AssessmentIcon color="warning" sx={{ mr: 1 }} />
                <Box>
                  <Typography variant="h6">{dashboardData.keyMetrics.riskScore}%</Typography>
                  <Typography variant="body2" color="text.secondary">Risk Score</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <PolicyIcon color="primary" sx={{ mr: 1 }} />
                <Box>
                  <Typography variant="h6">{dashboardData.keyMetrics.uptime}%</Typography>
                  <Typography variant="body2" color="text.secondary">Uptime</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Agent Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                BFSI Agent Status
              </Typography>
              {dashboardData.agentStatus ? (
                <Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="body1">Agent Health</Typography>
                    <Chip 
                      label={dashboardData.agentStatus.status || 'Unknown'} 
                      color={getStatusColor(dashboardData.agentStatus.status)}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Last Activity: {new Date(dashboardData.agentStatus.last_activity || Date.now()).toLocaleString()}
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Agent ID: {dashboardData.agentStatus.agent_id || 'N/A'}
                    </Typography>
                  </Box>
                  {dashboardData.agentStatus.performance_score && (
                    <Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Performance Score: {dashboardData.agentStatus.performance_score}
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={dashboardData.agentStatus.performance_score * 100}
                        sx={{ mt: 1 }}
                      />
                    </Box>
                  )}
                </Box>
              ) : (
                <Alert severity="info">No agent status data available</Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Compliance Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Compliance Status
              </Typography>
              {dashboardData.complianceStatus ? (
                <Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="body1">Overall Compliance</Typography>
                    <Chip 
                      label={dashboardData.complianceStatus.compliance_level || 'Unknown'} 
                      color={getStatusColor(dashboardData.complianceStatus.compliance_level)}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Industry: {dashboardData.complianceStatus.industry || 'BFSI'}
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Regulations Monitored: {dashboardData.complianceStatus.regulations_count || 0}
                    </Typography>
                  </Box>
                  {dashboardData.complianceStatus.violations && (
                    <Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Active Violations: {dashboardData.complianceStatus.violations.length}
                      </Typography>
                    </Box>
                  )}
                </Box>
              ) : (
                <Alert severity="info">No compliance status data available</Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activities
              </Typography>
              {dashboardData.recentActivities.length > 0 ? (
                <List>
                  {dashboardData.recentActivities.map((activity, index) => (
                    <React.Fragment key={activity.id}>
                      <ListItem>
                        <ListItemIcon>
                          {getStatusIcon(activity.status)}
                        </ListItemIcon>
                        <ListItemText
                          primary={activity.description}
                          secondary={new Date(activity.timestamp).toLocaleString()}
                        />
                        <Chip 
                          label={activity.status.replace('_', ' ')} 
                          color={getStatusColor(activity.status)}
                          size="small"
                        />
                      </ListItem>
                      {index < dashboardData.recentActivities.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Alert severity="info">No recent activities</Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BFSIDashboard;
