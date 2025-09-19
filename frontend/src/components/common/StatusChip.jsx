import React from 'react';
import { Chip } from '@mui/material';
import {
  CheckCircle as SuccessIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Schedule as PendingIcon,
  PlayArrow as RunningIcon,
  Pause as PausedIcon,
  Stop as StoppedIcon
} from '@mui/icons-material';

const StatusChip = ({ status, variant = 'filled', size = 'small' }) => {
  const getStatusConfig = (status) => {
    const statusLower = status?.toLowerCase() || '';
    
    switch (statusLower) {
      // Success states
      case 'approved':
      case 'compliant':
      case 'completed':
      case 'success':
      case 'active':
      case 'enabled':
        return {
          label: status,
          color: 'success',
          icon: <SuccessIcon />
        };
      
      // Warning states
      case 'pending':
      case 'in_progress':
      case 'review':
      case 'warning':
      case 'medium':
        return {
          label: status,
          color: 'warning',
          icon: <WarningIcon />
        };
      
      // Error states
      case 'rejected':
      case 'non_compliant':
      case 'failed':
      case 'error':
      case 'high':
      case 'critical':
      case 'disabled':
        return {
          label: status,
          color: 'error',
          icon: <ErrorIcon />
        };
      
      // Info states
      case 'draft':
      case 'low':
      case 'info':
      case 'new':
        return {
          label: status,
          color: 'info',
          icon: <InfoIcon />
        };
      
      // Special states
      case 'running':
        return {
          label: status,
          color: 'primary',
          icon: <RunningIcon />
        };
      
      case 'paused':
        return {
          label: status,
          color: 'secondary',
          icon: <PausedIcon />
        };
      
      case 'stopped':
        return {
          label: status,
          color: 'default',
          icon: <StoppedIcon />
        };
      
      default:
        return {
          label: status,
          color: 'default',
          icon: <PendingIcon />
        };
    }
  };

  const config = getStatusConfig(status);

  return (
    <Chip
      icon={config.icon}
      label={config.label}
      color={config.color}
      variant={variant}
      size={size}
      sx={{
        fontWeight: 500,
        '& .MuiChip-icon': {
          fontSize: '1rem'
        }
      }}
    />
  );
};

export default StatusChip;
