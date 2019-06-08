import axios from 'axios';
import {authHeader} from './auth';
import {store} from '../store/store'
import {authActions} from "../store/actions";
import {errorHandler} from "helpers/errorHandler";

export const http = axios.create({
    baseURL: '/api',
    headers: {'Content-Type': 'application/json'},
});

http.interceptors.request.use(
    function (config) {
        const token = authHeader();
        if (!token) {
            console.log("Token required!");
            store.dispatch(authActions.logout());
        }
        config.headers = {...token, 'Content-Type': 'application/json'};
        return config;
    },
    function (error) {
        console.log(error);
        return Promise.reject(error);
    }
);


// init http request => error => invalid token => refresh the token => retry the init request
http.interceptors.response.use(
    response => response,
    error => {
        // If token has expired then refresh the token using refreshToken
        if (error.config && error.response) {

            if (error.response.status === 401) {
                console.log('Refreshing Token...');

                // get new token
                return axios.post(`/api/auth/refresh`, null, {
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('refresh'),
                        'Content-Type': 'application/json'
                    },
                }).then(res => {

                    // Set new access token
                    localStorage.setItem("token", res.data.data.token);

                    // Make sure to remove the /api because it is by in http instance by default
                    error.config.baseURL = "";

                    // update the old request with the new token
                    error.config.headers.Authorization = 'Bearer ' + res.data.data.token;
                    return axios.request(error.config)
                        .then(res => res)
                        .catch(error => Promise.reject({...error, isRetry: true}));
                }).catch(error => {
                    // error: error from token refresher || error from retry request

                    // I need to logout if there is an error with token refresher ONLY
                    if (!error.isRetry) {
                        // we will catch the token refresher errors
                        console.log('Axios Unauthorised', error);
                        store.dispatch(authActions.logout());
                    }
                    return Promise.reject(error);
                });
            }

            if (error.response.status === 500) {
                console.log('there is an error and going to notify Sentry');
                errorHandler(error);
                return;
            }

            if (error.request.responseURL.includes('assistants')) {
                console.log('there is an error with Assistants and will notify Sentry');
                errorHandler(error);
                return;
            }

        } else
            return Promise.reject(error);
    }
);
