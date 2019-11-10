import React from 'react';
import styles from './customers.module.css';
import {Col, Container, Row} from "react-bootstrap";
import CustomerCard from "./customer-card/CustomerCard";
import {Fade} from "react-reveal";
import reviewsJson from './reviews.json'
import {BREAKPOINTS} from "../../../../../../constants/config";

const Customers = (props) => {

    let reviews = reviewsJson.map((review, i) => {

        let fadeAnim = {};
        if (window.innerWidth > BREAKPOINTS.md) {
            switch (i % 3) {
                case 0:
                    fadeAnim["left"] = true;
                    break;
                case 1:
                    fadeAnim["bottom"] = true;
                    break;
                case 2:
                    fadeAnim["right"] = true;
                    break;
                default:
                    fadeAnim = {};
                    break;
            }
        }


        return (
            <Col className={styles.card_col} key={i} md={4}>
                <Fade {...fadeAnim} fraction={0.5}>
                    <CustomerCard background={review.background}
                                  img={review.img}
                                  name={review.name}
                                  title={review.title}
                                  review={review.review}/>
                </Fade>
            </Col>
        )
    });

    return (
        <Container id={props.id}>
            <Row>
                <Col xs={12} className={styles.header_col}>
                    <h1 className={styles.section_header}>Customers' Review</h1>
                </Col>
            </Row>
            <Row>
                {reviews}
            </Row>
        </Container>
    );
};

export default Customers;
