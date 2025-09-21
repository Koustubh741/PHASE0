import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import {
  Analytics as AnalyticsIcon,
  TrendingUp,
  TrendingDown,
  Assessment
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const Analytics = ({ apiCall, onSuccess, loading }) => {
  const [timeRange, setTimeRange] = useState('30d');
  const [selectedMetric, setSelectedMetric] = useState('all');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Chart data state (will be populated from API)
  const [complianceTrendData, setComplianceTrendData] = useState([]);
  const [riskDistributionData, setRiskDistributionData] = useState([]);
  const [policyStatusData, setPolicyStatusData] = useState([]);
  const [workflowProgressData, setWorkflowProgressData] = useState([]);
  const [kpiData, setKpiData] = useState([]);

  // Load analytics data from API
  useEffect(() => {
    loadAnalyticsData();
  }, [timeRange, selectedMetric]);

  const loadAnalyticsData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      // TODO: Replace with actual API calls
      // const complianceData = await analyticsService.getComplianceTrend(timeRange);
      // const riskData = await analyticsService.getRiskDistribution(timeRange);
      // const policyData = await analyticsService.getPolicyStatus(timeRange);
      // const workflowData = await analyticsService.getWorkflowProgress(timeRange);
      // const kpiData = await analyticsService.getKPIs(timeRange);
      
      // For now, set empty arrays until API is implemented
      setComplianceTrendData([]);
      setRiskDistributionData([]);
      setPolicyStatusData([]);
      setWorkflowProgressData([]);
      setKpiData([]);
    } catch (err) {
      console.error('Error loading analytics data:', err);
      setError('Failed to load analytics data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <AnalyticsIcon />
          Analytics & Reporting
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              label="Time Range"
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <MenuItem value="7d">Last 7 days</MenuItem>
              <MenuItem value="30d">Last 30 days</MenuItem>
              <MenuItem value="90d">Last 90 days</MenuItem>
              <MenuItem value="1y">Last year</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Metric</InputLabel>
            <Select
              value={selectedMetric}
              label="Metric"
              onChange={(e) => setSelectedMetric(e.target.value)}
            >
              <MenuItem value="all">All Metrics</MenuItem>
              <MenuItem value="compliance">Compliance</MenuItem>
              <MenuItem value="risk">Risk</MenuItem>
              <MenuItem value="policy">Policy</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {kpiData.map((kpi, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography color="textSecondary" gutterBottom variant="body2">
                      {kpi.title}
                    </Typography>
                    <Typography variant="h4" component="div">
                      {kpi.value}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color={kpi.trend === 'up' ? 'success.main' : 'error.main'}
                      sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
                    >
                      {kpi.trend === 'up' ? <TrendingUp fontSize="small" /> : <TrendingDown fontSize="small" />}
                      {kpi.change}
                    </Typography>
                  </Box>
                  <Box sx={{ color: 'primary.main' }}>
                    {kpi.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts Row 1 */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Compliance & Risk Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={complianceTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="compliance" stroke="#4caf50" strokeWidth={2} name="Compliance %" />
                  <Line type="monotone" dataKey="risks" stroke="#f44336" strokeWidth={2} name="Active Risks" />
                  <Line type="monotone" dataKey="policies" stroke="#2196f3" strokeWidth={2} name="Policies" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Risk Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={riskDistributionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {riskDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row 2 */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Policy Status Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={policyStatusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {policyStatusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Workflow Progress
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={workflowProgressData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" domain={[0, 100]} />
                  <YAxis dataKey="name" type="category" width={120} />
                  <Tooltip />
                  <Bar dataKey="progress" fill="#2196f3" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Summary Report */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Executive Summary
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2, bgcolor: 'success.light', color: 'success.contrastText' }}>
                <Typography variant="h6" gutterBottom>
                  ✅ Strengths
                </Typography>
                <Typography variant="body2">
                  • Compliance score improved by 2.5% this month<br/>
                  • 42 workflows completed successfully<br/>
                  • Risk mitigation efforts showing positive results
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2, bgcolor: 'warning.light', color: 'warning.contrastText' }}>
                <Typography variant="h6" gutterBottom>
                  ⚠️ Areas for Improvement
                </Typography>
                <Typography variant="body2">
                  • 4 high-risk items require immediate attention<br/>
                  • Policy review cycle needs acceleration<br/>
                  • Incident response workflows need optimization
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Analytics;
