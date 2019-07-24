import React, { useEffect, useRef, useState } from 'react';
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
// Utils
import {
    dataHandler,
    getServerDomain,
    isReady,
    optionalDelayExecution,
    promiseWrapper,
    useInterval
} from '../../utils';
import { fetchData, getCurBlock } from '../../utils/flowHandler';
// Constants
import * as flowAttributes from '../../constants/FlowAttributes';
import * as messageTypes from '../../constants/MessageType';
// Components
import ChatButton from './ChatButton';
import Header from './Header';
import Flow from './Flow';
import Input from './Input';
import Signature from './Signature';
import 'antd/dist/antd.css';

export const Chatbot = ({
                     isDirectLink, btnColor, assistantID,
                     addBotMessage, setChatbotStatus, chatbot, initChatbot,
                     resetChatbot, resetMessage, setChatbotAnimation, messageList
                 }) => {
    const { assistant, status, animation } = chatbot;
    const { loading, thinking, open, disabled, active, started, curAction, finished } = status;
    const { open: animationOpen } = animation;
    let timer = useRef(null);
    let stopTimer = useRef(null);

    window.addEventListener('beforeunload', () => {
        if (!finished) {
            // localStorage.setItem('tsb_chatbot_draft', JSON.stringify({ver: '123', messages: messageList}))
            setChatbotStatus({ curAction: 'Early End Chat' });
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
        dataHandler.cancelRequest();
        stopTimer.current.reset();
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
                if (SecondsUntilPopup === 0) return;
                setTimeout(() => {
                    setChatbotAnimation({ open: true });
                }, SecondsUntilPopup * 1000);
            }
    }, [setChatbotAnimation, assistant]);

    // When the chatbot animation has been set to true
    useEffect(() => {
        let startupTimeout;
        if (animationOpen) {
            startupTimeout = setTimeout(() => {
                setChatbotStatus({ open: true });
            }, 500);
        }
        return () => clearInterval(startupTimeout);
    }, [setChatbotAnimation, setChatbotStatus, animationOpen]);


    // set timer for timeSpent
    useInterval(() => {
        dataHandler.incrementTimeElapsed(200);
    }, open === true ? 200 : null);

    // Every time the chatbot changes, call to flowHandler
    useEffect(() => {
        // if(disabled) return;
        const setChatbotWaiting = (block) => {
            if(!block.Content   ) return
            setChatbotStatus({
                curAction: null,
                waitingForUser: false,
                curBlockID: block.ID,
                curBlock: block,
                afterMessage: null,
                thinking: true
            });
        };

        const botRespond = (block, chatbot) => {
            if(!block.Content) return
            stopTimer.current = optionalDelayExecution(() => {
                setChatbotStatus({ thinking: false, waitingForUser: true });
                addBotMessage(block.Content.text, block.Type, block);
                if (block.selfContinue) {
                    setChatbotStatus({
                        curBlockID: block.selfContinue,
                        curAction: block.selfContinue === 'End Chat' ? 'End Chat' : 'Go To Next Block'
                    });
                }
                if (block[flowAttributes.TYPE] === messageTypes.RAW_TEXT) {
                    setChatbotStatus({
                        curBlockID: block[flowAttributes.CONTENT][flowAttributes.BLOCKTOGOID],
                        curAction: block[flowAttributes.CONTENT][flowAttributes.SUPER_ACTION]
                    })
                }
            }, !block.extra.needsToFetch, block.delay);
        };

        const fetch = async (block) => {
            let [key, data, cancelled] = await fetchData(block);
            let fetchedData = {};

            fetchedData[key] = data;

            if (cancelled) return {};
            console.log(block)
            if (!data.length) {
                setChatbotStatus({
                    curAction: 'End Chat',
                    afterMessage: 'Sorry, I could not find what you want!',
                    curBlockID: block[flowAttributes.CONTENT][flowAttributes.BLOCKTOGOID]
                });
                return {};
            }
            return fetchedData;
        };


        const setNextBlock = async (chatbot, started, curAction, assistant) => {
            if (!isReady(chatbot) || !assistant) return;
            if (!started) {
                setChatbotStatus({ started: true });
                return;
            }
            let nextBlock = getCurBlock(curAction, assistant, chatbot);
            if (!nextBlock) return;

            setChatbotWaiting(nextBlock);
            let fetchedData = {};
            if (nextBlock.extra.needsToFetch) {
                fetchedData = await fetch(nextBlock);
            }
            if (nextBlock.extra.end) {
                setChatbotStatus({ finished: true });
                let { cancelled } = await dataHandler.sendData(nextBlock.extra.finished);
                if (cancelled) return;
            }
            botRespond({ ...nextBlock, fetchedData }, chatbot);
            // }, 600)
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
            if (isDisabled)
                return setChatbotStatus({ disabled: isDisabled, active: assistant.Active, loading: false });

            dataHandler.setAssistantID(assistantID);
            initChatbot(
                assistant,
                [].concat(assistant.Flow.groups.map(group => group.blocks)).flat(1),
                { disabled: isDisabled, active: assistant.Active });
        };
        if (!assistant) {
            fetchChatbot();
        }
    }, [initChatbot, setChatbotStatus]);

    return (
        <>
            {active ?
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
                                    active={active}
                                    loading={loading}
                                    openWindow={openWindow}/>
                    }
                </>
                : null}
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
