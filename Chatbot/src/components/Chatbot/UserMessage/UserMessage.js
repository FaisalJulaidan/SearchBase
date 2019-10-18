import React from 'react';
import { connect } from 'react-redux';
// Constants
import * as messageTypes from '../../../constants/MessageType';
// Styles
import './styles/UserMessage.css';
// Components
import TextMessage from './TextMessage';
import { Icon, Tooltip } from 'antd';
import { getContainerElement } from '../../helpers';

const UserMessage = ({ type, message, addUserMessage, setChatbotStatus, rewind, finished }) => {
    const addStatus = (component) => {
        return React.cloneElement(component, { setChatbotStatus, addUserMessage });
    };

    const findMessageType = () => {
        switch (message.type) {
            case messageTypes.TEXT:
            case messageTypes.USER_INPUT:
            case messageTypes.FILE_UPLOAD:
                return (
                    <TextMessage
                        sender={message.sender}
                        key={message.index}
                        text={message.text}
                    />);
            default:
                return null
        }
    };

    return (
        <div className={'User'}>
            {finished ? null : <Tooltip placement={'left'}
                                        getPopupContainer={() => getContainerElement()}
                                        title="Rewind to change your answer to this question">
                <Icon type="sync" onClick={() => rewind(message.index)}/>
            </Tooltip>}
            <div className={'User_Message'}>
                {addStatus(findMessageType(type))}
            </div>
        </div>

    );
};

const mapStateToProps = (state) => ({
    finished: state.chatbot.status.finished
})

export default connect(mapStateToProps)(UserMessage);
