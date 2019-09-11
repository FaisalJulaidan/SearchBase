import * as constants from '../constants/Constants';
import uuid from 'uuid/v4';


const isReady = (chatbot) => {
    return !chatbot.status.loading && !chatbot.status.finished;
};

const getLink = (src) => {
    // include the colon if there is port number, which means localhost and not real server
    let colon = '';
    if (window.location.port !== '')
        colon = ':';

    const { protocol, port, hostname } = window.location;
    return protocol + '//' + hostname + colon + port + src;
};

const getServerDomain = () => {
    const env = process.env.REACT_APP_ENV;
    if (env === 'development')
        return 'http://localhost:5000';
    else if (env === 'staging')
        return 'http://staging.thesearchbase.com';
    else if (env === 'production')
        return 'https://www.thesearchbase.com';
    return undefined;
};

const optionalDelayExecution = (cb, delay, time) => {
    let timeout;
    if (delay) {
        timeout = setTimeout(cb, time);
    } else {
        cb();
    }
    const reset = () => clearTimeout(timeout);
    return { reset };
};

const createBlock = (Content, Type, delay, ID = null, DataType = null, selfContinue = null, extra = {}, deferredAction = null) => ({
    Content,
    Type,
    DataType,
    ID,
    delay,
    selfContinue,
    extra
});

const delayMessageLength = (message) => {
    if (message) {
        let delay = message.length * constants.BOT_DELAY_CHAR_MULTIPLIER;
        if (delay > constants.BOT_DELAY_MAX) {
            delay = constants.BOT_DELAY_MAX;
        } else if (delay < constants.BOT_DELAY_MIN) {
            delay = constants.BOT_DELAY_MIN;
        }
        return delay;
    } else {
        return 0;
    }

};

export const genUniqueFileName = (file) => uuid() + "." + file.name.split('.').splice(-1)[0];

export { isReady, getServerDomain, optionalDelayExecution, createBlock, delayMessageLength, getLink };

export * from './flowHandler';
export * from './dataHandler';
export * from './hooks';
export * from './validators';
export * from './wrappers';
