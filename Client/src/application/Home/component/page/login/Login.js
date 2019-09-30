import React from 'react';
import styles from './login.module.css';
import {Card, Container, Row, Col} from "react-bootstrap";
import {Fade} from "react-reveal";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCloud} from "@fortawesome/free-solid-svg-icons";
import {Link} from "react-router-dom";
import {WEBSITE_TITLE} from '../../../../../constants/config';
import LoginForm from "./LoginForm";

const Login = () => {

    document.title = "Login | " + WEBSITE_TITLE;

    return (
        <div className={styles.wrapper}>
            <Container>
                <Row className={styles.row}>
                    <Col  sm={8} md={6} lg={5} xl={4}>
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
                                    <LoginForm/>
                                    {/*<h6 className={styles.sign_up}>Don’t have an account?*/}
                                    {/*    <Link to="/signup">Sign Up</Link>*/}
                                    {/*</h6>*/}
                                </Card.Body>
                            </Card>
                        </Fade>
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
