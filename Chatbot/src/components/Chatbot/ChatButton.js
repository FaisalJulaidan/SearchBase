import React from 'react';

// Styles
import './styles/ChatButton.css';
import  './styles/Animations.css';

// Components
import { Button, Icon } from 'antd';

const Header = ({ loading, disabled, openWindow, btnColor }) => {

    const styling = {
        width: '50px',
        height: '50px',
        boxShadow: '0px 2px 20px -4.5px #666',
        backgroundColor: btnColor,
        borderColor: btnColor,
        padding: '0 !important'
    };

    return (
        <div className={`${'Chatbot_Button'} ${'BounceIn'}`}>
            <Button
                onClick={openWindow}
                type="primary"
                shape="circle"
                size="large"
                ghost={disabled}
                disabled={disabled}
                loading={loading}
                style={styling}
            >
                {!loading && <Icon type="message" theme="outlined" style={{ fontSize: '25px', margin: '11px 2px' }}/>}
            </Button>
        </div>
    );
};

export default Header;
