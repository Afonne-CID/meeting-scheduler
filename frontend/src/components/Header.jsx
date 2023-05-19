// Header.jsx
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import { logout } from '../actions/authActions';

const Header = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const user = useSelector(state => state.auth.user) || {};

  const handleLogout = () => {
    dispatch(logout());
  }

  return (
    <div className='text-right justify-right my-4'>
      <div className=''>
        <Button 
          onClick={() => navigate('/dashboard')} 
          color="blue-500" 
          extraClasses={`justify-right mr-4`}>
            {'<-'} Home
        </Button>
        <Button 
          onClick={() => handleLogout()} 
          color="red-500" 
          extraClasses={`justify-right`}>
            Logout
        </Button>
      </div>
      {user && (
        <div className='flex justify-end'> 
          <p className='m-2 p-2 bg-blue-100 rounded px-2'>{user.email}</p>
        </div>
      )}
    </div>
  );
};

export default Header;
