import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';

import { authApi } from './api/authApi';
import { circlesApi } from './api/circlesApi';
import authSlice from "./slices/authSlice";

const store = configureStore({
    reducer: {
        [authApi.reducerPath]: authApi.reducer,
        [circlesApi.reducerPath]: circlesApi.reducer,
        auth: authSlice,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(authApi.middleware, circlesApi.middleware),
});

setupListeners(store.dispatch);

export default store;