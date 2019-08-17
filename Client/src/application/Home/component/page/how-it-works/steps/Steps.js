import React from 'react';
import styles from './steps.module.css'
import {Col, Container, Image, Row} from "react-bootstrap";
import TextItem from "./text-item/TextItem";

const Steps = () => {
    return (
        <div>
            <div className={styles.section1}>
                <Container>
                    <Row>
                        <Col xs={{span: 2}}>
                            <div className={styles.arrow0}/>
                            <div className={styles.image_wrapper1}>
                                <Image className={styles.image1} fluid src="./assets/img/how-it-works/businessman.svg"/>
                            </div>
                        </Col>
                        <Col xs={5}>
                            <TextItem number="01" title="Automate non-revenue generating tasks"
                                      text="Scale communication and increase outreach by automating engagement."/>
                            <div className={styles.arrow1}/>
                        </Col>
                        <Col xs={4}>
                            <div className={styles.image_wrapper2}>
                                <Image className={styles.image2} fluid src="./assets/img/how-it-works/process.svg"/>
                            </div>
                        </Col>

                    </Row>
                </Container>
            </div>
            <div className={styles.section2}>
                <Container>
                    <Row>
                        <Col xs={{span: 4}}>
                            <div className={styles.image_wrapper1}>
                                <Image fluid className={styles.image1}
                                       src="./assets/img/how-it-works/personal-text.svg"/>
                            </div>
                        </Col>
                        <Col xs={5}>
                            <TextItem number="02" title="Chatbot messaging"
                                      text="Build relationships with conversation engines through Email and Text Messaging."/>
                            <div className={styles.arrow2}/>
                        </Col>
                        <Col xs={{span: 2}}>
                            <div className={styles.image_wrapper2}>
                                <Image fluid className={styles.image2} src="./assets/img/how-it-works/messages.svg"/>
                            </div>
                        </Col>
                    </Row>
                </Container>
            </div>
            <div className={styles.section3}>
                <Container>
                    <Row>
                        <Col xs={{span: 6, offset: 1}}>
                            <div className={styles.image_wrapper1}>
                                <Image fluid className={styles.image1} src="./assets/img/how-it-works/group-chat.svg"/>
                            </div>
                        </Col>
                        <Col xs={{span: 5}}>
                            <TextItem number="03" title="Lean and Mean"
                                      text="Stay informed about your candidates and reduce the time it takes to hire."/>
                            <div className={styles.arrow3}/>
                        </Col>
                    </Row>
                </Container>
            </div>
            <div className={styles.section4}>
                <Container>
                    <Row>
                        <Col xs={{span: 5, offset: 1}}>
                            <TextItem number="04" title="Measure success"
                                      text="Track your success and discover bottlenecks slowing you down. "/>
                        </Col>
                        <Col xs={{span: 5, offset: 0}}>
                            <div className={styles.image_wrapper1}>
                                <Image fluid className={styles.image1} src="./assets/img/how-it-works/analytics.svg"/>
                            </div>
                        </Col>
                    </Row>
                </Container>
            </div>
        </div>
    );
};

export default Steps;
