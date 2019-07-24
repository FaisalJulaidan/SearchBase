import * as constants from '../constants/Constants';

const isValidEmail = email => {
    return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(.\w{2,3})+$/.test(email);
};

const isValidTelephone = telephone => {
    return /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/.test(
        telephone
    );
};

const isValidURL = URL => {
    return /[-a-zA-Z0-9@:%_+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_+.~#?&//=]*)?/.test(
        URL
    );
};

const isValidString = input => {
    return isNaN(input);
};

const isValidNumber = number => {
    return !isNaN(number);
};

const isValidFile = (file, types) => {
    const type = file.name.split('.').splice(-1)[0];
    return types.includes(type);
    //JPEG - JPG FIX?
};

export const validate = (content, type) => {
    let valid, error;
    switch (type) {
        case constants.EMAIL:
            valid = isValidEmail(content.input);
            error = valid ? null : 'Invalid email address';
            break;
        case constants.TELEPHONE:
            valid = isValidTelephone(content.input);
            error = valid ? null : 'Invalid phone number';
            break;
        case constants.STRING:
            valid = isValidString(content.input);
            error = valid
                ? null
                : 'Please enter either an Alphanumeric or Alphabetic string';
            break;
        case constants.NUMBER:
            valid = isValidNumber(content.input);
            error = valid ? null : 'Please enter only numbers.';
            break;
        case constants.SALARY:
            valid = true;
            break;
        case constants.URL:
            valid = isValidURL(content.input);
            error = valid ? null : 'Invalid URL';
            break;
        case constants.FILE:
            valid = isValidFile(content.input, content.fileTypes);
            error = valid ? null : 'Allowed types: ' + content.fileTypes.join(', ');
            break;
        case constants.IGNORE:
            valid = true;
            break;
        default:
            throw new Error('No type supplied!');
    }
    return { error, valid };
};
