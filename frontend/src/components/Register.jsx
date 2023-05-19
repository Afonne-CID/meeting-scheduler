import { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useLocation, useNavigate } from 'react-router-dom';
import StatusMessage from './StatusMessage';
import { register } from '../actions/authActions';
import { clearError, clearSuccess } from '../actions';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const redirectToPreviousPath = useCallback(() => {
    const from = location.state?.from || "/dashboard";
    navigate(from);
  }, [location, navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(register({ email, password }));
  };

  // Reset error and success messages
  useEffect(() => {
    dispatch(clearError());
    dispatch(clearSuccess())
}, [dispatch]); 

  // If user is already authenticated, redirect to home page
  useEffect(() => {
    if (isAuthenticated) {
        redirectToPreviousPath();
    }
  }, [isAuthenticated, navigate, redirectToPreviousPath])

  return (
    <div className={`
      min-h-screen flex items-center justify-center 
      bg-gray-50 py-12 px-4 sm:px-6 lg:px-8`}
    >
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create an account
          </h2>
        </div>
        <StatusMessage />
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input 
                id="email-address" 
                name="email" 
                type="email" 
                autoComplete="email" 
                required 
                placeholder="Email address" 
                value={email} 
                onChange={e => setEmail(e.target.value)} 
                className={`
                  appearance-none rounded-none relative block w-full px-3 
                  py-2 borderborder-gray-300 placeholder-gray-500
                   text-gray-900 rounded-t-md focus:outline-none 
                   focus:ring-indigo-500 focus:border-indigo-500 
                   focus:z-10 sm:text-sm`}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input 
                id="password" 
                name="password" 
                type="password" 
                autoComplete="current-password" 
                required 
                placeholder="Password" 
                value={password} 
                onChange={e => setPassword(e.target.value)} 
                className={`
                  appearance-none rounded-none relative block w-full px-3 
                  py-2 borderborder-gray-300 placeholder-gray-500 
                  text-gray-900 rounded-b-md focus:outline-none 
                  focus:ring-indigo-500 focus:border-indigo-500 
                  focus:z-10 sm:text-sm` }
              />
            </div>
          </div>
  
          <div>
            <button 
              type="submit" 
              className={`
                group relative w-full flex justify-center py-2 
                px-4 border border-transparent text-sm font-medium 
                rounded-md text-white bg-indigo-600 
                hover:bg-indigo-700 focus:outline-none focus:ring-2 
                focus:ring-offset-2 focus:ring-indigo-500`}
            >
              Create Account
            </button>
          </div>
        </form>
        <div 
          className='justify-center text-center'>
            Already have an account? 
            <span 
              onClick={() => navigate('/login', { state: location.state } )}
              className='text-blue-500 cursor-pointer'>
                Login Here
            </span>
        </div>
      </div>
    </div>
  );
};

export default Register;
