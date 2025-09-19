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
  Fab,
  Tooltip
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Description as PolicyIcon,
  CheckCircle as ApprovedIcon,
  Pending as PendingIcon,
  Warning as WarningIcon
} from '@mui/icons-material';

const PolicyManagement = ({ apiCall, onSuccess, loading }) => {
  const [policies, setPolicies] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingPolicy, setEditingPolicy] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    status: 'draft',
    version: '1.0',
    effectiveDate: '',
    reviewDate: ''
  });

  // Mock data for demonstration
  useEffect(() => {
    const mockPolicies = [
      {
        id: 1,
        title: 'Data Privacy Policy',
        description: 'Comprehensive data privacy and protection guidelines',
        category: 'Privacy',
        status: 'approved',
        version: '2.1',
        effectiveDate: '2024-01-15',
        reviewDate: '2024-07-15',
        lastModified: '2024-01-10'
      },
      {
        id: 2,
        title: 'Information Security Policy',
        description: 'IT security standards and procedures',
        category: 'Security',
        status: 'pending',
        version: '1.5',
        effectiveDate: '2024-02-01',
        reviewDate: '2024-08-01',
        lastModified: '2024-01-20'
      },
      {
        id: 3,
        title: 'Code of Conduct',
        description: 'Employee behavior and ethical guidelines',
        category: 'HR',
        status: 'approved',
        version: '3.0',
        effectiveDate: '2023-12-01',
        reviewDate: '2024-06-01',
        lastModified: '2023-11-25'
      }
    ];
    setPolicies(mockPolicies);
  }, []);

  const handleOpenDialog = (policy = null) => {
    if (policy) {
      setEditingPolicy(policy);
      setFormData(policy);
    } else {
      setEditingPolicy(null);
      setFormData({
        title: '',
        description: '',
        category: '',
        status: 'draft',
        version: '1.0',
        effectiveDate: '',
        reviewDate: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingPolicy(null);
  };

  const handleSavePolicy = async () => {
    try {
      if (editingPolicy) {
        // Update existing policy
        const updatedPolicies = policies.map(p => 
          p.id === editingPolicy.id ? { ...formData, id: editingPolicy.id } : p
        );
        setPolicies(updatedPolicies);
        onSuccess('Policy updated successfully');
      } else {
        // Create new policy
        const newPolicy = {
          ...formData,
          id: policies.length + 1,
          lastModified: new Date().toISOString().split('T')[0]
        };
        setPolicies([...policies, newPolicy]);
        onSuccess('Policy created successfully');
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving policy:', error);
    }
  };

  const handleDeletePolicy = (policyId) => {
    setPolicies(policies.filter(p => p.id !== policyId));
    onSuccess('Policy deleted successfully');
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'approved':
        return <ApprovedIcon color="success" />;
      case 'pending':
        return <PendingIcon color="warning" />;
      case 'draft':
        return <WarningIcon color="info" />;
      default:
        return <PendingIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved':
        return 'success';
      case 'pending':
        return 'warning';
      case 'draft':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <PolicyIcon />
          Policy Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          sx={{ textTransform: 'none' }}
        >
          New Policy
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Policies
              </Typography>
              <Typography variant="h4">
                {policies.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Approved
              </Typography>
              <Typography variant="h4" color="success.main">
                {policies.filter(p => p.status === 'approved').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Review
              </Typography>
              <Typography variant="h4" color="warning.main">
                {policies.filter(p => p.status === 'pending').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Drafts
              </Typography>
              <Typography variant="h4" color="info.main">
                {policies.filter(p => p.status === 'draft').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Policies Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            All Policies
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Category</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Version</TableCell>
                  <TableCell>Effective Date</TableCell>
                  <TableCell>Review Date</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {policies.map((policy) => (
                  <TableRow key={policy.id}>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        {policy.title}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {policy.description}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip label={policy.category} size="small" />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getStatusIcon(policy.status)}
                        <Chip 
                          label={policy.status} 
                          size="small" 
                          color={getStatusColor(policy.status)}
                        />
                      </Box>
                    </TableCell>
                    <TableCell>{policy.version}</TableCell>
                    <TableCell>{policy.effectiveDate}</TableCell>
                    <TableCell>{policy.reviewDate}</TableCell>
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
                            onClick={() => handleOpenDialog(policy)}
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton 
                            size="small" 
                            color="error"
                            onClick={() => handleDeletePolicy(policy.id)}
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

      {/* Add/Edit Policy Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingPolicy ? 'Edit Policy' : 'Create New Policy'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Policy Title"
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
                  <MenuItem value="Privacy">Privacy</MenuItem>
                  <MenuItem value="Security">Security</MenuItem>
                  <MenuItem value="HR">HR</MenuItem>
                  <MenuItem value="Finance">Finance</MenuItem>
                  <MenuItem value="Operations">Operations</MenuItem>
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
                  <MenuItem value="draft">Draft</MenuItem>
                  <MenuItem value="pending">Pending Review</MenuItem>
                  <MenuItem value="approved">Approved</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Version"
                value={formData.version}
                onChange={(e) => setFormData({ ...formData, version: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="date"
                label="Effective Date"
                value={formData.effectiveDate}
                onChange={(e) => setFormData({ ...formData, effectiveDate: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="date"
                label="Review Date"
                value={formData.reviewDate}
                onChange={(e) => setFormData({ ...formData, reviewDate: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSavePolicy} variant="contained">
            {editingPolicy ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PolicyManagement;
