import 'react-app-polyfill/ie11';
import 'react-app-polyfill/stable';
import smoothscroll from 'smoothscroll-polyfill';
// import 'babel-polyfill';


import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';
import {Provider} from 'react-redux';
import WebFont from 'webfontloader';
import Chatbot from './components/Chatbot/Chatbot';
import Store from '../src/store/store'


// kick off the polyfill!
smoothscroll.polyfill();


WebFont.load({ google: { families: ['Source Sans Pro', 'sans-serif'] } });

const scriptTag = document.querySelector('script[data-name="tsb-widget"][data-id]');
const isDirectLink = scriptTag.getAttribute('directLink') === '';
const assistantID = scriptTag.getAttribute('data-id');
const loadByDefault = scriptTag.getAttribute('data-load');
const btnColor = scriptTag.getAttribute('data-circle') || '#1890ff';

let root = document.createElement('div');
root.setAttribute('id', 'TheSearchBase_Chatbot');
root.setAttribute('style', 'background:none');

if (isDirectLink)
    document.getElementById('direct_link_container').appendChild(root);
else
    document.body.appendChild(root);

ReactDOM.render(
    <Provider store={Store}>
        <Chatbot root={root}
                 isDirectLink={isDirectLink} btnColor={btnColor}
                 loadByDefault={loadByDefault}
                 assistantID={assistantID}/>
    </Provider>, root
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
