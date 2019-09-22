import React from 'react';
import styles from './pricing.module.css';
import {Card, Col, Container, Row} from "react-bootstrap";
import {Zoom} from "react-reveal";
import PricingCard from "./pricing-card/PricingCard";
import Layout from "../../../hoc/layout/Layout";
import {ReactComponent as Wave} from "../../../hoc/hero-layout/wave.svg";
import pricingJSON from './pricing.json';

const Pricing = () => {

    let pricing = pricingJSON.map((plan, key) => {
        return (
            <Col key={key}>
                    <PricingCard title={plan.title} subtitle={plan.subtitle} price={plan.price} items={plan.items}/>
            </Col>
        );
    });

    return (
        <Layout background={"linear-gradient(to bottom, #ffffff, #ffffff, #ebebf2)"}>
            <div>
                <div className={styles.hero}>
                    <Container>
                        <Row>
                            <Col className={styles.text_wrapper}>
                                <h1 className={styles.title}>Choose your plan</h1>
                                <h1 className={styles.subtitle}>SearchBase is simply designed to help you make more
                                    sales,
                                    boost user interaction and revolutionise your website.</h1>
                            </Col>
                        </Row>
                    </Container>
                    <Wave className={styles.wave}/>
                </div>
                <Container className={styles.content}>
                    <Row>
                        {pricing}
                    </Row>
                </Container>
            </div>
        </Layout>
    );
};

export default Pricing;
