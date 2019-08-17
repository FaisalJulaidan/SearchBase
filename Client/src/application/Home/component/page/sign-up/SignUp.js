import React from 'react';
import styles from "./sign-up.module.css";
import {Button, Card, Col, Container, Form, Row} from "react-bootstrap";
import {Fade} from "react-reveal";
import {Link} from "react-router-dom";
import {WEBSITE_TITLE} from "../../../config";

const SignUp = () => {

    document.title = "SignUp | " + WEBSITE_TITLE;

    return (
        <div className={styles.wrapper}>
            <Container className={styles.container}>
                <Row>
                    <Col sm={6} md={6} lg={{span: 6, offset: 1}} className={styles.col_desc}>
                        <Fade left>
                            <h1 className={styles.text1}>You're just few minutes away from using our ChatBot!</h1>
                            <h1 className={styles.text2}>Registration is free and takes less than 30 seconds (no credit
                                card required).</h1>
                        </Fade>
                    </Col>
                    <Col sm={{span: 6}} md="auto">
                        <Card className={styles.card}>
                            <Card.Body>
                                <h1 className={styles.title}>Sign up</h1>
                                <Form>
                                    <Form.Group controlId="formEmail">
                                        <Form.Control className={styles.input} type="email"
                                                      placeholder="E-mail"/>
                                    </Form.Group>

                                    <Form.Group controlId="formEmailConfirm">
                                        <Form.Control className={styles.input} type="email"
                                                      placeholder="Confirm E-mail"/>
                                    </Form.Group>

                                    <Form.Group controlId="formPassword">
                                        <Form.Control className={styles.input} type="password"
                                                      placeholder="Password"/>
                                    </Form.Group>

                                    <Form.Group controlId="formPasswordConfirm">
                                        <Form.Control className={styles.input} type="password"
                                                      placeholder="Confirm Password"/>
                                    </Form.Group>

                                    <Button className={styles.submit} block variant="primary" type="submit">
                                        Submit
                                    </Button>

                                </Form>
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
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default SignUp;
