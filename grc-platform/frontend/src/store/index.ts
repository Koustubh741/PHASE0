/**
 * Redux Store Configuration
 * 
 * This file configures the Redux store for the GRC Platform frontend.
 * It combines all feature reducers and applies middleware.
 */

import { configureStore } from '@reduxjs/toolkit';
import { authSlice } from '../features/auth/slice';
import { dashboardSlice } from '../features/dashboard/slice';
import { policiesSlice } from '../features/policies/slice';
import { risksSlice } from '../features/risks/slice';
import { complianceSlice } from '../features/compliance/slice';
import { workflowsSlice } from '../features/workflows/slice';
import { aiAgentsSlice } from '../features/ai-agents/slice';

export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
    dashboard: dashboardSlice.reducer,
    policies: policiesSlice.reducer,
    risks: risksSlice.reducer,
    compliance: complianceSlice.reducer,
    workflows: workflowsSlice.reducer,
    aiAgents: aiAgentsSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
