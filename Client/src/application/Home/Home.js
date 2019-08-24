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
    return (
        <Provider store={store}>
            <Router history={history}>
                <ScrollToTop>
                    <Routes/>
                </ScrollToTop>
            </Router>
        </Provider>
    )
};


ReactDOM.render(<Home/>, document.getElementById('root'));
