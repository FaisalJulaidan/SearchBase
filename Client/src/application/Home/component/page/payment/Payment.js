import React from 'react';
import styles from "./payment.module.css"
import queryString from 'query-string';
import {Link} from "react-router-dom";
import {Container, Row, Col, Card} from "react-bootstrap";
import {Fade} from "react-reveal";
import {Steps} from 'antd';
import SignupFormPayment from "./SignupFormPayment";
import {WEBSITE_TITLE} from "../../../../../constants/config";
import pricingJSON from "../pricing/pricing.json";
import {Elements} from 'react-stripe-elements';

const {Step} = Steps;

class Payment extends React.Component {

    state = {
        currentStep: 0,
        plan: pricingJSON[pricingJSON.length - 1].id
    };

    componentDidMount() {
        document.title = "Payment | " + WEBSITE_TITLE;
    }

    render() {
        return (
            <div className={styles.wrapper}>
                <Container>
                    <Row className={styles.row_steps}>
                        <Col xs={{span: 8, offset: 2}}>
                            <Steps current={this.state.currentStep}>
                                <Step title="Sign-up"/>
                                <Step title="Payment"/>
                            </Steps>
                        </Col>
                    </Row>
                    <div>
                        <Row>
                            <Col sm={6} md={6} lg={{span: 6, offset: 1}} className={styles.col_desc}>
                                <Fade left>
                                    <h1 className={styles.text1}>You're just few minutes away from using our
                                        ChatBot!</h1>
                                    <h4 className={styles.text2}>You need to register your account to complete
                                        your purchase process.</h4>
                                </Fade>
                            </Col>
                            <Col sm={6} md xl={4}>
                                <Fade right>
                                    <div className={styles.form_wrapper}>
                                        <Card className={styles.card}>
                                            <Card.Body>
                                                {/*<h1 className={styles.title}>Sign up</h1>*/}
                                                <Elements>
                                                    <SignupFormPayment
                                                        plan={queryString.parse(this.props.location.search)?.plan}
                                                        onSignupSuccessful={this.onSignupSuccessful}/>
                                                </Elements>
                                            </Card.Body>
                                        </Card>
                                        <div className={styles.navigation}>
                                            <ul>
                                                <li><Link to={"/"}>Home</Link></li>
                                                <li><Link to={"/terms"}>Terms & Conditions</Link></li>
                                                <li><Link to={"/privacy"}>Privacy Policy</Link></li>
                                            </ul>
                                        </div>
                                    </div>
                                </Fade>
                            </Col>
                        </Row>
                    </div>
                </Container>
            </div>
        );
    }
}
export default (Payment);