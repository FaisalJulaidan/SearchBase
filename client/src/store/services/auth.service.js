import { http } from '../../helpers';

const login = (email, password) =>{
    return http.post(`/api/auth`, {email, password})
        .then(res => {
            console.log("Success Login Service: ", res);
            const user = res.data.data.user
            // login successful if there's a jwt token in the response
            if (res.data.data.user.token) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
            }
            return user;
        }, error => {
            console.log(error.response.data);
            return Promise.reject(error.response.data);
        });
}

const logout = () => {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

export const authService = {
    login,
    logout
};
