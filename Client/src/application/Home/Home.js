import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import {BrowserRouter} from "react-router-dom";
import './bootstrap.css'

import Routes from './routes'
import ScrollToTop from "./hoc/scroll-to-top/ScrollToTop";
import {store} from "../../store/store";

const Home = () => {
    return (
        <Provider store={store}>
            <BrowserRouter>
                <ScrollToTop>
                    <Routes/>
                </ScrollToTop>
            </BrowserRouter>
        </Provider>
    )
};


ReactDOM.render(<Home/>, document.getElementById('root'));
