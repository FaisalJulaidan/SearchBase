import React, { useEffect, useRef, useState } from 'react';
import { connect } from 'react-redux';
// Actions
import { addBotMessage, addUserMessage, rewindToMessage, setChatbotStatus } from '../../store/actions';
// Utils
import { dataHandler } from '../../utils';
// Styles
import './styles/Flow.css';
import './styles/Animations.css';
// Components
import BotMessage from './BotMessage/BotMessage';
import UserMessage from './UserMessage/UserMessage';
import Thinking from './BotMessage/Thinking';

const Flow = ({ messages, setChatbotStatus, addUserMessage, addBotMessage, thinking, inputOpen, rewindToMessage, resetAsync }) => {
    const flowRef = useRef(null);
    const scrollRef = useRef(null);
    let [msgList, setMsgList] = useState([]);
    let [active, setActive] = useState(null);
    const addStatus = (component, message) => {
        return React.cloneElement(component, {
            setChatbotStatus,
            addUserMessage,
            addBotMessage,
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
        let timeOut = setTimeout(() => {
            flowRef.current.scrollTo({ top: scrollRef.current.offsetTop, behavior: 'smooth' });
        }, 200);
        return () => clearTimeout(timeOut);
    }, [messages, thinking, inputOpen]);

    useEffect(() => {
        dataHandler.updateMessages(messages);
        setActive(null);
        setMsgList(messages);
    }, [messages]);


    const getBySender = (message) => {
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
        const active = msgList.filter(msg => msg.index <= idx).reverse().filter(msg => msg.sender === 'BOT')[0];
        setActive(active.index);
        rewindToMessage(active.index);
        resetAsync();
        setChatbotStatus({ thinking: false, finished: false });
    };

    let groupedMessages = groupMessages(msgList);
    return (
        <div className={['Flow', (inputOpen ? '' : 'Extended')].join(' ')} ref={flowRef}>
            {
                groupedMessages.map((group, i) =>
                    <div className={[group[0].sender, 'BounceIn'].join(' ')} key={i}>
                        {group.map(message => addStatus(getBySender(message), message))}
                    </div>
                )
            }
            {thinking ? <Thinking/> : null}
            <div className={'FlowBottom'} ref={scrollRef}/>
        </div>
    );
};

const mapStateToProps = state => ({
    messages: state.messages.messageList
});

export default connect(
    mapStateToProps,
    { setChatbotStatus, addUserMessage, addBotMessage, rewindToMessage }
)(Flow);