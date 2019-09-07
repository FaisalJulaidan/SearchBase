import './bootstrap.css'
import React from 'react';
import ReactGA from 'react-ga';
import Routes from './routes'
import ScrollToTop from "./hoc/scroll-to-top/ScrollToTop"
ReactGA.initialize('UA-70419779-2');
ReactGA.pageview(window.location.pathname + window.location.search);
const Home = () => {
    return (
        <ScrollToTop>
            <Routes/>
        </ScrollToTop>
    )
};
export default Home