import React from 'react'
import ReactDOM from 'react-dom'
import Chatbot from './components/Chatbot/Chatbot'
import WebFont from 'webfontloader';
import 'antd/lib/button/style';
import {Provider} from 'react-redux';
import {createStore} from 'redux';
import reducer from './store/reducer';
import 'react-app-polyfill/ie11';

if (!String.prototype.startsWith) {
    String.prototype.startsWith = function(searchString, position) {
        position = position || 0;
        return this.indexOf(searchString, position) === position;
    };
}

Object.defineProperty(Array.prototype, 'flat', {
    value: function(depth = 1) {
        return this.reduce(function (flat, toFlatten) {
            return flat.concat((Array.isArray(toFlatten) && (depth>1)) ? toFlatten.flat(depth-1) : toFlatten);
        }, []);
    }
});

const store = createStore(reducer);
WebFont.load({
    google: {
        families: ['Source Sans Pro', 'sans-serif']
    }
});

const app = (
    <Provider store={store}>
        <Chatbot height={'600px'} width={'400px'}/>
    </Provider>
);

const root = document.createElement('div');
root.id = "TheSearchBase_Chatbot";

const waitFor = object => {
    Boolean(object) ? object.appendChild(root) : setTimeout(() => waitFor(document.body), 500);
};

const scriptTag = document.querySelector('script[data-name="tsb-widget"][data-id]');
const isDirectLink = scriptTag.getAttribute('data-directLink') === '';

if (!document.body)
    waitFor(document.body);
else {

    if (isDirectLink) {
        document.getElementById('directlink').appendChild(root);
    } else {
        document.body.appendChild(root);
    }
}



ReactDOM.render(app, root);
