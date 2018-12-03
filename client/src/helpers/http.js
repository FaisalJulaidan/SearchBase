import axios from 'axios';
import {authHeader} from './authHeader';


export const http = axios.create({
    headers: {'Content-Type': 'application/json'},
});

http.interceptors.request.use(
    function (config) {
        const header = authHeader();
        if (header) config.headers.Authorization = header;
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);
