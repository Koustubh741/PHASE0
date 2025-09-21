/**
 * Main App Component
 * 
 * This is the root component of the GRC Platform frontend application.
 * It sets up routing, theme, and global state management.
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';

import { theme } from './theme';
import { store } from './store';
import { Layout } from './components/Layout';
import { ProtectedRoute } from './components/ProtectedRoute';

// Feature modules
import { Dashboard } from './features/dashboard';
import { Policies } from './features/policies';
import { Risks } from './features/risks';
import { Compliance } from './features/compliance';
import { Workflows } from './features/workflows';
import { AIAgents } from './features/ai-agents';
import { Auth } from './features/auth';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/auth/*" element={<Auth />} />
            
            {/* Protected routes */}
            <Route path="/" element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="policies/*" element={<Policies />} />
              <Route path="risks/*" element={<Risks />} />
              <Route path="compliance/*" element={<Compliance />} />
              <Route path="workflows/*" element={<Workflows />} />
              <Route path="ai-agents/*" element={<AIAgents />} />
            </Route>
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  );
};

export default App;
