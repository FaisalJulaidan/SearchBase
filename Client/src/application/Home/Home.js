import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter} from "react-router-dom";

import Routes from './routes'
import ScrollToTop from "./hoc/scroll-to-top/ScrollToTop";

const Home = () => {
    return (
        <BrowserRouter>
            <ScrollToTop>
                <Routes/>
            </ScrollToTop>
        </BrowserRouter>
    )
};


ReactDOM.render(<Home/>, document.getElementById('root'));
