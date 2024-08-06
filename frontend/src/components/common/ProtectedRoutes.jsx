import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth.js";

const ProtectedRoutes = () => {
  const { isAuthenticated, isInitialized } = useAuth();

  if (!isInitialized) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoutes;