import React from 'react';
import styles from './enterprise-pricing-tab.module.css';
import {Link} from "react-router-dom";
import {Button, Col, Row, Card} from "react-bootstrap";
import EmailShare from "react-email-share-link";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faChevronRight} from "@fortawesome/free-solid-svg-icons";

const EnterprisePricingTab = () => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.desc_wrapper}>
                <Row>
                    <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}}>
                        <h1>Enterprise</h1>
                        <p>At SearchBase, our customers tell us they want us to be a strategic partner, not a
                            transactional vendor. They want us to apply our fully specialised solutions to help them
                            meet their goals. And we do.
                        </p>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Button variant="primary" className={styles.contact_button}>
                            <EmailShare email="info@SearchBase.com"
                                        subject="Contact"
                                        body="Hi, I would like to talk about...">
                                {link => (<a href={link} data-rel="external">Contact us</a>)}
                            </EmailShare>
                        </Button>
                        <Link to="/how-it-works" className={styles.learn}>Learn How it works ></Link>
                    </Col>
                </Row>
            </div>
            <div>
                <Row>
                    <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Card.Body className={styles.product_card_body}>
                                <div>
                                    <h1>CHATBOTS</h1>
                                    <p>Our chatbots help you spend less time screening and qualifying candidates.</p>
                                </div>
                                <Link to="/how-it-works#chatbot">learn more<FontAwesomeIcon className={styles.icon}
                                                                                            icon={faChevronRight}/>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Card.Body className={styles.product_card_body}>
                                <div>
                                    <h1>SMS outreach</h1>
                                    <p>Candidates may have access to the internet, so we have developed a solution that
                                        works, offline and online.</p>
                                </div>
                                <Link to="/how-it-works#sms">learn more<FontAwesomeIcon className={styles.icon}
                                                                                        icon={faChevronRight}/>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Card.Body className={styles.product_card_body}>
                                <div>
                                    <h1>Candidate Activation</h1>
                                    <p>Connect with candidates that they have never engaged with or have simply lost
                                        communication with.</p>
                                </div>
                                <Link to="/how-it-works#candidate">learn more<FontAwesomeIcon className={styles.icon}
                                                                                              icon={faChevronRight}/>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Card.Body className={styles.product_card_body}>
                                <div>
                                    <h1>Automation & Engamenet</h1>
                                    <p>Set up a tailored automation sequences that help you improve the efficiency of
                                        your workflow.</p>
                                </div>
                                <Link to="/how-it-works#engagement">learn more<FontAwesomeIcon className={styles.icon}
                                                                                               icon={faChevronRight}/></Link>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </div>
            <div>
                <Row>
                    <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}}  className={styles.col_demo_text}>
                        <h1>Join the 100+ businesses which are using SearchBase to connect with their customers.</h1>
                    </Col>
                </Row>
                <Row>
                    <Col className={styles.col_demo_button}>
                        <Button as={Link} to={"/get-started"} variant="primary" className={styles.demo_button}>Get a
                            demo</Button>
                    </Col>
                </Row>
            </div>
        </div>
    );
};

export default EnterprisePricingTab;