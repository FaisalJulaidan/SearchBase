import { authConstants } from '../../constants';
import { history, http } from '../../helpers';
import { authService } from '../services';


const login = (email, password) => {
    return dispatch => {
        // Start
        dispatch(request());
        http.post(`/api/auth`, {email, password})
        .then(res => {
            // Success
            console.log("Success Login Service: ", res);
            const user = res.data.data.user
            // login successful if there's a jwt token in the response
            if (res.data.data.user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }
            dispatch(success(user));
            history.push('/dashboard');
        }).catch(error => {
            // Error
            console.log(error.response.data);
            dispatch(failure(error.response.data));

        });
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