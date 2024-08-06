import { fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { logout, setCredentials } from '../slices/authSlice';
import { Mutex } from 'async-mutex';

const baseUrl = import.meta.env.VITE_API_URL;

const mutex = new Mutex();

const baseQuery = fetchBaseQuery({
  baseUrl: `${baseUrl}/api`,
  prepareHeaders: (headers, { getState }) => {
    const token = localStorage.getItem('token');
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  },
});

const baseQueryWithReauth = async (args, api, extraOptions) => {
  await mutex.waitForUnlock();
  let result = await baseQuery(args, api, extraOptions);
  if (result.error && result.error.status === 401) {
    if (!mutex.isLocked()) {
      const release = await mutex.acquire();
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const refreshResult = await baseQuery(
            {
              url: 'auth/refresh/',
              method: 'POST',
              body: { refresh: refreshToken },
            },
            api,
            extraOptions
          );
          if (refreshResult.data) {
            api.dispatch(setCredentials({
              token: refreshResult.data.access_token,
              refreshToken: refreshToken,
            }));
            result = await baseQuery(args, api, extraOptions);
          } else {
            api.dispatch(logout());
          }
        } else {
          api.dispatch(logout());
        }
      } finally {
        release();
      }
    } else {
      await mutex.waitForUnlock();
      result = await baseQuery(args, api, extraOptions);
    }
  }
  return result;
};

export default baseQueryWithReauth;