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

  // Mock data for demonstration
  const complianceTrendData = [
    { month: 'Jan', compliance: 85, risks: 12, policies: 45 },
    { month: 'Feb', compliance: 88, risks: 10, policies: 48 },
    { month: 'Mar', compliance: 92, risks: 8, policies: 52 },
    { month: 'Apr', compliance: 89, risks: 9, policies: 50 },
    { month: 'May', compliance: 94, risks: 6, policies: 55 },
    { month: 'Jun', compliance: 96, risks: 4, policies: 58 }
  ];

  const riskDistributionData = [
    { name: 'High Risk', value: 15, color: '#f44336' },
    { name: 'Medium Risk', value: 35, color: '#ff9800' },
    { name: 'Low Risk', value: 50, color: '#4caf50' }
  ];

  const policyStatusData = [
    { name: 'Approved', value: 65, color: '#4caf50' },
    { name: 'Pending', value: 25, color: '#ff9800' },
    { name: 'Draft', value: 10, color: '#2196f3' }
  ];

  const workflowProgressData = [
    { name: 'Policy Approval', progress: 75, completed: 15, total: 20 },
    { name: 'Risk Assessment', progress: 60, completed: 12, total: 20 },
    { name: 'Compliance Review', progress: 90, completed: 18, total: 20 },
    { name: 'Incident Response', progress: 45, completed: 9, total: 20 }
  ];

  const kpiData = [
    {
      title: 'Overall Compliance Score',
      value: '94%',
      change: '+2.5%',
      trend: 'up',
      icon: <Assessment color="primary" />
    },
    {
      title: 'Active Risks',
      value: '23',
      change: '-15%',
      trend: 'down',
      icon: <TrendingDown color="error" />
    },
    {
      title: 'Policies Updated',
      value: '58',
      change: '+8%',
      trend: 'up',
      icon: <TrendingUp color="success" />
    },
    {
      title: 'Workflows Completed',
      value: '42',
      change: '+12%',
      trend: 'up',
      icon: <TrendingUp color="info" />
    }
  ];

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
