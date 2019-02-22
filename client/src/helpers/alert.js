import {message, notification} from 'antd';

const duration = 2.5;
const placement = "topRight";

export const alertSuccess = (title, message) => {
    notification.success({
        message: title,
        description: message,
        duration: duration,
        placement: placement,
    });
};


export const alertError = (title, message) => {
    notification.error({
        message: title,
        description: message
    });
};

export const loadingMessage = (title, time = 1.5) => message.loading(title, time);
export const sucessMessage = (title, time = 1.5) => message.success(title, time);

export const destroyMessage = () => {
    message.destroy();
    notification.destroy();
};

export const alertInfo = (title, message) => {
    notification.info({
        message: title,
        description: message,
        duration: duration,
        placement: placement,
    });
};


export const alertWarn = (title, message) => {
    notification.warn({
        message: title,
        description: message,
        duration: duration,
        placement: placement,
    });
};