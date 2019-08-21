import React from 'react';
import {Col, Container, Row} from "react-bootstrap";
import styles from "./message-intro.module.css";
import MobileFrame from "./mobile-frame/MobileFrame";
import {Bounce, Fade} from "react-reveal";
import {faArrowCircleRight} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import messagesJSON from './messages.json'
import {Link} from "react-router-dom";
import MessageItem from "./message-item/MessageItem";
import JobOfferItem from "./job-offer-item/JobOfferItem";


class MessageIntro extends React.Component {

    constructor(props) {
        super(props);
        this.onReveal = this.onReveal.bind(this);
    }

    state = {
        text: {
            intro: 'Seamless Experience',
            title: 'Capture candidates, in seconds',
            text: 'By interacting with candidates using Chatbots,\n' +
                'you are working at times of Convenience for the Candidates, in a Confidential\n' +
                'Environment. With direct interaction between you and candidates, your business can\n' +
                'make Connections and build Highly Descriptive Candidate Profiles in Seconds.',
        },
        animWhen: { //mobile demo messages animation helper
            m1Reveal: false, //Second Message Status
            m2Reveal: false,
            offerReveal: false //Job Offer Anim Status
        }
    };

    //Animation Reveal Spy
    onReveal() {
        if (this.state.animWhen.m1Reveal) {
            this.setState({animWhen: {m2Reveal: true}})
        } else if (this.state.animWhen.m2Reveal) {
            this.setState({animWhen: {offerReveal: true}})
        } else {
            this.setState({animWhen: {m1Reveal: true}})
        }
    }

    render() {

        let messages = messagesJSON.map((message, i) => {

            let animWhen;
            switch (i) {
                case 1:
                    animWhen = this.state.animWhen.m1Reveal;
                    break;
                case 2:
                    animWhen = this.state.animWhen.m2Reveal;
                    break;
            }

            return (
                <Bounce delay={((i+1) * 1000)} when={animWhen} onReveal={this.onReveal}>
                    <MessageItem key={i} mine={message.mine} text={message.text}/>
                </Bounce>
            )

        });

        let fadeAnim = {};
        if (window.innerWidth > 767.98) fadeAnim["left"] = true; else fadeAnim["bottom"] = true;
        return (
            <Container id={this.props.id}>
                <Row className={styles.center}>
                    <Col xs={{span: 8, offset: 2, order: 1}} md={{span: 6, offset: 0, order: 1}}
                         lg={{span: 4, offset: 1, order: 1}}>
                        <MobileFrame>
                            {messages}
                            <Bounce delay={4000} when={this.state.animWhen.offerReveal}>
                                <JobOfferItem/>
                            </Bounce>
                        </MobileFrame>
                    </Col>
                    <Col xs={{span: 12, order: 2}} sm={{span: 10, order: 2, offset: 1}} md={{span: 6, offset: 0}}
                         lg={{span: 6, offset: 1}}>
                        <div className={styles.text_section}>
                            <Fade {...fadeAnim} big>
                                <h1 className={styles.intro}>{this.state.text.intro}</h1>
                                <h3 className={styles.title}>{this.state.text.title}</h3>
                                <h6 className={styles.text}>{this.state.text.text}</h6>
                                <Link to="/how-it-works" className={styles.button}>
                                    Read How it works <FontAwesomeIcon className={styles.icon}
                                                                       icon={faArrowCircleRight}/>
                                </Link>
                            </Fade>
                        </div>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default MessageIntro;
