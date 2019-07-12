import * as constants from '../constants/Constants';

const isReady = (chatbot) => {
    return !chatbot.status.loading && !chatbot.status.finished;
};

const getServerDomain = () => {
    const env = process.env.NODE_ENV;
    if (env === 'development')
        return 'http://localhost:5000';
    else if (env === 'staging')
        return 'http://staging.thesearchbase.com';
    else if (env === 'production')
        return 'https://thesearchbase.com';
    return undefined;
};

const optionalDelayExecution = (cb, delay, time) => {
    let timeout;
    if (delay) {
        timeout = setTimeout(cb, time);
    } else {
        cb();
    }
    return timeout;
};

const createBlock = (Content, Type, delay, ID = null, DataType = null, selfContinue = null, extra = {}) => ({
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


export { isReady, getServerDomain, optionalDelayExecution, createBlock, delayMessageLength };

export * from './flowHandler';
export * from './dataHandler';
export * from './hooks';
export * from './validators';
export * from './wrappers';