import React, {Component} from 'react';
import styles from './success-payment.module.css'
import {Card, Container, Row, Col} from "react-bootstrap";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faQuoteRight,faQuoteLeft} from "@fortawesome/free-solid-svg-icons";
import {faCheckCircle} from "@fortawesome/free-regular-svg-icons";

class SuccessPayment extends Component {
    render() {
        return (
            <div className={styles.wrapper}>
                <div className={styles.background}>
                    <div className={styles.background3}/>
                    <div className={styles.background2}/>
                    <div className={styles.background1}/>
                </div>
                <Container className={styles.container}>
                    <Row className={styles.row}>
                        <Col sm={10} md={8} lg={6} xl={6}>
                            <Card className={styles.card}>
                                <Card.Body className={styles.body}>
                                    <FontAwesomeIcon size="4x" color="#4CAF50" icon={faCheckCircle}/>
                                    <h1 className={styles.title}>Your payment has been successful.</h1>
                                    <span className={styles.span}>
                                        <FontAwesomeIcon className={styles.icon} color="#625a74" icon={faQuoteRight}/>
                                        Thank you for your subscription with SearchBase. An automated payment receipt will be sent to your registered email.
                                        <FontAwesomeIcon className={styles.icon} color="#625a74" icon={faQuoteLeft}/>
                                    </span>
                                    <Link className={styles.link} to={"/"}>Back to Home</Link>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

export default SuccessPayment;