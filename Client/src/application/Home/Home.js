    import './bootstrap.css'

import React from 'react'
import Routes from './routes'
import ScrollToTop from "./hoc/scroll-to-top/ScrollToTop";
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
        <>
                <script async src="https://www.googletagmanager.com/gtag/js?id=UA-70419779-2"/>
                <script>{injectGA()}</script>
                <ScrollToTop>
                    <Routes/>
                </ScrollToTop>
        </>
    )

}

export default Home