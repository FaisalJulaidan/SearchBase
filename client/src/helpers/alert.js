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
        description: message,
        duration: duration,
        placement: placement,
    });
};

export const loadingMessage = title => message.loading(title);

export const destroyMessage = () => message.destroy();

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