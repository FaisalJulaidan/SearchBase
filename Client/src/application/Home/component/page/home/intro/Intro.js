import React from 'react';
import {Button, Col, Container, Row} from "react-bootstrap";
import styles from "./intro.module.css";
import {Bounce,Zoom} from "react-reveal";
import {Link} from "react-router-dom";
import TextTransition from "react-text-transition";
import {getLink} from "helpers";
import MobileFrame from "../message-intro/mobile-frame/MobileFrame";
import JobOfferItem from "../message-intro/job-offer-item/JobOfferItem";
import messagesJSON from "../message-intro/messages";
import MessageItem from "../message-intro/message-item/MessageItem";

class Intro extends React.Component {

    constructor(props) {
        super(props);
        this.onReveal = this.onReveal.bind(this);
    }

    state = {
        activeTitleIndex: 0,
        animWhen: { //mobile demo messages animation helper
            m1Reveal: false, //Second Message Status
            m2Reveal: false,
            offerReveal: false //Job Offer Anim Status
        }
    };

    titles = ['Automate', 'Analyse', 'Empower'];
    timerIntervalID = 0;

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

    componentDidMount() {
        this.timerIntervalID = setInterval(() => {
            let activeTitleIndex = this.state.activeTitleIndex + 1;
            if (activeTitleIndex >= this.titles.length)
                activeTitleIndex = 0;
            this.setState({activeTitleIndex: activeTitleIndex});
        }, 3000);
    }

    componentWillUnmount() {
        clearInterval(this.timerIntervalID);
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
                <Zoom key={i} wait={1200} when={animWhen} onReveal={this.onReveal}>
                    <MessageItem mine={message.mine} text={message.text}/>
                </Zoom>
            )

        });

        return (
            <Container id={this.props.id}>
                <Row>
                    <Col className={styles.text_col}
                         xs={{span: 12}} sm={{span: 10, offset: 1}} md={{span: 6, offset: 0}} lg={{span: 6}}>
                        <Bounce left big>
                            <TextTransition className={styles.title_transient}
                                            text={this.titles[this.state.activeTitleIndex]}/>
                            <h2 className={styles.title}>
                                your recruitment process and Grow
                            </h2>
                            <h3 className={styles.subtitle}>Delivering Powerful Automation to Recruiters</h3>
                            <Button variant="outline-light" className={styles.button}>
                                <Link to="/get-started" style={{textDecoration: 'none'}}>Book a demo</Link>
                            </Button>
                        </Bounce>
                    </Col>
                    <Col xs={{span: 8, offset: 2}} md={{span: 6, offset: 0}} lg={{span: 4, offset: 1}}>
                        <MobileFrame>
                            {messages}
                            <Zoom when={this.state.animWhen.offerReveal}>
                                <JobOfferItem/>
                            </Zoom>
                        </MobileFrame>
                    </Col>
                </Row>
            </Container>
        );
    }

}

export default Intro;
