import React, { useEffect, useRef } from 'react';
import { connect } from 'react-redux';
import axios from 'axios';
// Actions
import {
    addBotMessage,
    initChatbot,
    resetChatbot,
    resetMessage,
    setChatbotAnimation,
    setChatbotStatus
} from '../../store/actions';
// Styles
import './styles/Chatbot.css';
import 'antd/dist/antd.css';
// Utils
import {
    dataHandler,
    isReady,
    optionalDelayExecution,
    promiseWrapper,
    useInterval,
    getServerDomain
} from '../../utils';
import { fetchData, getCurBlock } from '../../utils/flowHandler';
// Constants
import * as flowAttributes from '../../constants/FlowAttributes';
// Components
import ChatButton from './ChatButton';
import Header from './Header';
import Flow from './Flow';
import Input from './Input';
import Signature from './Signature';

const Chatbot = ({
                     isDirectLink, btnColor, assistantID,
                     addBotMessage, setChatbotStatus, chatbot, initChatbot,
                     resetChatbot, resetMessage, setChatbotAnimation, messageList
                 }) => {
    const { assistant, status, animation } = chatbot;
    const { loading, thinking, open, disabled, started, curAction, finished } = status;
    const { open: animationOpen } = animation;
    let timer = useRef(null);
    let stopTimer = useRef(null);

    window.addEventListener('beforeunload', () => {
        if (!finished) {
            // localStorage.setItem('tsb_chatbot_draft', JSON.stringify({ver: '123', messages: messageList}))
            setChatbotStatus({ curAction: 'End Chat' });
        }
    });

    // reset chatbot
    const reset = () => {
        resetChatbot();
        resetMessage();
        dataHandler.resetTimeElapsed();
        clearTimeout(timer.current);
        resetAsync();
    };

    const resetAsync = () => {
        console.log(stopTimer.current)
        dataHandler.cancelRequest();
        console.log(stopTimer.current)
        stopTimer.current.reset()
    };

    const closeWindow = () => {
        setChatbotAnimation({ open: false });
        setTimeout(() => setChatbotStatus({ open: false }), 500);
        // reset?
    };

    const openWindow = () => {
        setChatbotAnimation({ open: true });
    };

    // useEffect(() => {
    //   let chat = localStorage.getItem('tsb_chatbot_draft')
    //   if(chat){
    //     alert('Hello again, you left last time without finishing the chatbot, would you like to continue where you left off?')
    //   }
    // }, [])

    // On boot first time animation
    useEffect(() => {
        if (assistant)
            if (isDirectLink) {
                setChatbotAnimation({ open: true });
                setChatbotStatus({ open: true });
            } else {
                const { SecondsUntilPopup } = assistant;
                setTimeout(() => {
                    setChatbotAnimation({ open: true });
                }, SecondsUntilPopup * 1000);
            }
    }, [setChatbotAnimation, assistant]);

    // When the chatbot animation has been set to true
    useEffect(() => {
        let startupTimeout;
        if (assistant && started && animationOpen) {
            startupTimeout = setTimeout(() => {
                setChatbotStatus({ open: true });
            }, 500);
        }
        return () => clearInterval(startupTimeout);
    }, [started, setChatbotAnimation, setChatbotStatus, assistant, animationOpen]);

    // On start, set open true
    useEffect(() => {
        if (started)
            setChatbotAnimation({ open: true });
    }, [started, setChatbotAnimation]);

    // set timer for timeSpent
    useInterval(() => {
        dataHandler.incrementTimeElapsed(200);
    }, open === true ? 200 : null);

    // Every time the chatbot changes, call to flowHandler
    useEffect(() => {
        const setChatbotWaiting = (block, overrideAction = null) => {
            setChatbotStatus({
                curAction: overrideAction,
                waitingForUser: false,
                curBlockID: block.ID,
                curBlock: block,
                thinking: true
            });
        };

        const endChat = async (completed) => {
            return await dataHandler.sendData(completed);
        };

        const botRespond = (block) => {
            stopTimer.current = optionalDelayExecution(() => {
                setChatbotStatus({ thinking: false, waitingForUser: true });
                addBotMessage(block.Content.text, block.Type, block);
                if (block.selfContinue) {
                    setChatbotStatus({
                        curBlockID: block.selfContinue,
                        curAction: 'Go To Next Block'
                    });
                }
            }, !block.extra.needsToFetch, block.delay);
        };

        const setNextBlock = async (chatbot, started, curAction, assistant) => {
            if (isReady(chatbot)) {
                if (!started) {
                    setChatbotStatus({ started: true });
                } else {
                    let nextBlock = getCurBlock(curAction, assistant, chatbot);
                    if (nextBlock) {
                        setChatbotWaiting(nextBlock);
                        let fetchedData = {};
                        if (nextBlock.extra.needsToFetch) {
                            let [key, data, cancelled] = await fetchData(nextBlock);
                            fetchedData[key] = data;
                            if (cancelled) return;
                            if (!data.length) {
                                setChatbotStatus({
                                    curAction: 'Not Found',
                                    curBlockID: nextBlock[flowAttributes.CONTENT][flowAttributes.BLOCKTOGOID]
                                });
                                return;
                            }
                        }
                        if (nextBlock.extra.end) {
                            setChatbotStatus({ finished: true });
                            let { cancelled } = await endChat(true);
                            if (cancelled) return;
                        }
                        botRespond({ ...nextBlock, fetchedData });
                    }
                }
            }
        };
        setNextBlock(chatbot, started, curAction, assistant);
    }, [chatbot, setChatbotStatus, addBotMessage, assistant, curAction, started]);

    // initialize chatbot
    useEffect(() => {
        const fetchChatbot = async () => {
            const { data, error } = await promiseWrapper(axios.get(`${getServerDomain()}/api/assistant/${assistantID}/chatbot`));
            if (error) {
                // ERROR SENTRY
                console.log(error);
                return;
            }

            const { assistant, isDisabled } = data.data.data;
            dataHandler.setAssistantID(assistantID);
            initChatbot(
                assistant,
                [].concat(assistant.Flow.groups.map(group => group.blocks)).flat(1),
                { disabled: isDisabled }
            );
        };
        fetchChatbot();
    }, [initChatbot]);

    return (
        <>
            {open && !loading ?
                <div style={{ position: isDirectLink ? 'relative' : '' }}
                     className={[
                         animation.open ? 'ZoomIn' : 'ZoomOut',
                         isDirectLink ? 'Chatbot_DirectLink' : 'Chatbot'
                     ].join(' ')}>
                    <Header isDirectLink={isDirectLink}
                            title={assistant.TopBarText}
                            logoPath={assistant.LogoPath}
                            resetChatbot={reset}
                            closeWindow={closeWindow}/>
                    <Flow inputOpen={animation.inputOpen} thinking={thinking}
                          resetAsync={resetAsync}/>
                    <Input isDirectLink={isDirectLink}
                           visible={animation.inputOpen}/>
                    <Signature isDirectLink={isDirectLink}/>
                </div>
                :
                <ChatButton btnColor={btnColor}
                            disabled={disabled}
                            loading={loading}
                            openWindow={openWindow}/>
            }
        </>
    );
};

const mapStateToProps = (state) => ({
    chatbot: state.chatbot,
    messageList: state.messages.messageList
});


export default connect(mapStateToProps, {
    setChatbotStatus,
    addBotMessage,
    initChatbot,
    resetChatbot,
    resetMessage,
    setChatbotAnimation
})(Chatbot);
