import React, { useEffect, useRef, useState } from 'react';
// Utils
import { validate } from '../../../utils/validators';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
// Components
import { Icon, Tooltip } from 'antd';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { getContainerElement } from '../../helpers';

const Text = ({ message, submitMessage }) => {
    let [error, setError] = useState(null);
    let [valid, setValid] = useState(true);
    let [text, setText] = useState('');
    let delay = useRef(null);

    const inputHandler = e => {
        setText(e.target.value);
    };

    const validateInput = () => {
        const validation = message.block[flowAttributes.DATA_TYPE][flowAttributes.DATA_TYPE_VALIDATION];
        let validator = validate({ input: text }, validation);
        if (validator.error) {
            setValid(false);
            setError(validator.error);
        } else {
          setValid(true);
          setError(null)
        }
        return validator.error
    };

    const submitAnswer = () => {
        try {
          let error = validateInput()
          if (!error) {
              setValid(true);
              let type = messageTypes.TEXT;
              let block = message.block;
              let afterMessage = message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
              let newState = {
                  curAction: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_ACTION],
                  curBlockID: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_BLOCKTOGOID],
                  waitingForUser: false
              };
              submitMessage(text, type, newState, afterMessage, block, { input: text, skipped: false });
          }
        } catch (e) {
            console.log(e);
            // SENTRY HERE
        }
    };

    useEffect(() => {
        if (text) {
            if (delay.current) {
                clearTimeout(delay.current);
            }
            delay.current = setTimeout(validateInput, 500);
        }
        return () => clearTimeout(delay.current)
    }, [text]);

    return (
        <>
            <div className={'InputContainer'}>
                <Tooltip
                    placement="top"
                    title={error}
                    getPopupContainer={() => getContainerElement()}
                    visible={!valid}>
                    <input
                        className={'Text'}
                        type="text"
                        value={text}
                        onChange={inputHandler}
                        onKeyPress={e => {
                            if (e.key === 'Enter') {
                                submitAnswer();
                            }
                        }}
                        placeholder={'Type your message here...'}
                        ref={input => input && input.focus()}/>
                </Tooltip>
            </div>
            <div className={'Actions'}>
                <i>
                    <Icon
                        type="paper-clip"
                        theme="outlined"
                        style={{ fontSize: '22px' }}/>
                </i>
            </div>
            <div className={'Submit'}>
                <i className={'SendIconActive'} onClick={submitAnswer}>
                    <FontAwesomeIcon
                        size="2x"
                        icon={faTelegramPlane}
                        color={valid ? '' : 'red'}/>
                </i>
            </div>
        </>
    );
};

export default Text;
