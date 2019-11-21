import React, {useEffect, useRef, useState} from 'react';
import {connect} from 'react-redux';
// Actions
import {addBotMessage, addUserMessage, rewindToMessage, setChatbotStatus} from '../../store/actions';
// Utils
import {dataHandler} from '../../utils';
// Styles
import './styles/Flow.css';
import './styles/Animations.css';
// Components
import BotMessage from './BotMessage/BotMessage';
import UserMessage from './UserMessage/UserMessage';
import Thinking from './BotMessage/Thinking';

const Flow = ({messages, setChatbotStatus, addUserMessage, addBotMessage, hideSignature, thinking, inputOpen, rewindToMessage, resetAsync, status}) => {
    const flowRef = useRef(null);
    const scrollRef = useRef(null);
    let [lastBotMessage, setLastBotMessage] = useState(null)
    let [active, setActive] = useState(null);
    let curHeight = useRef(0)

    const addStatus = (component, message) => {
        return React.cloneElement(component, {
            setChatbotStatus,
            addUserMessage,
            addBotMessage,
            thinking: status.thinking,
            message
        });
    };

    const groupMessages = (messages) => {
        let group = [];
        let messageList = [];
        let curSender = 'BOT';
        messages.forEach((message, i) => {
            if (message.sender !== curSender) {
                messageList.push(group);
                curSender = message.sender;
                group = [message];
            } else {
                group.push(message);
            }
            if (i === messages.length - 1) {
                messageList.push(group);
            }
        });
        return messageList;
    };

    useEffect(() => {
        curHeight.current = window.innerHeight
    }, [])


    window.addEventListener('resize', () => {
        if(window.innerHeight != curHeight.current){
            console.log('scroll')
            curHeight.current = window.innerHeight
            flowRef.current.scrollTo({ top: scrollRef.current.offsetTop, behavior: 'smooth' });
        }

    })

    useEffect(() => {
        let timeOut = setTimeout(() => {
            flowRef.current.scrollTo({ top: scrollRef.current.offsetTop, behavior: 'smooth' });
        }, 200);
        return () => clearTimeout(timeOut);
    }, [messages, thinking, inputOpen]);

    useEffect(() => {
        dataHandler.updateMessages(messages);
        const lastBotMessage = messages.slice().reverse().filter(msg => msg.sender === 'BOT')[0];
        setLastBotMessage(lastBotMessage ? lastBotMessage.index : null)
    }, [messages]);

    useEffect(() => {
        setActive(lastBotMessage ? lastBotMessage : null)
    }, [status, lastBotMessage])

    const getBySender = (message) =>  {
        if (message.sender === 'BOT') {
            return <BotMessage
                key={message.index}
                type={message.type}
                active={message.index === active}/>;
        } else {
            return <UserMessage key={message.index} type={message.type} rewind={rewind}/>;
        }
    };

    const rewind = (idx) => {
        const lastBotMessage = messages.slice().filter(msg => msg.index <= idx).reverse().filter(msg => msg.sender === 'BOT')[0];
        setLastBotMessage(lastBotMessage.index)
        rewindToMessage(lastBotMessage.index);
        resetAsync();
        setChatbotStatus({ thinking: false, finished: false });
    };

    let groupedMessages = groupMessages(messages);

    const isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
    const getSender = (sender) => {
        switch (sender) {
            case 'BOT':
                return isIE11 ? 'BOT_IE11' : 'BOT';
            case 'USER':
                return isIE11 ? 'USER_IE11' : 'USER'
        }
    };
    const getFlowClass = () => {
        if (!inputOpen && hideSignature) {
            return 'Extended_Without_Signature'
        }

        if (inputOpen && hideSignature) {
            return 'Extended'
        }

        if (!inputOpen && !hideSignature) {
            return 'Extended'
        }
    };
    return (
        <div className={[isIE11 ? 'Flow_IE11' : 'Flow', getFlowClass()].join(' ')}
             ref={flowRef}>
            {
                groupedMessages.map((group, i) =>
                    <div className={[getSender(group[0].sender), 'BounceIn'].join(' ')} key={i}>
                        {group.map(message => addStatus(getBySender(message), message))}
                    </div>
                )
            }
            {thinking ? <Thinking/> : null}
            <div className={isIE11 ? 'FlowBottom_IE11' : 'FlowBottom'} ref={scrollRef}/>
        </div>
    );
};

const mapStateToProps = state => ({
    status: state.chatbot.status,
    messages: state.messages.messageList
});

export default connect(
    mapStateToProps,
    { setChatbotStatus, addUserMessage, addBotMessage, rewindToMessage }
)(Flow);
