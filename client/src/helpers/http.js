import axios from 'axios';
import {authHeader} from './auth';
import { store } from '../store/store'
import { authActions } from "../store/actions";

export const http = axios.create({
    baseURL: '/api',
    headers: {'Content-Type': 'application/json'},
});

http.interceptors.request.use(
    function (config) {
        const header = authHeader();
        if (!header) {
            console.log("Token required!");
            store.dispatch(authActions.logout());
        }
        config.headers = header;
        return config;
    },
    function (error) {
        console.log(error);
        return Promise.reject(error);
    }
);

http.interceptors.response.use(response => {
    return response;
    }, error => {
        // If token has expired then refresh the token using refreshToken
        if (error.config && error.response && error.response.status === 401) {
            console.log('Refresh Token...');
            return axios.post(`/api/auth/refresh`, null,{
                headers: {'Authorization': 'Bearer ' + localStorage.getItem('refresh')},
            }).then(res => {
                // Set new access token
                const {token, expiresIn} = res.data.data;
                localStorage.setItem("token", token);
                localStorage.setItem("expiresIn", expiresIn);
                // Make sure to remove the /api because it is by in http instance by default
                error.config.baseURL="";
                // Retry the request with the new token
                return http.request(error.config)
            }).catch(error => {
                console.log('Axios Unauthorised');
                store.dispatch(authActions.logout());
            });
        }
    return Promise.reject(error);
    }
);