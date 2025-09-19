import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider,
  Paper,
  Tabs,
  Tab
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Policy as PolicyIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { bfsiService } from '../services/bfsiService';

const BFSIPolicyManagement = ({ apiCall, onSuccess, loading }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [industryStandardToggle, setIndustryStandardToggle] = useState(false);
  const [policyStandards, setPolicyStandards] = useState([]);
  const [selectedStandard, setSelectedStandard] = useState('');
  const [customPolicy, setCustomPolicy] = useState({
    name: '',
    description: '',
    category: '',
    requirements: '',
    complianceLevel: 'high'
  });
  const [policies, setPolicies] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogMode, setDialogMode] = useState('add'); // 'add' or 'edit'
  const [editingPolicy, setEditingPolicy] = useState(null);

  // BFSI Industry Standard Policies
  const bfsiStandardPolicies = [
    {
      id: 'basel_iii',
      name: 'Basel III Capital Requirements',
      description: 'International regulatory framework for bank capital adequacy',
      category: 'Capital Adequacy',
      requirements: 'Minimum capital ratios, leverage ratios, liquidity requirements',
      complianceLevel: 'critical'
    },
    {
      id: 'sox',
      name: 'Sarbanes-Oxley Act (SOX)',
      description: 'Corporate governance and financial disclosure requirements',
      category: 'Corporate Governance',
      requirements: 'Internal controls, financial reporting, audit requirements',
      complianceLevel: 'critical'
    },
    {
      id: 'pci_dss',
      name: 'PCI DSS',
      description: 'Payment Card Industry Data Security Standard',
      category: 'Data Security',
      requirements: 'Cardholder data protection, network security, access controls',
      complianceLevel: 'high'
    },
    {
      id: 'aml_kyc',
      name: 'AML/KYC Requirements',
      description: 'Anti-Money Laundering and Know Your Customer regulations',
      category: 'Anti-Money Laundering',
      requirements: 'Customer due diligence, transaction monitoring, suspicious activity reporting',
      complianceLevel: 'critical'
    },
    {
      id: 'gdpr',
      name: 'GDPR Compliance',
      description: 'General Data Protection Regulation for EU customers',
      category: 'Data Privacy',
      requirements: 'Data protection, consent management, breach notification',
      complianceLevel: 'high'
    },
    {
      id: 'ifrs',
      name: 'IFRS Standards',
      description: 'International Financial Reporting Standards',
      category: 'Financial Reporting',
      requirements: 'Standardized financial reporting, disclosure requirements',
      complianceLevel: 'high'
    }
  ];

  useEffect(() => {
    loadPolicyStandards();
    loadPolicies();
  }, []);

  const loadPolicyStandards = async () => {
    try {
      setIsLoading(true);
      const standards = await bfsiService.getPolicyStandards();
      setPolicyStandards(standards || bfsiStandardPolicies);
    } catch (error) {
      console.error('Failed to load policy standards:', error);
      setPolicyStandards(bfsiStandardPolicies); // Fallback to local data
    } finally {
      setIsLoading(false);
    }
  };

  const loadPolicies = async () => {
    try {
      setIsLoading(true);
      // This would typically load from backend
      setPolicies([]);
    } catch (error) {
      console.error('Failed to load policies:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleIndustryStandardToggle = async (event) => {
    const isEnabled = event.target.checked;
    setIndustryStandardToggle(isEnabled);
    
    try {
      if (isEnabled && selectedStandard) {
        const selectedPolicy = policyStandards.find(p => p.id === selectedStandard);
        if (selectedPolicy) {
          await bfsiService.addIndustryStandardPolicy(selectedPolicy);
          setSuccess(`Industry standard policy "${selectedPolicy.name}" has been applied`);
          onSuccess(`Industry standard policy "${selectedPolicy.name}" has been applied`);
        }
      }
    } catch (error) {
      setError(`Failed to apply industry standard policy: ${error.message}`);
    }
  };

  const handleAddCustomPolicy = () => {
    setDialogMode('add');
    setCustomPolicy({
      name: '',
      description: '',
      category: '',
      requirements: '',
      complianceLevel: 'high'
    });
    setOpenDialog(true);
  };

  const handleEditPolicy = (policy) => {
    setDialogMode('edit');
    setEditingPolicy(policy);
    setCustomPolicy({
      name: policy.name,
      description: policy.description,
      category: policy.category,
      requirements: policy.requirements,
      complianceLevel: policy.complianceLevel
    });
    setOpenDialog(true);
  };

  const handleSavePolicy = async () => {
    try {
      if (dialogMode === 'add') {
        const newPolicy = {
          ...customPolicy,
          id: Date.now().toString(),
          type: 'custom',
          createdAt: new Date().toISOString()
        };
        setPolicies([...policies, newPolicy]);
        setSuccess('Custom policy added successfully');
      } else {
        const updatedPolicies = policies.map(p => 
          p.id === editingPolicy.id ? { ...p, ...customPolicy } : p
        );
        setPolicies(updatedPolicies);
        setSuccess('Policy updated successfully');
      }
      setOpenDialog(false);
      onSuccess(dialogMode === 'add' ? 'Custom policy added successfully' : 'Policy updated successfully');
    } catch (error) {
      setError(`Failed to save policy: ${error.message}`);
    }
  };

  const handleDeletePolicy = async (policyId) => {
    try {
      const updatedPolicies = policies.filter(p => p.id !== policyId);
      setPolicies(updatedPolicies);
      setSuccess('Policy deleted successfully');
      onSuccess('Policy deleted successfully');
    } catch (error) {
      setError(`Failed to delete policy: ${error.message}`);
    }
  };

  const getComplianceLevelColor = (level) => {
    switch (level) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const TabPanel = ({ children, value, index }) => (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        <PolicyIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        BFSI Policy Management
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      <Paper sx={{ mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Industry Standards" icon={<SecurityIcon />} />
          <Tab label="Custom Policies" icon={<PolicyIcon />} />
          <Tab label="Policy Compliance" icon={<AssessmentIcon />} />
        </Tabs>
      </Paper>

      {/* Industry Standards Tab */}
      <TabPanel value={activeTab} index={0}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Industry Standard Policy Integration
            </Typography>
            
            <Grid container spacing={3} alignItems="center">
              <Grid item xs={12} md={6}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={industryStandardToggle}
                      onChange={handleIndustryStandardToggle}
                      color="primary"
                    />
                  }
                  label="Enable Industry Standard Policy"
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Select Standard Policy</InputLabel>
                  <Select
                    value={selectedStandard}
                    onChange={(e) => setSelectedStandard(e.target.value)}
                    disabled={!industryStandardToggle}
                  >
                    {policyStandards.map((policy) => (
                      <MenuItem key={policy.id} value={policy.id}>
                        {policy.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            {industryStandardToggle && selectedStandard && (
              <Box sx={{ mt: 3 }}>
                <Alert severity="info">
                  Industry standard policy integration is enabled. The selected policy will be applied to all BFSI operations.
                </Alert>
              </Box>
            )}

            <Divider sx={{ my: 3 }} />

            <Typography variant="h6" gutterBottom>
              Available Industry Standard Policies
            </Typography>
            
            <Grid container spacing={2}>
              {policyStandards.map((policy) => (
                <Grid item xs={12} md={6} key={policy.id}>
                  <Card variant="outlined">
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Typography variant="h6">{policy.name}</Typography>
                        <Chip 
                          label={policy.complianceLevel} 
                          color={getComplianceLevelColor(policy.complianceLevel)}
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {policy.description}
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        Category: {policy.category}
                      </Typography>
                      <Typography variant="body2">
                        Requirements: {policy.requirements}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Custom Policies Tab */}
      <TabPanel value={activeTab} index={1}>
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6">
                Custom Policies
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddCustomPolicy}
              >
                Add Custom Policy
              </Button>
            </Box>

            {policies.length === 0 ? (
              <Alert severity="info">
                No custom policies defined. Click "Add Custom Policy" to create one.
              </Alert>
            ) : (
              <List>
                {policies.map((policy) => (
                  <ListItem key={policy.id} divider>
                    <ListItemText
                      primary={policy.name}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {policy.description}
                          </Typography>
                          <Box sx={{ mt: 1 }}>
                            <Chip 
                              label={policy.category} 
                              size="small" 
                              sx={{ mr: 1 }}
                            />
                            <Chip 
                              label={policy.complianceLevel} 
                              color={getComplianceLevelColor(policy.complianceLevel)}
                              size="small"
                            />
                          </Box>
                        </Box>
                      }
                    />
                    <ListItemSecondaryAction>
                      <IconButton onClick={() => handleEditPolicy(policy)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton onClick={() => handleDeletePolicy(policy.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            )}
          </CardContent>
        </Card>
      </TabPanel>

      {/* Policy Compliance Tab */}
      <TabPanel value={activeTab} index={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Policy Compliance Status
            </Typography>
            <Alert severity="info">
              Policy compliance monitoring will be implemented based on the selected industry standard policies and custom policies.
            </Alert>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Add/Edit Policy Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {dialogMode === 'add' ? 'Add Custom Policy' : 'Edit Policy'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Policy Name"
                value={customPolicy.name}
                onChange={(e) => setCustomPolicy({ ...customPolicy, name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                multiline
                rows={3}
                value={customPolicy.description}
                onChange={(e) => setCustomPolicy({ ...customPolicy, description: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Category"
                value={customPolicy.category}
                onChange={(e) => setCustomPolicy({ ...customPolicy, category: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Compliance Level</InputLabel>
                <Select
                  value={customPolicy.complianceLevel}
                  onChange={(e) => setCustomPolicy({ ...customPolicy, complianceLevel: e.target.value })}
                >
                  <MenuItem value="critical">Critical</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Requirements"
                multiline
                rows={4}
                value={customPolicy.requirements}
                onChange={(e) => setCustomPolicy({ ...customPolicy, requirements: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleSavePolicy} variant="contained">
            {dialogMode === 'add' ? 'Add Policy' : 'Update Policy'}
          </Button>
        </DialogActions>
      </Dialog>

      {isLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <CircularProgress />
        </Box>
      )}
    </Box>
  );
};

export default BFSIPolicyManagement;
