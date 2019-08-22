import React from 'react';
import styles from './pricing.module.css';
import {Card, Col, Container, Row} from "react-bootstrap";
import {Zoom} from "react-reveal";
import PricingCard from "./pricing-card/PricingCard";

const Pricing = () => {
    return (
        <div>
            <div className={styles.hero}>
                <Container className={styles.text_wrapper}>
                    <h1 className={styles.title}>Choose your plan</h1>
                    <h1 className={styles.subtitle}>SearchBase is simply designed to help you make more sales,
                        boost user interaction and revolutionise your website.</h1>
                </Container>
            </div>
            <Container className={styles.content}>
                <Row>
                    <Col>
                        <Zoom fraction={0.5}>
                            <PricingCard/>
                        </Zoom>
                    </Col>
                    <Col>
                        <Zoom fraction={0.5}>
                            <PricingCard/>
                        </Zoom>
                    </Col>
                    <Col>
                        <Zoom fraction={0.5}>
                            <PricingCard/>
                        </Zoom>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default Pricing;
