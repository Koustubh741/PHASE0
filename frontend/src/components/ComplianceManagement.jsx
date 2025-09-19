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
  Alert
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Assignment as ComplianceIcon,
  CheckCircle as CompliantIcon,
  Warning as NonCompliantIcon,
  Schedule as PendingIcon
} from '@mui/icons-material';

const ComplianceManagement = ({ apiCall, onSuccess, loading }) => {
  const [complianceItems, setComplianceItems] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    framework: '',
    requirement: '',
    status: 'pending',
    priority: 'medium',
    dueDate: '',
    owner: '',
    evidence: ''
  });

  // Mock data for demonstration
  useEffect(() => {
    const mockComplianceItems = [
      {
        id: 1,
        title: 'GDPR Data Protection',
        description: 'Ensure compliance with GDPR data protection requirements',
        framework: 'GDPR',
        requirement: 'Article 32 - Security of processing',
        status: 'compliant',
        priority: 'high',
        dueDate: '2024-02-15',
        owner: 'Privacy Team',
        evidence: 'Data protection impact assessment completed',
        lastUpdated: '2024-01-15',
        progress: 100
      },
      {
        id: 2,
        title: 'SOX Financial Controls',
        description: 'Implement and maintain SOX financial reporting controls',
        framework: 'SOX',
        requirement: 'Section 404 - Management assessment',
        status: 'in_progress',
        priority: 'high',
        dueDate: '2024-03-31',
        owner: 'Finance Team',
        evidence: 'Control documentation in progress',
        lastUpdated: '2024-01-20',
        progress: 65
      },
      {
        id: 3,
        title: 'ISO 27001 Security',
        description: 'Maintain ISO 27001 information security management system',
        framework: 'ISO 27001',
        requirement: 'A.8.1.1 - Inventory of assets',
        status: 'non_compliant',
        priority: 'medium',
        dueDate: '2024-04-30',
        owner: 'Security Team',
        evidence: 'Asset inventory needs updating',
        lastUpdated: '2024-01-10',
        progress: 30
      }
    ];
    setComplianceItems(mockComplianceItems);
  }, []);

  const handleOpenDialog = (item = null) => {
    if (item) {
      setEditingItem(item);
      setFormData(item);
    } else {
      setEditingItem(null);
      setFormData({
        title: '',
        description: '',
        framework: '',
        requirement: '',
        status: 'pending',
        priority: 'medium',
        dueDate: '',
        owner: '',
        evidence: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingItem(null);
  };

  const handleSaveItem = async () => {
    try {
      const progress = calculateProgress(formData.status);
      const itemData = { 
        ...formData, 
        progress, 
        lastUpdated: new Date().toISOString().split('T')[0] 
      };
      
      if (editingItem) {
        const updatedItems = complianceItems.map(item => 
          item.id === editingItem.id ? { ...itemData, id: editingItem.id } : item
        );
        setComplianceItems(updatedItems);
        onSuccess('Compliance item updated successfully');
      } else {
        const newItem = {
          ...itemData,
          id: complianceItems.length + 1
        };
        setComplianceItems([...complianceItems, newItem]);
        onSuccess('Compliance item created successfully');
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving compliance item:', error);
    }
  };

  const handleDeleteItem = (itemId) => {
    setComplianceItems(complianceItems.filter(item => item.id !== itemId));
    onSuccess('Compliance item deleted successfully');
  };

  const calculateProgress = (status) => {
    switch (status) {
      case 'compliant':
        return 100;
      case 'in_progress':
        return 65;
      case 'non_compliant':
        return 30;
      case 'pending':
        return 0;
      default:
        return 0;
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant':
        return <CompliantIcon color="success" />;
      case 'non_compliant':
        return <NonCompliantIcon color="error" />;
      case 'in_progress':
        return <PendingIcon color="warning" />;
      default:
        return <PendingIcon color="info" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'compliant':
        return 'success';
      case 'non_compliant':
        return 'error';
      case 'in_progress':
        return 'warning';
      case 'pending':
        return 'info';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getComplianceScore = () => {
    const total = complianceItems.length;
    const compliant = complianceItems.filter(item => item.status === 'compliant').length;
    return total > 0 ? Math.round((compliant / total) * 100) : 0;
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <ComplianceIcon />
          Compliance Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          sx={{ textTransform: 'none' }}
        >
          New Compliance Item
        </Button>
      </Box>

      {/* Compliance Score Alert */}
      <Alert 
        severity={getComplianceScore() >= 80 ? 'success' : getComplianceScore() >= 60 ? 'warning' : 'error'}
        sx={{ mb: 3 }}
      >
        <Typography variant="h6">
          Overall Compliance Score: {getComplianceScore()}%
        </Typography>
        <Typography variant="body2">
          {getComplianceScore() >= 80 
            ? 'Excellent compliance status maintained' 
            : getComplianceScore() >= 60 
            ? 'Good compliance with room for improvement'
            : 'Immediate attention required for compliance issues'
          }
        </Typography>
      </Alert>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Items
              </Typography>
              <Typography variant="h4">
                {complianceItems.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Compliant
              </Typography>
              <Typography variant="h4" color="success.main">
                {complianceItems.filter(item => item.status === 'compliant').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                In Progress
              </Typography>
              <Typography variant="h4" color="warning.main">
                {complianceItems.filter(item => item.status === 'in_progress').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Non-Compliant
              </Typography>
              <Typography variant="h4" color="error.main">
                {complianceItems.filter(item => item.status === 'non_compliant').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Compliance Items Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Compliance Items
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Framework</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Priority</TableCell>
                  <TableCell>Progress</TableCell>
                  <TableCell>Due Date</TableCell>
                  <TableCell>Owner</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {complianceItems.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        {item.title}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {item.description}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {item.requirement}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip label={item.framework} size="small" />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getStatusIcon(item.status)}
                        <Chip 
                          label={item.status.replace('_', ' ')} 
                          size="small" 
                          color={getStatusColor(item.status)}
                        />
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={item.priority} 
                        size="small" 
                        color={getPriorityColor(item.priority)}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 100 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={item.progress} 
                          color={getStatusColor(item.status)}
                          sx={{ flexGrow: 1 }}
                        />
                        <Typography variant="body2" fontWeight={600}>
                          {item.progress}%
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>{item.dueDate}</TableCell>
                    <TableCell>{item.owner}</TableCell>
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
                            onClick={() => handleOpenDialog(item)}
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton 
                            size="small" 
                            color="error"
                            onClick={() => handleDeleteItem(item.id)}
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

      {/* Add/Edit Compliance Item Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingItem ? 'Edit Compliance Item' : 'Create New Compliance Item'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Title"
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
                <InputLabel>Framework</InputLabel>
                <Select
                  value={formData.framework}
                  label="Framework"
                  onChange={(e) => setFormData({ ...formData, framework: e.target.value })}
                >
                  <MenuItem value="GDPR">GDPR</MenuItem>
                  <MenuItem value="SOX">SOX</MenuItem>
                  <MenuItem value="ISO 27001">ISO 27001</MenuItem>
                  <MenuItem value="HIPAA">HIPAA</MenuItem>
                  <MenuItem value="PCI DSS">PCI DSS</MenuItem>
                  <MenuItem value="NIST">NIST</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Requirement"
                value={formData.requirement}
                onChange={(e) => setFormData({ ...formData, requirement: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={formData.status}
                  label="Status"
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                >
                  <MenuItem value="pending">Pending</MenuItem>
                  <MenuItem value="in_progress">In Progress</MenuItem>
                  <MenuItem value="compliant">Compliant</MenuItem>
                  <MenuItem value="non_compliant">Non-Compliant</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Priority</InputLabel>
                <Select
                  value={formData.priority}
                  label="Priority"
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                >
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="date"
                label="Due Date"
                value={formData.dueDate}
                onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
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
                label="Evidence"
                value={formData.evidence}
                onChange={(e) => setFormData({ ...formData, evidence: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveItem} variant="contained">
            {editingItem ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ComplianceManagement;
