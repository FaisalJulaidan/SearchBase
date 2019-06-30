import React from "react";
import styles from "./Bot.module.css";

import {constants} from "../../../../utilities/constants";
import * as actionTypes from '../../../../store/actions';
import { connect } from 'react-redux';
import Question from "./Question/Question";
import Solutions from "./Solutions/Solutions";
import Thinking from "./Thinking/Thinking";
import {Button as AntdButton, Row} from "antd";


class Bot extends React.Component {


    isIE11 = false;
    isEdge = false;
    componentWillMount() {
        // check if lastMsg and ensure that thinking animation won't happen 
        // with old messages when toggling the chatbot window.
        let delay = 0;
        if (this.props.isLastMsg) {
            delay = this.props.delay;
        }

        // Show thinking gif animation for the last message only
        this.props.onIsTypingUpdate(true);
        setTimeout(() => {
            this.props.onIsTypingUpdate(false)
                .then(() => {this.props.finishedTyping(0)});
        }, delay);

        this.isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
        this.isEdge = /Edge/.test(navigator.userAgent);

    }

    // check for links and create <a>-s out of them
    // NOTE: pure text is label as <></> does not allow key property
    hyperLinkifyText = (text) => {
        // split the whole message into the parts by using the start of the link
        let linksArray = text.split("*&&TEXT:");

        // put in the first part of the message which would be the only one without a link in it
        let result = [<label key="0">{linksArray[0]}</label>];

        // go through all the links
        for(let i=1;i < linksArray.length;i++){
            // create anchor tag out of the link in the text
            let linkSplit = linksArray[i].split("*&&LINK:");
            result.push(
                <a key={i+"link"} href={linkSplit[1].split("*&&END*")[0]}
                    target={"_blank"}>{linkSplit[0]}</a>);
            // push the message after the link
            result.push(<label key={i+"afterText"}>{linksArray[i].split("*&&END*")[1]}</label>);
        }

        // spread the pushed text and links into 1 component
        return <>{[...result]}</>;
    };

    render() {
        let msgContent; // this will only be used for Question and Solutions block types
        switch (this.props.type) {
            case constants.QUESTION:
                msgContent = <Question className={styles.fadeIn} {...this.props} />;
                break;
            case constants.SOLUTIONS:
                msgContent = <Solutions className={styles.fadeIn} {...this.props} />;
                break;
        }

        let msgText = this.hyperLinkifyText(this.props.text);
        const {content, isLastMsg, isBotTyping } = this.props; // represents the message object

        // Show this skippable button only for Input and not for Question and Solutions types
        const skippable = content && content.hasOwnProperty('skippable') ? content.skippable : false;
        // if msgContent is null that mean it is neither a Question nor Solution. So, it is UserInput
        if (skippable && !(msgContent)){
            msgText = (
                <>
                    <p className={styles.fadeIn}>{this.props.text}</p>
                    <AntdButton block type="danger" key={99} disabled={!isLastMsg} style={{marginTop: "10px"}}
                                onClick={() => this.props.skipped(content.skipText)}>
                        {content.skipText}
                    </AntdButton>
                </>
            )
        }

        // after certain amount of time we remove thinking and show the msgContent and message.text
        return (
            <Row>
                <div className={[this.isIE11 || this.isEdge ? styles.Bot_IE11 : styles.Bot, styles.bounceIn].join(" ")}>
                    {isBotTyping && isLastMsg ? <Thinking/> : msgText }
                    {isBotTyping && isLastMsg  ? null : msgContent}
                </div>
            </Row>
        );
    }
}

const mapStateToProps = state => {
    return {
        isBotTyping: state.isBotTyping
    }
};

const mapDispatchToProps = dispatch => {
    return {
        onIsTypingUpdate: (value) => {
            dispatch({type:actionTypes.UPDATE_IS_BOT_TYPING, payload:{value}});
            return Promise.resolve();
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Bot);
