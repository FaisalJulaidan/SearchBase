import { authConstants } from '../../constants';
import { history } from '../../helpers';
import { authService } from '../services';

const login = (email, password) => {
    return dispatch => {
        dispatch(request());

        authService.login(email, password)
            .then(
                user => { 
                    dispatch(success(user));
                    history.push('/dashboard');
                },
                error => {
                    dispatch(failure(error));
                }
            );
    };

    function request() { return { type: authConstants.LOGIN_REQUEST} }
    function success(user) { return { type: authConstants.LOGIN_SUCCESS, user } }
    function failure(error) { return { type: authConstants.LOGIN_FAILURE, error } }
}

const logout = () => {
    authService.logout();
    return { type: authConstants.LOGOUT };
}

export const authActions = {
    login,
    logout
};