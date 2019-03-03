import axios from 'axios';
import {authHeader} from './auth';
import { store, persistor} from '../store/store'
import { authActions } from "../store/actions";

export const http = axios.create({
    baseURL: '/api',
    headers: {'Content-Type': 'application/json'},
});

http.interceptors.request.use(
    function (config) {
        const header = authHeader();
        if (!header) throw new Error('Token required!');  
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
    if (error.response.status === 401) {
        console.log('Axios Unauthorised');
        store.dispatch(authActions.logout());
    }
    return Promise.reject(error);
});