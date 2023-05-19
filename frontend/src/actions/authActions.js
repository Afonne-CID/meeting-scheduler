import { 
  AUTH_ERROR,
  LOGIN_SUCCESS,
  LOGOUT_SUCCESS,
  REGISTER_SUCCESS,
} from '../constants/actionTypes';
import { 
  login as apiLogin, 
  register as apiRegister 
} from '../services/api';

export const authError = (error) => ({
  type: AUTH_ERROR,
  payload: error,
});

export const loginSuccess = (user) => ({
  type: LOGIN_SUCCESS,
  payload: user,
});

export const logoutSuccess = () => ({
  type: LOGOUT_SUCCESS,
});

export const registerSuccess = (user) => ({
  type: REGISTER_SUCCESS,
  payload: user,
});

export const register = (credentials) => async (dispatch) => {
  return apiRegister(credentials)
    .then((response) => {
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      dispatch(registerSuccess(response.user));
    })
    .catch((error) => {
      dispatch(authError(error.toString()))
    });
};

export const login = (credentials) => async (dispatch) => {
  return apiLogin(credentials)
    .then((response) => {
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      dispatch(loginSuccess(response.user));
    })
    .catch((error) => {
      dispatch(authError(error.toString()))
    });
};

export const logout = () => (dispatch) => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  dispatch(logoutSuccess());
};