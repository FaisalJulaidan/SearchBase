// React
import React from 'react';
import { connect } from 'react-redux';
// Constants
import * as messageTypes from '../../constants/MessageType';
import * as flowAttributes from '../../constants/FlowAttributes';
import * as constants from '../../constants/Constants';
// Utils
import { delayMessageLength } from '../../utils';
// Actions
import { addBotMessage, addUserMessage, setChatbotAnimation, setChatbotStatus } from '../../store/actions';
// Styles
import './UserInputs/styles/Inputs.css';
// Components
import { DatePicker, FileUpload, SalaryPicker, Text } from './UserInputs';


const Input = ({ setChatbotStatus, isDirectLink, addUserMessage, lastMessage, addBotMessage, setChatbotAnimation, visible }) => {

    const submitMessage = (text, type, newState, afterMessage, block, content) => {
        addUserMessage(text, type, block, content);
        if (afterMessage) {
            setChatbotStatus({ thinking: true });
            setTimeout(() => {
                addBotMessage(afterMessage, messageTypes.TEXT);
                setChatbotStatus({ ...newState, thinking: false });
            }, delayMessageLength(afterMessage));
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
                return (<FileUpload/>);
            case messageTypes.USER_INPUT:
                switch (message.block[flowAttributes.DATA_TYPE][flowAttributes.DATA_TYPE_VALIDATION]) {
                    case constants.SALARY:
                        return (<SalaryPicker/>);
                    case constants.DATEPICKER:
                        return (<DatePicker/>);
                    default:
                        return (<Text/>);
                }
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
                        (<div className={[
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