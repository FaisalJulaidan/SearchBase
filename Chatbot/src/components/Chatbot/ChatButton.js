import React from 'react';
// Styles
import './styles/ChatButton.css';
import './styles/Animations.css';
// Components
import { Button, Icon } from 'antd';

const Header = ({ loading, active, openWindow, btnColor, position }) => {

    const styling = {
        width: '50px',
        height: '50px',
        boxShadow: '0px 2px 20px -4.5px #666',
        backgroundColor: btnColor,
        borderColor: btnColor
    };

    return (
        <div className={`${'Chatbot_Button'} ${'BounceIn'} ${position}`}>
            <Button
                onClick={openWindow}
                type="primary"
                shape="circle"
                size="large"
                ghost={!active}
                disabled={!active}
                loading={loading}
                style={styling}>
                {!loading && <Icon type="message" theme="outlined" style={{ fontSize: '25px', margin: '11px 2px' }}/>}
            </Button>
        </div>
    );
};

export default Header;
