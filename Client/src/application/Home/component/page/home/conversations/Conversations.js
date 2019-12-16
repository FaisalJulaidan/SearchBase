import React from 'react';
import {Col, Container, Image, Row} from "react-bootstrap";
import styles from './conversations.module.css';
import odometerStyle from './odometer.css';
import Odometer from 'react-odometerjs';
import 'odometer/themes/odometer-theme-default.css';
import {getLink} from "helpers";

class Conversations extends React.Component {

    state = {
        conversationsNum: 0
    };

    timerIntervalID = 0;

    componentDidMount() {
        const rand = 20000 + Math.random() * (25000 - 20000);
        this.setState({conversationsNum: rand});
        this.timerIntervalID = setInterval(() => {
            const rand = 1 + Math.random() * (10 - 1);
            let conversationsNum = this.state.conversationsNum + rand;
            this.setState({conversationsNum: conversationsNum});
        }, 4000);
    }

    componentWillUnmount() {
        clearInterval(this.timerIntervalID);
    }

    render() {
        return (
            <div className={styles.bg_gradient}>
                <Container>
                    <Row>
                        <Col className={styles.col_text}>
                            <h1>ChatBot on going conversations</h1>
                        </Col>
                    </Row>
                    <Row className={styles.center}>
                        <Col className={styles.col_num} xs={12} md={8} xl={7}>
                            <div className={styles.div_number}>
                                <Odometer duration={1000} value={this.state.conversationsNum} format="dd"/>
                            </div>
                        </Col>
                        <Col xs={{span: 8, offset: 2}} md={{span: 4, offset: 0}} xl={5}>
                            <div className={styles.image_wrapper}>
                                <Image className={styles.image} fluid
                                       src={"/images/home/home/message.svg"}/>
                            </div>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }


}

export default Conversations;
