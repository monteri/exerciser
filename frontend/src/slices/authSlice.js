import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  isAuthenticated: false,
  token: '',
  refreshToken: '',
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (state, action) => {
      localStorage.setItem('token', action.payload.token);
      localStorage.setItem('refresh_token', action.payload.refreshToken);
      state.isAuthenticated = true;
      state.token = action.payload.token;
      state.refreshToken = action.payload.refreshToken;
    },
    logout: (state) => {
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      state.isAuthenticated = false;
      state.token = '';
      state.refreshToken = '';
    },
    initializeAuthState: (state) => {
      const token = localStorage.getItem('token');
      const refreshToken = localStorage.getItem('refresh_token');
      if (token && refreshToken) {
        state.isAuthenticated = true;
        state.token = token;
        state.refreshToken = refreshToken;
      }
    },
  },
});

export const { setCredentials, logout, initializeAuthState } = authSlice.actions;
export default authSlice.reducer;