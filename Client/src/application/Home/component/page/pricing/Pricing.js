import React from 'react';
import styles from './pricing.module.css';
import {Col, Container, Row, Button} from "react-bootstrap";
import {Link} from "react-router-dom";
import EmailShare from "react-email-share-link";
import PricingCard from "./pricing-card/PricingCard";
import Layout from "../../../hoc/layout/Layout";
import {ReactComponent as Wave} from "../../../hoc/hero-layout/wave.svg";
import pricingJSON from './pricing.json';
import {WEBSITE_TITLE} from "../../../../../constants/config";

const Pricing = () => {

    document.title = "Pricing | " + WEBSITE_TITLE;

    let pricing = pricingJSON.map((plan, key) => {
        return (
            <Col className={styles.col_card} xs={{span:10,offset:1}} sm={{span:8,offset:2}} md={{span:4,offset:0}} key={key}>
                <PricingCard id={plan.id} plan={plan}/>
            </Col>
        );
    });

    return (
        <Layout>
            <div>
                <div className={styles.hero}>
                    <Container>
                        <Row>
                            <Col className={styles.text_wrapper}>
                                <h1 className={styles.title}>Boost candidates interaction and automate every mundane task in your business.</h1>
                            </Col>
                        </Row>
                    </Container>
                    <Wave className={styles.wave}/>
                </div>
                <Container className={styles.content}>
                    <Row>
                        {pricing}
                    </Row>
                    <Row className={styles.row_enterprise}>
                        <Col md={10} lg={8}>
                            <h1>Need more?</h1>
                        </Col>
                        <Col md={12} lg={10} className={styles.desc_col}>
                            <span>We offer additional enterprise services — if you need features not available in the current plans to help your enterprise requirements get going, please let us know. If you are interested in partnering with us around technology, services, or go-to-market, we’d love to have a conversation!</span>
                        </Col>
                        <Col md={8}>
                            <Link to="/get-started">
                                <Button variant="light" className={styles.demo_button}>Request a demo</Button>
                            </Link>
                            <Button variant="outline-light" className={styles.contact_button}>
                                <EmailShare email="info@SearchBase.com"
                                            subject="Contact"
                                            body="Hi, I would like to talk about...">
                                    {link => (<a href={link} data-rel="external">Contact us</a>)}
                                </EmailShare>
                            </Button>
                        </Col>
                    </Row>
                </Container>
            </div>
        </Layout>
    );
};

export default Pricing;
