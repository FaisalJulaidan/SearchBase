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
import Settings from './Settings';
import Input from './Input';
import Signature from './Signature';
import 'antd/dist/antd.css';

export const Chatbot = ({
                            isDirectLink, btnColor, assistantID,
                            addBotMessage, setChatbotStatus, chatbot, initChatbot,
                            resetChatbot, resetMessage, setChatbotAnimation, messageList,
                            loadByDefault, root
                        }) => {
    const { assistant, status, animation } = chatbot;
    const { loading, thinking, open, disabled, active, started, curAction, finished } = status;
    const { open: animationOpen } = animation;


    let timer = useRef(null);
    let messageTimer = useRef(null);
    let chatbotRef = useRef(null);
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
        dataHandler.setSessionID(undefined);
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

    useEffect(() => {
        const hasBeenUsed = () => {
            let used = localStorage.getItem('TSB_CHATBOT_USED');
            if (used === null) {
                localStorage.setItem('TSB_CHATBOT_USED', true);
                return false;
            } else {
                return true;
            }
        };

        if (isDirectLink) {
            setChatbotAnimation({ open: true });
            setChatbotStatus({ open: true });
        }

        if (assistant && !hasBeenUsed()) {
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
            if (!block.Content) return;
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
            if (!block.Content) return;
            stopTimer.current = optionalDelayExecution(() => {
                addBotMessage(block.Content.text, block.Type, block);
                setChatbotStatus({ thinking: false, waitingForUser: true });
                if (block.selfContinue) {
                    setChatbotStatus({
                        thinking: false,
                        curBlockID: block.selfContinue,
                        curAction: block.selfContinue === 'End Chat' ? 'End Chat' : 'Go To Next Block'
                    });
                    return;
                }
                if (block[flowAttributes.TYPE] === messageTypes.RAW_TEXT) {
                    setChatbotStatus({
                        thinking: false,
                        curBlockID: block[flowAttributes.CONTENT][flowAttributes.BLOCKTOGOID],
                        curAction: block[flowAttributes.CONTENT][flowAttributes.SUPER_ACTION]
                    });
                    return;
                }
                // messageTimer.current = { timer: setInterval(() => console.log('lol'), 100), count: messageList.length }
            }, block.extra.needsToFetch !== false, block.delay);
        };

        const fetch = async (block) => {
            let [key, data, cancelled] = await fetchData(block);
            let fetchedData = {};

            fetchedData[key] = data;

            if (cancelled) return {};
            if (!data.length) {
                setChatbotStatus({
                    curAction: block[flowAttributes.SKIP_ACTION] || 'Go To Next Block',
                    afterMessage: 'Sorry, I could not find what you want!',
                    curBlockID: block[flowAttributes.CONTENT][flowAttributes.BLOCKTOGOID]
                });
                return ['Failed to fetch data', null];
            }
            return [null, fetchedData];
        };


        const setNextBlock = async (chatbot, started, curAction, assistant) => {
            if (!isReady(chatbot) || !assistant) return;
            if (!started) {
                setChatbotStatus({ started: true });
                return;
            }


            let nextBlock = getCurBlock(curAction, assistant, chatbot);

            if (!nextBlock) return;

            if (messageTimer.current) {
                clearInterval(messageTimer.current.timer);
                messageTimer.current = null;
            }
            setChatbotWaiting(nextBlock);
            let fetchedData, err;
            if (nextBlock.extra.needsToFetch) {
                [err, fetchedData] = await fetch(nextBlock);
            }
            if (err) {
                return;
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
        if (!assistant && (loadByDefault === 'true' || !loadByDefault)) {
            fetchChatbot();
        }
        if (!window.__TSB_CHATBOT) {
            window.__TSB_CHATBOT = {};
            window.__TSB_CHATBOT.ready = true;
            window.__TSB_CHATBOT.load = () => fetchChatbot();
            window.__TSB_CHATBOT.open = () => openWindow();
            window.__TSB_CHATBOT.close = () => closeWindow();
        }
    }, [initChatbot, setChatbotStatus]);

    let position = undefined;

    if (assistant)
        position = assistant.Config.chatbotPosition || 'Right';

    return (
        <>
            {!disabled ?
                <>
                    {open && !loading ?
                        <div ref={chatbotRef}
                             style={{ position: isDirectLink ? 'relative' : '' }}
                             className={[
                                 animation.open ? `ZoomIn_${position}` : `ZoomOut_${position}`,
                                 isDirectLink ? 'Chatbot_DirectLink' : 'Chatbot',
                                 position
                             ].join(' ')}>
                            <Header isDirectLink={isDirectLink}
                                    title={assistant.TopBarText}
                                    logoPath={assistant.LogoPath}
                                    resetChatbot={reset}
                                    closeWindow={closeWindow}/>
                            <Flow inputOpen={animation.inputOpen}
                                  hideSignature={assistant.HideSignature}
                                  thinking={thinking}
                                  resetAsync={resetAsync}/>
                            <Input isDirectLink={isDirectLink}
                                   hideSignature={assistant.HideSignature}
                                   visible={animation.inputOpen}/>
                            {assistant.HideSignature ? null : <Signature isDirectLink={isDirectLink}/>}
                            <Settings/>
                        </div>
                        :
                            <ChatButton btnColor={btnColor}
                                        active={active}
                                        loading={loading}
                                        position={position}
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
