// React
import React from 'react';
import { connect } from 'react-redux';
// Constants
import * as messageTypes from '../../constants/MessageType';
// Actions
import { addBotMessage, addUserMessage, setChatbotAnimation, setChatbotStatus } from '../../store/actions';
// Styles
import './UserInputs/styles/Inputs.css';
// Components
import { DatePicker, FileUpload, MultiDatePicker, SalaryPicker, Text } from './UserInputs';


const Input = ({ setChatbotStatus, hideSignature, addUserMessage, lastMessage, addBotMessage, setChatbotAnimation, visible }) => {

    const submitMessage = (text, type, newState, afterMessage, block, content) => {
        addUserMessage(text, type, block, content);
        _checkAfterMessage(afterMessage, newState, messageTypes.TEXT);

    };

    const _checkAfterMessage = (afterMessage, newState, type) => {
        if (afterMessage) {
            setChatbotStatus({ ...newState, afterMessage });
        } else {
            setChatbotStatus(newState);
        }
    };

    const addStatus = (component, message) => {
        return React.cloneElement(component, { setChatbotStatus, submitMessage, message });
    };

    const getInput = (message) => {
        switch (message.type) {
            case messageTypes.FILE_UPLOAD:
                return <FileUpload/>;
            case messageTypes.SALARY_PICKER:
                return <SalaryPicker block_min={message.block.Content.min}
                                     block_max={message.block.Content.max}
                                     period={message.block.Content.period}
                                     currency={message.block.Content.currency}
                />;
            case messageTypes.DATE_PICKER:
                return message.block.Content.type === 'Exact' ? <DatePicker/> : <MultiDatePicker/>;
            case messageTypes.USER_INPUT:
                return <Text/>;
            default:
                return null;
        }
    };

    if (lastMessage) {
        const component = getInput(lastMessage);
        if (visible === false && component) {
            setChatbotAnimation({ inputOpen: true });

        } else if (!component && visible === true) {
            setChatbotAnimation({ inputOpen: false });
        }
        return (
            <>
                {
                    component ?
                        (<div id={'TheSearchBase_Chatbot_Input'} className={[
                            hideSignature ? 'WithOutSignature' : null,
                            'Input',
                            visible ? 'Visible' : ''
                        ].join(' ')}>
                            {addStatus(component, lastMessage)}
                        </div>) : null
                }
            </>
        );
    }
    return null;

};

const mapStateToProps = (state) => ({
    lastMessage: state.messages.messageList[state.messages.messageList.length - 1]
});

export default connect(mapStateToProps, {
    setChatbotAnimation,
    setChatbotStatus,
    addUserMessage,
    addBotMessage
})(Input);
