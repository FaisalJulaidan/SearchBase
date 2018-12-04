import axios from 'axios';
import {authHeader} from './authHeader';


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
        console.log(error)
        return Promise.reject(error);
    }
);
