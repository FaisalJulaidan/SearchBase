import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import {Router} from "react-router-dom";
import './bootstrap.css'

import Routes from './routes'
import ScrollToTop from "./hoc/scroll-to-top/ScrollToTop";
import {store} from "../../store/store";
import {history} from "../../helpers";

const Home = () => {

    const injectGA = () => {
        if (typeof window == 'undefined') {
            return;
        }
        window.dataLayer = window.dataLayer || [];
        function gtag() {
            window.dataLayer.push(arguments);
        }
        gtag('js', new Date());
        gtag('config', 'UA-70419779-2');
    };

    return (
        <Provider store={store}>
            <Router history={history}>
                <script async src="https://www.googletagmanager.com/gtag/js?id=UA-70419779-2"/>
                <script>{injectGA()}</script>
                <ScrollToTop>
                    <Routes/>
                </ScrollToTop>
            </Router>
        </Provider>
    )
};


ReactDOM.render(<Home/>, document.getElementById('root'));
