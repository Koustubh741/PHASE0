import React, { useState } from 'react';
import {
  BrowserRouter as Router
} from 'react-router-dom';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  LinearProgress,
  Alert,
  Snackbar
} from '@mui/material';

// Import components
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import PolicyManagement from './components/PolicyManagement';
import RiskManagement from './components/RiskManagement';
import ComplianceManagement from './components/ComplianceManagement';
import WorkflowManagement from './components/WorkflowManagement';
import Analytics from './components/Analytics';
import Settings from './components/Settings';
import AIAgentsManagement from './components/AIAgentsManagement';
import ErrorBoundary from './components/Common/ErrorBoundary';

// Import BFSI-specific components
import BFSIDashboard from './components/BFSIDashboard';
import BFSIPolicyManagement from './components/BFSIPolicyManagement';

// Create theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

// Navigation items (used by Layout component)
// const navigationItems = [
//   { id: 'dashboard', label: 'Dashboard', path: '/dashboard' },
//   { id: 'policies', label: 'Policies', path: '/policies' },
//   { id: 'risks', label: 'Risks', path: '/risks' },
//   { id: 'compliance', label: 'Compliance', path: '/compliance' },
//   { id: 'workflows', label: 'Workflows', path: '/workflows' },
//   { id: 'analytics', label: 'Analytics', path: '/analytics' },
//   { id: 'settings', label: 'Settings', path: '/settings' },
// ];

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // API base URL
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Handle API calls
  const apiCall = async (endpoint, options = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer dummy-token', // In production, use real JWT
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Handle navigation
  const handleNavigation = (pageId) => {
    setCurrentPage(pageId);
  };

  // Handle success messages
  const handleSuccess = (message) => {
    setSuccess(message);
  };

  // Close notifications
  const handleCloseError = () => setError(null);
  const handleCloseSuccess = () => setSuccess(null);

  // Render current page
  const renderCurrentPage = () => {
    const commonProps = {
      apiCall,
      onSuccess: handleSuccess,
      loading,
    };

    switch (currentPage) {
      case 'dashboard':
        return <BFSIDashboard {...commonProps} />;
      case 'policies':
        return <BFSIPolicyManagement {...commonProps} />;
      case 'risks':
        return <RiskManagement {...commonProps} />;
      case 'compliance':
        return <ComplianceManagement {...commonProps} />;
      case 'workflows':
        return <WorkflowManagement {...commonProps} />;
      case 'analytics':
        return <Analytics {...commonProps} />;
      case 'ai-agents':
        return <AIAgentsManagement {...commonProps} />;
      case 'settings':
        return <Settings {...commonProps} />;
      default:
        return <BFSIDashboard {...commonProps} />;
    }
  };

  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Layout 
            currentPage={currentPage} 
            onNavigation={handleNavigation}
            onSuccess={handleSuccess}
          >
            {/* Loading Bar */}
            {loading && <LinearProgress />}

            {/* Main Content */}
            {renderCurrentPage()}

            {/* Notifications */}
            <Snackbar
              open={!!error}
              autoHideDuration={6000}
              onClose={handleCloseError}
              anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
              <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
                {error}
              </Alert>
            </Snackbar>

            <Snackbar
              open={!!success}
              autoHideDuration={4000}
              onClose={handleCloseSuccess}
              anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
              <Alert onClose={handleCloseSuccess} severity="success" sx={{ width: '100%' }}>
                {success}
              </Alert>
            </Snackbar>
          </Layout>
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
