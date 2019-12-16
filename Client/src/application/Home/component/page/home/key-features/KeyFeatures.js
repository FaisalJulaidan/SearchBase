import React from 'react';
import styles from './key-features.module.css'
import {Col, Container, Image, Row} from "react-bootstrap";
import {Slide} from "react-reveal";
import {getLink} from "helpers";

const KeyFeatures = (props) => {
    return (
        <Container id={props.id}>
            <Row className={styles.center}>
                <Col className={styles.col_text} xs={{span:12,order:2}} sm={{span:10,offset:1,order:2}} md={{span:5,offset:0,order:0}}>
                    <h1 className={styles.title}>Key Features</h1>
                    <hr/>
                    <h1 className={styles.subtitle}>SearchBase works within your current ecosystem,
                        and is easy to
                        plug-and-play.</h1>
                    <ul className={styles.list}>
                        <Slide bottom big cascade>
                            <div>
                            <li>ATS/CRM</li>
                            <li>Calendars</li>
                            <li>Messaging Apps</li>
                            <li>Job Boards</li>
                            <li>Learning & Development</li>
                            </div>
                        </Slide>
                    </ul>

                </Col>
                <Col xs={{span:12,offset:0,order:1}} md={{span:7,offset:0,order:0}}>
                    <div className={styles.image_wrapper}>
                        <Image className={styles.image}
                               src={"/images/home/home/os.svg"}/>
                    </div>
                </Col>
            </Row>

        </Container>
    );
};

export default KeyFeatures;
