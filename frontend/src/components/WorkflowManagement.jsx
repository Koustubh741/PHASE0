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
  AccountTree as WorkflowIcon,
  PlayArrow as RunningIcon,
  Pause as PausedIcon,
  CheckCircle as CompletedIcon,
  Schedule as PendingIcon
} from '@mui/icons-material';

const WorkflowManagement = ({ apiCall, onSuccess, loading }) => {
  const [workflows, setWorkflows] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingWorkflow, setEditingWorkflow] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    status: 'draft',
    priority: 'medium',
    assignedTo: '',
    dueDate: '',
    steps: []
  });

  // Mock data for demonstration
  useEffect(() => {
    const mockWorkflows = [
      {
        id: 1,
        name: 'Policy Approval Workflow',
        description: 'Standard workflow for policy review and approval',
        category: 'Policy',
        status: 'running',
        priority: 'high',
        assignedTo: 'Compliance Team',
        dueDate: '2024-02-15',
        steps: ['Draft', 'Review', 'Approval', 'Implementation'],
        currentStep: 2,
        progress: 60,
        lastUpdated: '2024-01-15'
      },
      {
        id: 2,
        name: 'Risk Assessment Workflow',
        description: 'Process for identifying and assessing risks',
        category: 'Risk',
        status: 'completed',
        priority: 'medium',
        assignedTo: 'Risk Team',
        dueDate: '2024-01-30',
        steps: ['Identification', 'Assessment', 'Mitigation', 'Monitoring'],
        currentStep: 4,
        progress: 100,
        lastUpdated: '2024-01-25'
      },
      {
        id: 3,
        name: 'Incident Response Workflow',
        description: 'Emergency response process for security incidents',
        category: 'Security',
        status: 'paused',
        priority: 'high',
        assignedTo: 'Security Team',
        dueDate: '2024-02-20',
        steps: ['Detection', 'Analysis', 'Containment', 'Recovery', 'Lessons Learned'],
        currentStep: 3,
        progress: 45,
        lastUpdated: '2024-01-20'
      }
    ];
    setWorkflows(mockWorkflows);
  }, []);

  const handleOpenDialog = (workflow = null) => {
    if (workflow) {
      setEditingWorkflow(workflow);
      setFormData(workflow);
    } else {
      setEditingWorkflow(null);
      setFormData({
        name: '',
        description: '',
        category: '',
        status: 'draft',
        priority: 'medium',
        assignedTo: '',
        dueDate: '',
        steps: []
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingWorkflow(null);
  };

  const handleSaveWorkflow = async () => {
    try {
      const workflowData = { 
        ...formData, 
        lastUpdated: new Date().toISOString().split('T')[0] 
      };
      
      if (editingWorkflow) {
        const updatedWorkflows = workflows.map(w => 
          w.id === editingWorkflow.id ? { ...workflowData, id: editingWorkflow.id } : w
        );
        setWorkflows(updatedWorkflows);
        onSuccess('Workflow updated successfully');
      } else {
        const newWorkflow = {
          ...workflowData,
          id: workflows.length + 1,
          currentStep: 1,
          progress: 0
        };
        setWorkflows([...workflows, newWorkflow]);
        onSuccess('Workflow created successfully');
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving workflow:', error);
    }
  };

  const handleDeleteWorkflow = (workflowId) => {
    setWorkflows(workflows.filter(w => w.id !== workflowId));
    onSuccess('Workflow deleted successfully');
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running':
        return <RunningIcon color="primary" />;
      case 'completed':
        return <CompletedIcon color="success" />;
      case 'paused':
        return <PausedIcon color="warning" />;
      case 'draft':
        return <PendingIcon color="info" />;
      default:
        return <PendingIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'primary';
      case 'completed':
        return 'success';
      case 'paused':
        return 'warning';
      case 'draft':
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

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <WorkflowIcon />
          Workflow Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          sx={{ textTransform: 'none' }}
        >
          New Workflow
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Workflows
              </Typography>
              <Typography variant="h4">
                {workflows.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Running
              </Typography>
              <Typography variant="h4" color="primary.main">
                {workflows.filter(w => w.status === 'running').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Completed
              </Typography>
              <Typography variant="h4" color="success.main">
                {workflows.filter(w => w.status === 'completed').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Paused
              </Typography>
              <Typography variant="h4" color="warning.main">
                {workflows.filter(w => w.status === 'paused').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Workflows Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            All Workflows
          </Typography>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Category</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Priority</TableCell>
                  <TableCell>Progress</TableCell>
                  <TableCell>Assigned To</TableCell>
                  <TableCell>Due Date</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {workflows.map((workflow) => (
                  <TableRow key={workflow.id}>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        {workflow.name}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {workflow.description}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip label={workflow.category} size="small" />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getStatusIcon(workflow.status)}
                        <Chip 
                          label={workflow.status} 
                          size="small" 
                          color={getStatusColor(workflow.status)}
                        />
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={workflow.priority} 
                        size="small" 
                        color={getPriorityColor(workflow.priority)}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 120 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={workflow.progress} 
                          color={getStatusColor(workflow.status)}
                          sx={{ flexGrow: 1 }}
                        />
                        <Typography variant="body2" fontWeight={600}>
                          {workflow.progress}%
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>{workflow.assignedTo}</TableCell>
                    <TableCell>{workflow.dueDate}</TableCell>
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
                            onClick={() => handleOpenDialog(workflow)}
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete">
                          <IconButton 
                            size="small" 
                            color="error"
                            onClick={() => handleDeleteWorkflow(workflow.id)}
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

      {/* Add/Edit Workflow Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingWorkflow ? 'Edit Workflow' : 'Create New Workflow'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Workflow Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
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
                  <MenuItem value="Policy">Policy</MenuItem>
                  <MenuItem value="Risk">Risk</MenuItem>
                  <MenuItem value="Security">Security</MenuItem>
                  <MenuItem value="Compliance">Compliance</MenuItem>
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
                  <MenuItem value="running">Running</MenuItem>
                  <MenuItem value="paused">Paused</MenuItem>
                  <MenuItem value="completed">Completed</MenuItem>
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
                label="Assigned To"
                value={formData.assignedTo}
                onChange={(e) => setFormData({ ...formData, assignedTo: e.target.value })}
              />
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
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveWorkflow} variant="contained">
            {editingWorkflow ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WorkflowManagement;
