import React from "react";
import styles from "./Flow.module.css";
import {constants} from "../../../utilities/constants";
import "./Flow.css";

import Bot from "./Bot/Bot";
import User from "./User/User";

class Flow extends React.Component {

    scrollToBottom = (delay = constants.DELAY_DEFAULT) => {
        setTimeout(() => {
            if (this.el) {
                this.el.scrollIntoView({behavior: "smooth"});
            }
        }, delay)
    };

    // componentDidMount() {
        // this.scrollToBottom(0);
    // }

    // componentDidUpdate() {
        // this.scrollToBottom(0);
    // }

    render() {
        return (
            <div className={styles.Flow}>
                {this.props.messages.map((message, i) => {
                    // Set additional props related to every individual messages
                    message.answerClicked = this.props.answerClicked;
                    message.selectSolution = this.props.selectSolution;
                    message.submitSolutions = this.props.submitSolutions;
                    message.skipped = this.props.skipped;
                    message.isLastMsg = (this.props.messages.length - 1) === i;

                    if (message.from === constants.BOT)
                        return <Bot {...message} key={i} finishedTyping={this.scrollToBottom}/>;
                    else
                        return <User {...message} key={i}/>;
                })}
                {/* Dummy div to scroll flow to the bottom automatically */}
                <div ref={el => {
                    this.el = el;
                }}/>
            </div>
        );
    }
}


export default Flow;
