import { 
  CLEAR_ERROR,
  CLEAR_SUCCESS,
  AUTH_ERROR,
  LOGIN_SUCCESS, 
  LOGOUT_SUCCESS,
  REGISTER_SUCCESS,
} from '../constants/actionTypes';

const initialState = {
  isAuthenticated: !!localStorage.getItem('token'),
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
  error: null,
  success: null,
};

export default function authReducer(state = initialState, action) {
  switch (action.type) {
    case REGISTER_SUCCESS:
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        success: 'User registered successfully!',
        error: null,
      };
    case LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
        success: 'Logged in successfully!',
        error: null,
      };
    case LOGOUT_SUCCESS:
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        success: 'Logged out successfully!',
        error: null,
      };
    case AUTH_ERROR:
      return {
        ...state,
        error: action.payload,
        success: null, // clear success message on error
      };
    case CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    case CLEAR_SUCCESS:
      return {
        ...state,
        success: null,
      };
    default:
      return state;
  }
}
