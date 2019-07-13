import React, { useEffect, useState } from 'react';
// Constants
import * as flowAttributes from '../../../constants/FlowAttributes';
import * as messageTypes from '../../../constants/MessageType';
// Utils
import { delayMessageLength } from '../../../utils';
// Style
import './styles/BotMessage.css';
// Components
import Question from './Question';
import TextMessage from './TextMessage';
import Solutions from './Solutions';

const BotMessage = ({ type, message, addUserMessage, addBotMessage, setChatbotStatus, index, active }) => {
    let [responded, setResponded] = useState(false);
    let [skip, setSkip] = useState({skipText: false, skippable: false});

    const _checkAfterMessage = (afterMessage, newState, type) => {
        if (afterMessage) {
            setChatbotStatus({ thinking: true });
            setTimeout(() => {
                addBotMessage(afterMessage, type);
                setChatbotStatus(newState);
            }, delayMessageLength(afterMessage));
        } else {
            setChatbotStatus(newState);
        }
    };

    const skipResponse = () => {
        let { block } = message;
        const text = block[flowAttributes.SKIP_TEXT];
        const newState = {
            curAction: block[flowAttributes.SKIP_ACTION],
            curBlockID: block[flowAttributes.SKIP_BLOCKTOGOID],
            waitingForUser: false
        };
        setResponded(true);
        addUserMessage(text, messageTypes.TEXT, message.block, {input: text, skipped:true});
        setChatbotStatus(newState);
    };

    const submitAnswer = (text, type, newState, content, afterMessage) => {
        addUserMessage(text, type, message.block, content);
        _checkAfterMessage(afterMessage, newState, messageTypes.TEXT);
        setResponded(true);
    };


    const submitSolution = (text, type, content, skip = false) => {
        const { block } = message;
        addUserMessage(text, type, block, content);
        const afterMessage = block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
        let newState = {
            curAction: block[flowAttributes.CONTENT][flowAttributes.SOLUTION_ACTION],
            curBlockID: block[flowAttributes.CONTENT][flowAttributes.SOLUTION_BLOCKTOGOID],
            waitingForUser: false
        };
        _checkAfterMessage(afterMessage, newState, messageTypes.TEXT);
        setResponded(true);
    };

    useEffect(() => {
        let { block } = message;
        // in case for afterMessage which does not have a block
        if (block) setSkip({skipText: block[flowAttributes.SKIP_TEXT], skippable: block[flowAttributes.SKIPPABLE]});
    }, [message]);

    useEffect(() => {
        if (active) {
            setResponded(!active);
        }
    }, [active]);


    const addStatus = (component) => {
        return React.cloneElement(component, { responded, skipResponse, skipText: skip.skipText, skippable: skip.skippable });
    };

    const findMessageType = (type, message) => {
        let { block } = message;
        switch (type) {
            case messageTypes.TEXT:
            case messageTypes.USER_INPUT:
            case messageTypes.FILE_UPLOAD:
            case messageTypes.RAW_TEXT:
                return (
                    <TextMessage
                        key={message.index}
                        text={message.text}
                    />);
            case messageTypes.QUESTION:
                return (
                    <Question
                        submitAnswer={submitAnswer}
                        key={message.index}
                        answers={message.block[flowAttributes.CONTENT][flowAttributes.QUESTION_ANSWERS]}
                        question={message.block[flowAttributes.CONTENT][flowAttributes.QUESTION_TEXT]}/>);
            case messageTypes.SOLUTIONS:
                return (<Solutions
                    solutions={block.fetchedData.solutions}
                    submitSolution={submitSolution}
                    afterMessage={message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE]}/>);

            default:
        }
    };

    return (
        <div className={['Message', type === messageTypes.SOLUTIONS ? 'Solution' : null].join(' ')}>
            {addStatus(findMessageType(type, message, index))}
        </div>
    );
};

export default BotMessage;