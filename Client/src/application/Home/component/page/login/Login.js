import React from 'react';
import styles from './login.module.css';
import {Card, Container, Row, Form, Button, Col} from "react-bootstrap";
import {Fade} from "react-reveal";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCloud} from "@fortawesome/free-solid-svg-icons";
import {Link} from "react-router-dom";
import {WEBSITE_TITLE} from "../../../config";

const Login = () => {

    document.title = "Login | " + WEBSITE_TITLE;


    //TODO: Fix inputs bottom border when they have value - They should stay purple with inputs
    return (
        <div className={styles.wrapper}>
            <Container className={styles.container}>
                <Row>
                    <Col md={3.5}>
                        <div>
                            <Fade top>
                                <Card className={styles.card}>
                                    <Card.Body>
                                        <h1 className={styles.title}>Login</h1>
                                        <div className={styles.logo}>
                                            <FontAwesomeIcon size="6x" icon={faCloud}/>
                                            <h1 className={styles.brand_title}>
                                                SearchBase
                                            </h1>
                                        </div>
                                        <Form>
                                            <Form.Group controlId="formEmail">
                                                <Form.Control className={styles.input} type="email"
                                                              placeholder="E-mail"/>
                                            </Form.Group>

                                            <Form.Group controlId="formBPassword">
                                                <Form.Control className={styles.input} type="password"
                                                              placeholder="Password"/>
                                            </Form.Group>

                                            <Form.Group >
                                                <Button className={styles.submit} block variant="primary" type="submit">
                                                    Submit
                                                </Button>
                                            </Form.Group>

                                        </Form>
                                        <h6 className={styles.sign_up}>Don’t have an account?
                                            <Link to="/sign-up">Sign Up</Link>
                                        </h6>
                                    </Card.Body>
                                </Card>
                            </Fade>
                        </div>
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

export default Login;
