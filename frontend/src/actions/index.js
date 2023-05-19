import { 
    CLEAR_ERROR,
    CLEAR_SUCCESS,
  } from '../constants/actionTypes';
  
  export const clearError = () => ({
    type: CLEAR_ERROR,
  });
  
  export const clearSuccess = () => ({
    type: CLEAR_SUCCESS,
  });
  