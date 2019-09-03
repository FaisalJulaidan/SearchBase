import React from 'react';
import ReactDOM from 'react-dom';
import './bootstrap.css'
import {Router} from 'react-router-dom';
import {Provider} from 'react-redux';
import Routes from './routes'
import {history} from '../../helpers'
import ScrollToTop from "./hoc/scroll-to-top/ScrollToTop";
import {store} from "../../store/store";
import ReactGA from 'react-ga';

ReactGA.initialize('UA-70419779-2');
ReactGA.pageview(window.location.pathname + window.location.search);
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
