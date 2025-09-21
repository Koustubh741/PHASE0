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
  LinearProgress,
  Alert,
  CircularProgress
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
import { riskService } from '../services/riskService';

const RiskManagement = ({ apiCall, onSuccess, loading }) => {
  const [risks, setRisks] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingRisk, setEditingRisk] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({});

  // Generate default form data
  const getDefaultFormData = () => ({
    title: '',
    description: '',
    category: '',
    impact: 'medium',
    probability: 'medium',
    status: 'open',
    owner: '',
    mitigationPlan: ''
  });

  // Load risks from API
  useEffect(() => {
    loadRisks();
  }, []);

  const loadRisks = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await riskService.getAllRisks();
      setRisks(response.data || []);
    } catch (err) {
      console.error('Error loading risks:', err);
      setError('Failed to load risks. Please try again.');
      // Fallback to empty array instead of mock data
      setRisks([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenDialog = (risk = null) => {
    if (risk) {
      setEditingRisk(risk);
      setFormData(risk);
    } else {
      setEditingRisk(null);
      setFormData(getDefaultFormData());
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingRisk(null);
  };

  const handleSaveRisk = async () => {
    // Validate required fields
    if (!formData.title?.trim()) {
      setError('Title is required');
      return;
    }
    if (!formData.description?.trim()) {
      setError('Description is required');
      return;
    }
    
    try {
      setIsLoading(true);
      setError(null);
      
      const riskData = {
        ...formData,
        lastUpdated: new Date().toISOString().split('T')[0]
      };
      
      if (editingRisk) {
        await riskService.updateRisk(editingRisk.id, riskData);
        await loadRisks(); // Reload from API
        onSuccess('Risk updated successfully');
      } else {
        await riskService.createRisk(riskData);
        await loadRisks(); // Reload from API
        onSuccess('Risk created successfully');
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving risk:', error);
      setError('Failed to save risk. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteRisk = async (riskId) => {
    try {
      setIsLoading(true);
      setError(null);
      await riskService.deleteRisk(riskId);
      await loadRisks(); // Reload from API
      onSuccess('Risk deleted successfully');
    } catch (error) {
      console.error('Error deleting risk:', error);
      setError('Failed to delete risk. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const calculateRiskScore = (impact, probability) => {
    const impactScores = { low: 1, medium: 2, high: 3 };
    const probabilityScores = { low: 1, medium: 2, high: 3 };
    
    // Validate inputs
    if (!impactScores.hasOwnProperty(impact) || !probabilityScores.hasOwnProperty(probability)) {
      return 0;
    }
    
    // Calculate raw score (range 1-9)
    const raw = impactScores[impact] * probabilityScores[probability];
    
    // Normalize to 0-100: ((raw - 1) / 8) * 100
    const normalized = ((raw - 1) / 8) * 100;
    
    // Clamp to 0-100 and round
    return Math.max(0, Math.min(100, Math.round(normalized)));
  };

  const computeRiskScore = (risk) => {
    return calculateRiskScore(risk.impact, risk.probability);
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

  if (isLoading && risks.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <RiskIcon />
          Risk Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          disabled={isLoading}
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
                {risks.filter(r => computeRiskScore(r) >= 70).length}
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
                {risks.filter(r => computeRiskScore(r) >= 40 && computeRiskScore(r) < 70).length}
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
                {risks.filter(r => computeRiskScore(r) < 40).length}
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
                      {getRiskIcon(computeRiskScore(risk))}
                    </Box>
                    <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                      {risk.description}
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="textSecondary">
                        Risk Score: {computeRiskScore(risk)}/100
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={computeRiskScore(risk)} 
                        color={getRiskColor(computeRiskScore(risk))}
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
                        {getRiskIcon(computeRiskScore(risk))}
                        <Typography variant="body2" fontWeight={600}>
                          {computeRiskScore(risk)}
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
