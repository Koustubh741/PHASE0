import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tooltip,
  LinearProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Security as RiskIcon,
  TrendingUp as HighRiskIcon,
  TrendingFlat as MediumRiskIcon,
  TrendingDown as LowRiskIcon
} from '@mui/icons-material';

const RiskManagement = ({ apiCall, onSuccess, loading }) => {
  const [risks, setRisks] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingRisk, setEditingRisk] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    impact: 'medium',
    probability: 'medium',
    status: 'open',
    owner: '',
    mitigationPlan: ''
  });

  // Mock data for demonstration
  useEffect(() => {
    const mockRisks = [
      {
        id: 1,
        title: 'Data Breach Risk',
        description: 'Potential unauthorized access to sensitive customer data',
        category: 'Security',
        impact: 'high',
        probability: 'medium',
        status: 'open',
        owner: 'Security Team',
        mitigationPlan: 'Implement multi-factor authentication and regular security audits',
        lastUpdated: '2024-01-15',
        score: 75
      },
      {
        id: 2,
        title: 'Regulatory Compliance Risk',
        description: 'Risk of non-compliance with new GDPR regulations',
        category: 'Compliance',
        impact: 'high',
        probability: 'low',
        status: 'mitigated',
        owner: 'Compliance Team',
        mitigationPlan: 'Updated privacy policies and implemented data protection measures',
        lastUpdated: '2024-01-10',
        score: 30
      },
      {
        id: 3,
        title: 'Operational Disruption',
        description: 'Risk of system downtime affecting business operations',
        category: 'Operational',
        impact: 'medium',
        probability: 'medium',
        status: 'monitoring',
        owner: 'IT Team',
        mitigationPlan: 'Implemented backup systems and disaster recovery procedures',
        lastUpdated: '2024-01-20',
        score: 50
      }
    ];
    setRisks(mockRisks);
  }, []);

  const handleOpenDialog = (risk = null) => {
    if (risk) {
      setEditingRisk(risk);
      setFormData(risk);
    } else {
      setEditingRisk(null);
      setFormData({
        title: '',
        description: '',
        category: '',
        impact: 'medium',
        probability: 'medium',
        status: 'open',
        owner: '',
        mitigationPlan: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingRisk(null);
  };

  const handleSaveRisk = async () => {
    try {
      const riskScore = calculateRiskScore(formData.impact, formData.probability);
      const riskData = { ...formData, score: riskScore, lastUpdated: new Date().toISOString().split('T')[0] };
      
      if (editingRisk) {
        const updatedRisks = risks.map(r => 
          r.id === editingRisk.id ? { ...riskData, id: editingRisk.id } : r
        );
        setRisks(updatedRisks);
        onSuccess('Risk updated successfully');
      } else {
        const newRisk = {
          ...riskData,
          id: risks.length + 1
        };
        setRisks([...risks, newRisk]);
        onSuccess('Risk created successfully');
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving risk:', error);
    }
  };

  const handleDeleteRisk = (riskId) => {
    setRisks(risks.filter(r => r.id !== riskId));
    onSuccess('Risk deleted successfully');
  };

  const calculateRiskScore = (impact, probability) => {
    const impactScores = { low: 1, medium: 2, high: 3 };
    const probabilityScores = { low: 1, medium: 2, high: 3 };
    return impactScores[impact] * probabilityScores[probability] * 25; // Scale to 0-100
  };

  const getRiskIcon = (score) => {
    if (score >= 70) return <HighRiskIcon color="error" />;
    if (score >= 40) return <MediumRiskIcon color="warning" />;
    return <LowRiskIcon color="success" />;
  };

  const getRiskColor = (score) => {
    if (score >= 70) return 'error';
    if (score >= 40) return 'warning';
    return 'success';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open':
        return 'error';
      case 'monitoring':
        return 'warning';
      case 'mitigated':
        return 'success';
      case 'closed':
        return 'default';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <RiskIcon />
          Risk Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          sx={{ textTransform: 'none' }}
        >
          New Risk
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Risks
              </Typography>
              <Typography variant="h4">
                {risks.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                High Risk
              </Typography>
              <Typography variant="h4" color="error.main">
                {risks.filter(r => r.score >= 70).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Medium Risk
              </Typography>
              <Typography variant="h4" color="warning.main">
                {risks.filter(r => r.score >= 40 && r.score < 70).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Low Risk
              </Typography>
              <Typography variant="h4" color="success.main">
                {risks.filter(r => r.score < 40).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Risk Heat Map */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Risk Heat Map
          </Typography>
          <Grid container spacing={2}>
            {risks.map((risk) => (
              <Grid item xs={12} sm={6} md={4} key={risk.id}>
                <Card variant="outlined" sx={{ height: '100%' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="subtitle2" fontWeight={600}>
                        {risk.title}
                      </Typography>
                      {getRiskIcon(risk.score)}
                    </Box>
                    <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                      {risk.description}
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="textSecondary">
                        Risk Score: {risk.score}/100
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={risk.score} 
                        color={getRiskColor(risk.score)}
                        sx={{ mt: 0.5 }}
                      />
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Chip label={risk.category} size="small" />
                      <Chip 
                        label={risk.status} 
                        size="small" 
                        color={getStatusColor(risk.status)}
                      />
                    </Box>
                  </CardContent>
                  <CardActions>
                    <Button size="small" onClick={() => handleOpenDialog(risk)}>
                      Edit
                    </Button>
                    <Button size="small" color="error" onClick={() => handleDeleteRisk(risk.id)}>
                      Delete
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Risks Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            All Risks
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Category</TableCell>
                  <TableCell>Impact</TableCell>
                  <TableCell>Probability</TableCell>
                  <TableCell>Risk Score</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Owner</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {risks.map((risk) => (
                  <TableRow key={risk.id}>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        {risk.title}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {risk.description}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip label={risk.category} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={risk.impact} 
                        size="small" 
                        color={risk.impact === 'high' ? 'error' : risk.impact === 'medium' ? 'warning' : 'success'}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={risk.probability} 
                        size="small" 
                        color={risk.probability === 'high' ? 'error' : risk.probability === 'medium' ? 'warning' : 'success'}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getRiskIcon(risk.score)}
                        <Typography variant="body2" fontWeight={600}>
                          {risk.score}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={risk.status} 
                        size="small" 
                        color={getStatusColor(risk.status)}
                      />
                    </TableCell>
                    <TableCell>{risk.owner}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Tooltip title="View">
                          <IconButton size="small" color="primary">
                            <ViewIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit">
                          <IconButton 
                            size="small" 
                            color="primary"
                            onClick={() => handleOpenDialog(risk)}
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton 
                            size="small" 
                            color="error"
                            onClick={() => handleDeleteRisk(risk.id)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Add/Edit Risk Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingRisk ? 'Edit Risk' : 'Create New Risk'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Risk Title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={formData.category}
                  label="Category"
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                >
                  <MenuItem value="Security">Security</MenuItem>
                  <MenuItem value="Compliance">Compliance</MenuItem>
                  <MenuItem value="Operational">Operational</MenuItem>
                  <MenuItem value="Financial">Financial</MenuItem>
                  <MenuItem value="Strategic">Strategic</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Impact</InputLabel>
                <Select
                  value={formData.impact}
                  label="Impact"
                  onChange={(e) => setFormData({ ...formData, impact: e.target.value })}
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Probability</InputLabel>
                <Select
                  value={formData.probability}
                  label="Probability"
                  onChange={(e) => setFormData({ ...formData, probability: e.target.value })}
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={formData.status}
                  label="Status"
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                >
                  <MenuItem value="open">Open</MenuItem>
                  <MenuItem value="monitoring">Monitoring</MenuItem>
                  <MenuItem value="mitigated">Mitigated</MenuItem>
                  <MenuItem value="closed">Closed</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Owner"
                value={formData.owner}
                onChange={(e) => setFormData({ ...formData, owner: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Mitigation Plan"
                value={formData.mitigationPlan}
                onChange={(e) => setFormData({ ...formData, mitigationPlan: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveRisk} variant="contained">
            {editingRisk ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default RiskManagement;
