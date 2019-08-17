import React from 'react';
import {Col, Container, Image, Row} from "react-bootstrap";
import styles from './conversations.module.css';
import odometerStyle from './odometer.css';
import Odometer from 'react-odometerjs';
import 'odometer/themes/odometer-theme-default.css';

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
        }, 3000);
    }

    componentWillUnmount() {
        clearInterval(this.timerIntervalID);
    }

    render() {
        return (
            <div className={styles.bg_gradient}>
                <Container>
                    <Row className={styles.center}>
                        <Col className={styles.col_text} xs={{span: 7}}>
                            <div className={styles.div_text}>
                                <h1 className={styles.text}>ChatBot on going conversations</h1>
                            </div>
                            <div className={styles.div_number}>
                                <Odometer duration={1000} value={this.state.conversationsNum} format="dd"/>
                            </div>
                        </Col>
                        <Col xs={{span:5}}>
                            <Image className={styles.image} fluid src="assets/img/home/message.svg"/>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }


}

export default Conversations;
