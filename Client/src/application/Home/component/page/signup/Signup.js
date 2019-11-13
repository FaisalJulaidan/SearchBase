import React from 'react';
import styles from "./signup.module.css";
import {Card, Col, Container, Row} from "react-bootstrap";
import {Fade} from "react-reveal";
import {Link} from "react-router-dom";
import {WEBSITE_TITLE} from '../../../../../constants/config';
import SignupForm from "./SignupForm";

const Signup = () => {

    document.title = "Signup | " + WEBSITE_TITLE;

    return (
        <div className={styles.wrapper}>
            <Container className={styles.container}>
                <Row>
                    <Col md={6} lg={{span: 6, offset: 1}} className={styles.col_desc}>
                        <Fade left>
                            <h1 className={styles.text1}>You're just few minutes away from using our ChatBot!</h1>
                            <h1 className={styles.text2}>Registration is free and takes less than 30 seconds (no credit
                                card required).</h1>
                        </Fade>
                    </Col>
                    <Col md xl={4}>
                        <Fade right>
                            <div className={styles.form_wrapper}>
                                <Card className={styles.card}>
                                    <Card.Body>
                                        <h1 className={styles.title}>Sign up</h1>
                                        <SignupForm/>
                                        <h6 className={styles.sign_up}>Or log into an
                                            <Link to="/login">existing account!</Link>
                                        </h6>
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
            </Container>
        </div>
    );
};

export default Signup;
