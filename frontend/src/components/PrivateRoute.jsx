import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { nodeType } from '../utils/propTypes';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = useSelector(state => state.auth.isAuthenticated);

  return isAuthenticated ? children 
    : <Navigate to="/login" replace state={{ from: location.pathname }} />;
}

PrivateRoute.propTypes = {
  children: nodeType,
};

export default PrivateRoute;
