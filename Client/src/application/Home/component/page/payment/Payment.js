import React from 'react';
import styles from "./payment.module.css"
import queryString from 'query-string';
import {Link} from "react-router-dom";
import {Container, Row, Col, Card} from "react-bootstrap";
import {Fade} from "react-reveal";
import SignupFormPayment from "./SignupFormPayment";
import {WEBSITE_TITLE} from "../../../../../constants/config";
import pricingJSON from "../pricing/pricing.json";
import {Elements} from 'react-stripe-elements';

class Payment extends React.Component {

    state = {
        currentStep: 0,
        planID: pricingJSON[pricingJSON.length - 1].id
    };

    componentDidMount() {
        document.title = "Payment | " + WEBSITE_TITLE;
    }

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
                        <Col lg={10} xl={8}>
                            <Fade bottom>
                                <Card className={styles.card}>
                                    <Card.Body>
                                        <Row>
                                            <Col sm={12} md={6} className={styles.col_desc}>
                                                <h1 className={styles.text1}>Your clients are waiting for you, what are
                                                    you
                                                    waiting for?</h1>
                                                <hr/>
                                                <h4 className={styles.text2}>You need to register your account to
                                                    continue
                                                    your purchase process.</h4>
                                                <div className={styles.navigation}>
                                                    <ul>
                                                        <li><Link to={"/"}>Home</Link></li>
                                                        <li><Link to={"/terms"}>Terms & Conditions</Link></li>
                                                        <li><Link to={"/privacy"}>Privacy Policy</Link></li>
                                                    </ul>
                                                </div>
                                            </Col>
                                            <Col sm={12} md={6}>
                                                <div className={styles.form_wrapper}>
                                                    <Elements>
                                                        <SignupFormPayment
                                                            planID={queryString.parse(this.props.location.search)?.plan}
                                                            onSignupSuccessful={this.onSignupSuccessful}/>
                                                    </Elements>
                                                </div>
                                                <div className={styles.navigation2}>
                                                    <ul>
                                                        <li><Link to={"/"}>Home</Link></li>
                                                        <li><Link to={"/terms"}>Terms & Conditions</Link></li>
                                                        <li><Link to={"/privacy"}>Privacy Policy</Link></li>
                                                    </ul>
                                                </div>

                                            </Col>
                                        </Row>
                                    </Card.Body>
                                </Card>
                            </Fade>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

export default (Payment);