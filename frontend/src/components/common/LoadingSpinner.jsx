import React from 'react';
import {
  Box,
  CircularProgress,
  Typography,
  Backdrop
} from '@mui/material';

const LoadingSpinner = ({ 
  loading = false, 
  message = 'Loading...', 
  fullScreen = false,
  size = 40,
  color = 'primary'
}) => {
  if (!loading) return null;

  const SpinnerContent = () => (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2
      }}
    >
      <CircularProgress size={size} color={color} />
      {message && (
        <Typography variant="body2" color="textSecondary">
          {message}
        </Typography>
      )}
    </Box>
  );

  if (fullScreen) {
    return (
      <Backdrop
        sx={{ 
          color: '#fff', 
          zIndex: (theme) => theme.zIndex.drawer + 1,
          bgcolor: 'rgba(0, 0, 0, 0.5)'
        }}
        open={loading}
      >
        <SpinnerContent />
      </Backdrop>
    );
  }

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        p: 4
      }}
    >
      <SpinnerContent />
    </Box>
  );
};

export default LoadingSpinner;
