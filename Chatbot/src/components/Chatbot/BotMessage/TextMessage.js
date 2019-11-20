import React from 'react';

import URLParser from '../../helpers/URLParser';
import './styles/TextMessage.css';
import { Button } from 'antd';

const TextMessage = ({ key, text, responded, skipResponse, skipText, skippable }) => {

    // Create the skip button if Skippable is set as true
    let skipBtn = skippable ?
        (<Button block data-warning="true"
                 disabled={responded}
                 className={['Button', 'Danger', 'SkipButton'].join(' ')}
                 onClick={skipResponse}>
            {skipText}
        </Button>) : null;
    return (
        <>
            <p><URLParser>{text}</URLParser></p>
            {skipBtn}
        </>
    );
};

export default TextMessage;
