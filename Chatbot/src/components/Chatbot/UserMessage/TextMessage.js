import React from 'react';

import URLParser from '../../helpers/URLParser'

const TextMessage = ({ text }) => {
    return (<p><URLParser>{text}</URLParser></p>);
};

export default TextMessage;