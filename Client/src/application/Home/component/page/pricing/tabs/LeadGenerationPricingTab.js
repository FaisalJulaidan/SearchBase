import React from 'react';
import styles from './lead-generation-pricing-tab.module.css';
import {Link} from "react-router-dom";
import {Button, Col, Row, Card} from "react-bootstrap";
import PricingItem from "../pricing-item/PricingItem";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faChevronRight} from "@fortawesome/free-solid-svg-icons";
import plansJSON from "./lead-generation-plans.json";

const AgencyPricingTab = () => {


    let plans = plansJSON.map((plan, key) => {
        return (
            <Col className={styles.col_item} xs={{span: 10, offset: 1}} sm={{span: 8, offset: 2}}
                 md={{span: 4, offset: 0}}
                 key={key}>
                <PricingItem id={plan.id} plan={plan} hideSubtitle={true} showAutomationButton={true}/>
            </Col>
        );
    });
    return (
        <div className={styles.wrapper}>
            <div>
                <Card className={styles.card}>
                    <Card.Body className={styles.pricing_card_body}>
                        <Row>
                            {plans}
                            <Col className={styles.col_item} xs={{span: 10, offset: 1}} sm={{span: 8, offset: 2}}
                                 md={{span: 8, offset: 0}}>
                                <div className={styles.product_wrapper}>
                                    <div>
                                        <h1>CHATBOTS</h1>
                                        <p>Our chatbots help you spend less time screening and qualifying
                                            candidates.</p>
                                    </div>
                                    <Link to="/how-it-works#chatbot">learn more<FontAwesomeIcon className={styles.icon}
                                                                                                icon={faChevronRight}/>
                                    </Link>
                                </div>
                                <div className={styles.product_wrapper}>
                                    <div>
                                        <h1>SMS outreach</h1>
                                        <p>Candidates may have access to the internet, so we have developed a solution
                                            that
                                            works, offline and online.</p>
                                    </div>
                                    <Link to="/how-it-works#sms">learn more<FontAwesomeIcon className={styles.icon}
                                                                                            icon={faChevronRight}/>
                                    </Link>
                                </div>
                                <div className={styles.product_wrapper}>
                                    <div>
                                        <h1>Candidate Activation</h1>
                                        <p>Connect with candidates that they have never engaged with or have simply lost
                                            communication with.</p>
                                    </div>
                                    <Link to="/how-it-works#candidate">learn more<FontAwesomeIcon
                                        className={styles.icon}
                                        icon={faChevronRight}/>
                                    </Link>
                                </div>
                                <div className={styles.product_wrapper}>
                                    <div>
                                        <h1>Automation & Engagement</h1>
                                        <p>Set up a tailored automation sequences that help you improve the efficiency
                                            of your workflow.</p>
                                    </div>
                                    <Link to="/how-it-works#engagement">learn more<FontAwesomeIcon
                                        className={styles.icon}
                                        icon={faChevronRight}/>
                                    </Link>
                                </div>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>
            </div>
            <div>
                <Row>
                    <Col md={{span: 10, offset: 1}} className={styles.col_demo_text}>
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

export default AgencyPricingTab;