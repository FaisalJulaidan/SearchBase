import React from 'react';
import styles from './statistics.module.css'
import {Col, Container, Row} from "react-bootstrap";
import itemsJSON from './items.json'
import {Fade} from "react-reveal";

const Statistics = (props) => {

    let items = itemsJSON.map((item, i) => {
        // let span = {};
        // if (i % 2 === 0) {
        //     span = {span: 5, offset: 1};
        // } else {
        //     span = {span: 5, offset: 0};
        // }
        return (
            <Col key={i} xs={6}>
                <div className={styles.text_section}>
                    <Fade left big>
                        <h1 className={styles.intro}>{item.title}</h1>
                        <h3 className={styles.title}>{item.subtitle}</h3>
                        <h6 className={styles.text}>{item.text}</h6>
                    </Fade>
                </div>
            </Col>
        )
    });

    return (
        <Container id={props.id}>
            <Row>
                {items}
            </Row>
        </Container>
    );
};

export default Statistics;
