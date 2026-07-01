import { Navigate, useLocation } from "react-router-dom";
import { useStudentAuth } from "../../context/StudentAuthContext";

/**
 * Wraps every /student/* page except login/register. Anyone without a
 * valid student token is bounced to /student/login.
 */
export default function StudentProtectedRoute({ children }) {
  const { isAuthenticated } = useStudentAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/student/login" replace state={{ from: location }} />;
  }

  return children;
}
