import React from 'react';
import styles from './key-features.module.css'
import {Col, Container, Image, Row} from "react-bootstrap";
import {Slide} from "react-reveal";

const KeyFeatures = (props) => {
    return (
        <Container id={props.id}>
            <Row className={styles.center}>
                <Col xs={{span:8,offset:2,order:2}} md={{span:5,offset:0,order:0}}>
                    <h1 className={styles.title}>Key Features</h1>
                    <h1 className={styles.subtitle}>SearchBase works within your current ecosystem,
                        and is easy to
                        plug-and-play.</h1>
                    <ul className={styles.list}>
                        <Slide bottom big>
                            <li>ATS/CRM</li>
                            <li>Calendars</li>
                            <li>Messaging Apps</li>
                            <li>Job Boards</li>
                            <li>Learning & Development</li>
                        </Slide>
                    </ul>

                </Col>
                <Col xs={{span:8,offset:2,order:1}} md={{span:7,offset:0,order:0}}>
                    <div className={styles.image_wrapper}>
                        <Image className={styles.image} src="assets/img/home/os.svg"/>
                    </div>
                </Col>
            </Row>

        </Container>
    );
};

export default KeyFeatures;
