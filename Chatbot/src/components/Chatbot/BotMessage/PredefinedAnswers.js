import React from 'react';
import PropTypes from 'prop-types';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Question.css';
// Components
import { Button } from 'antd';
import URLParser from '../../helpers/URLParser';

const PredefinedAnswers = ({ answers, question, submitAnswer, responded, skipResponse, skippable, skipText }) => {

    const clickAnswer = (key) => {
        let answer = answers.filter((a, i) => i === key)[0]; // selected answer
        let afterMessage = answer[flowAttributes.QUESTION_ANSWERS_AFTER_MESSAGE];
        let newState = {
            curAction: answer[flowAttributes.QUESTION_ANSWERS_ACTION],
            curBlockID: answer[flowAttributes.QUESTION_ANSWERS_BLOCKTOGOID],
            waitingForUser: false
        };
        submitAnswer(
            answer[flowAttributes.QUESTION_ANSWERS_TEXT],
            messageTypes.TEXT,
            newState,
            { skipped: false, selectedAnswer: answer, otherAnswers: answers },
            afterMessage
        );
    };

    const answersButtons = [];

    answers.forEach((answer, i) => {
        answersButtons.push(
            <Button block disabled={responded} onClick={() => clickAnswer(i)} key={i}>
                {answer.text}
            </Button>
        );
    });

    // Add the skip button if the question is skippable
    if (skippable) {
        answersButtons.push(
            <Button block data-danger="true" type="danger" disabled={responded} onClick={skipResponse}  key={99}>
                {skipText}
            </Button>
        );
    }


    return (
        <>
            <p><URLParser>{question}</URLParser></p>
            <div className={'Question'}>
                {answersButtons}
            </div>
        </>
    );
};

PredefinedAnswers.propTypes = {
    answers: PropTypes.array,
    question: PropTypes.string,
    setChatbotStatus: PropTypes.func,
    addUserMessage: PropTypes.func
};

export default PredefinedAnswers;
