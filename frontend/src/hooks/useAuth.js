import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { initializeAuthState } from '../slices/authSlice';

export const useAuth = () => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    dispatch(initializeAuthState());
    setIsInitialized(true);
  }, [dispatch]);

  return { isAuthenticated, isInitialized };
};