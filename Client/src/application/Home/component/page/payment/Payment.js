import React from 'react';
import styles from "./payment.module.css"
import queryString from 'query-string';
import {Container, Row, Col, Card} from "react-bootstrap";
import {Fade} from "react-reveal";
import {Steps} from 'antd';
import SignupFormPayment from "./SignupFormPayment";
import {WEBSITE_TITLE} from "../../../../../constants/config";
import Layout from "../../../hoc/layout/Layout";
import pricingJSON from "../pricing/pricing";

import {Elements} from 'react-stripe-elements';
import PaymentForm from "./PaymentForm";

const {Step} = Steps;

class Payment extends React.Component {

    state = {
        planID: queryString.parse(this.props.location.search)?.plan,
        currentStep: 1,
        email: "", //This Will be filled through SignUp form Callback
        firstName: "", //This Will be filled through SignUp form Callback
        lastName: "" //This Will be filled through SignUp form Callback
    };

    componentDidMount() {
        document.title = "Payment | " + WEBSITE_TITLE;
    }

    onSignupSuccessful = (email, firstName, lastName) => {
        this.setState({
                currentStep: 1,
                email: email,
                firstName: firstName,
                lastName: lastName
            }
        )
    };

    render() {

        const plan = pricingJSON.find(plan => {
            if (plan.id === this.state.planID)
                return plan;
        });

        return (
            <Layout>
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
                            {this.state.currentStep === 0 ? (
                                <Row>
                                    <Col sm={6} md={6} lg={{span: 6, offset: 1}} className={styles.col_desc}>
                                        <Fade left>
                                            <h1 className={styles.text1}>You're just few minutes away from using our
                                                ChatBot!</h1>
                                            <h4 className={styles.text2}>You need to register your account to complete
                                                your payment process.</h4>
                                        </Fade>
                                    </Col>
                                    <Col sm={6} md xl={4}>
                                        <Fade right>
                                            <div className={styles.form_wrapper}>
                                                <Card className={styles.card}>
                                                    <Card.Body>
                                                        {/*<h1 className={styles.title}>Sign up</h1>*/}
                                                        <SignupFormPayment
                                                            planID={this.state.planID}
                                                            onSignupSuccessful={this.onSignupSuccessful}/>
                                                    </Card.Body>
                                                </Card>
                                            </div>
                                        </Fade>
                                    </Col>
                                </Row>
                            ) : (
                                <Elements>
                                    <Row>
                                        <Col sm={6} md={6} lg={{span: 6}} className={styles.col_desc}>
                                            <h1 className={styles.title}>{plan.title}</h1>
                                            <hr/>
                                            <ul className={styles.list}>
                                                {plan.items?.map((item, key) => {
                                                    return <li key={key}>{item}</li>
                                                })}
                                            </ul>
                                        </Col>
                                        <Col sm={6} md lg={{offset: 1}} xl={4}>
                                            <div className={styles.form_wrapper}>
                                                <Card className={styles.card}>
                                                    <Card.Body>
                                                        <h1 className={styles.title}>Pay with card</h1>
                                                        <PaymentForm
                                                            planID={this.state.planID}
                                                            email={this.state.email}/>
                                                        <h6 className={styles.sign_up}>Powered by
                                                            <a href="https://stripe.com">Stripe</a>
                                                        </h6>
                                                    </Card.Body>
                                                </Card>
                                            </div>
                                        </Col>
                                    </Row>
                                </Elements>
                            )}

                        </div>
                    </Container>
                </div>
            </Layout>
        );
    }
}

export default Payment;