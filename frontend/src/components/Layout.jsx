import React from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Button,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Divider
} from '@mui/material';
import {
  AccountCircle,
  Notifications,
  Settings,
  Logout,
  Dashboard as DashboardIcon
} from '@mui/icons-material';

const Layout = ({ children, currentPage, onNavigation, onSuccess }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [notificationAnchor, setNotificationAnchor] = React.useState(null);

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationMenuOpen = (event) => {
    setNotificationAnchor(event.currentTarget);
  };

  const handleNotificationMenuClose = () => {
    setNotificationAnchor(null);
  };

  const handleLogout = () => {
    // Handle logout logic
    onSuccess('Logged out successfully');
    handleProfileMenuClose();
  };

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
    { id: 'policies', label: 'Policies', icon: <DashboardIcon /> },
    { id: 'risks', label: 'Risks', icon: <DashboardIcon /> },
    { id: 'compliance', label: 'Compliance', icon: <DashboardIcon /> },
    { id: 'workflows', label: 'Workflows', icon: <DashboardIcon /> },
    { id: 'analytics', label: 'Analytics', icon: <DashboardIcon /> },
    { id: 'ai-agents', label: 'AI Agents', icon: <DashboardIcon /> },
    { id: 'settings', label: 'Settings', icon: <Settings /> },
  ];

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Top App Bar */}
      <AppBar position="sticky" elevation={2} sx={{ bgcolor: 'primary.main' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            BFSI GRC Platform
          </Typography>
          
          <Chip 
            label="BFSI AI Agent" 
            color="secondary" 
            size="small" 
            sx={{ mr: 2 }}
          />
          
          <Typography variant="body2" sx={{ opacity: 0.8, mr: 2 }}>
            Banking, Financial Services & Insurance GRC
          </Typography>

          {/* Notifications */}
          <IconButton
            size="large"
            color="inherit"
            onClick={handleNotificationMenuOpen}
            sx={{ mr: 1 }}
          >
            <Notifications />
          </IconButton>

          {/* Profile Menu */}
          <IconButton
            size="large"
            color="inherit"
            onClick={handleProfileMenuOpen}
          >
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
              <AccountCircle />
            </Avatar>
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Navigation */}
      <Box sx={{ bgcolor: 'background.paper', borderBottom: 1, borderColor: 'divider' }}>
        <Container maxWidth="xl">
          <Box sx={{ display: 'flex', gap: 1, py: 1, overflowX: 'auto' }}>
            {navigationItems.map((item) => (
              <Button
                key={item.id}
                startIcon={item.icon}
                onClick={() => onNavigation(item.id)}
                variant={currentPage === item.id ? 'contained' : 'text'}
                color={currentPage === item.id ? 'primary' : 'inherit'}
                sx={{ 
                  textTransform: 'none',
                  fontWeight: currentPage === item.id ? 600 : 400,
                  minWidth: 'auto',
                  px: 2
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxWidth="xl" sx={{ py: 3 }}>
        {children}
      </Container>

      {/* Profile Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleProfileMenuClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <MenuItem onClick={handleProfileMenuClose}>
          <AccountCircle sx={{ mr: 1 }} />
          Profile
        </MenuItem>
        <MenuItem onClick={handleProfileMenuClose}>
          <Settings sx={{ mr: 1 }} />
          Settings
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleLogout}>
          <Logout sx={{ mr: 1 }} />
          Logout
        </MenuItem>
      </Menu>

      {/* Notifications Menu */}
      <Menu
        anchorEl={notificationAnchor}
        open={Boolean(notificationAnchor)}
        onClose={handleNotificationMenuClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <MenuItem onClick={handleNotificationMenuClose}>
          New compliance requirement added
        </MenuItem>
        <MenuItem onClick={handleNotificationMenuClose}>
          Risk assessment completed
        </MenuItem>
        <MenuItem onClick={handleNotificationMenuClose}>
          Policy review due in 3 days
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Layout;
