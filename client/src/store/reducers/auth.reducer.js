import { authConstants } from '../../constants';
import { updateObject } from '../utility';

let user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? { isAuthenticated: true, user, isLoggingIn: false, errorMsg: '' } : 
                            { isAuthenticated: false, user: null, isLoggingIn: false, errorMsg: ''};


export const auth = (state = initialState, action) => {
  switch (action.type) {
    case authConstants.LOGIN_REQUEST:
      return updateObject(state, {
        isLoggingIn: true,
        errorMsg: ''
      });
    case authConstants.LOGIN_SUCCESS:
      return updateObject(state, {
        isLoggingIn: false,
        isAuthenticated: true,
        user: action.user,
        errorMsg: ''
      });
    case authConstants.LOGIN_FAILURE:
      return updateObject(state, {
        isLoggingIn: false,
        isAuthenticated: false,
        user: null,
        errorMsg: action.error.msg
      });
    case authConstants.LOGOUT:
      return updateObject(state, {
        isLoggingIn: false,
        isAuthenticated: false,
        user: null,
        errorMsg: ''
      });
    default:
      return state
  }
}