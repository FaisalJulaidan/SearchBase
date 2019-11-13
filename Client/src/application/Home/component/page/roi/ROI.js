import React from 'react';
import styles from './roi.module.css'
import {Col, Container, Row, Card} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";
import {Input, Icon} from 'antd';
import ResultItem from "./result-item/ResultItem";

const ROI = () => {
    return (
        <Layout>
            <Container className={styles.container}>
                <Row>
                    <Col md={{span: 8, offset: 2}} className={styles.col_intro}>
                        <h1>What could you save with SearchBase?</h1>
                        <hr/>
                        <h4>Use our super simple ROI calculator below to learn more</h4>
                    </Col>
                </Row>
                <Row>
                    <Col md={{span: 10, offset: 1}} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Container>
                                <Row className={styles.row_input}>
                                    <Col>
                                        <span className={styles.input_title}>staff number</span>
                                        <Input className={styles.input} size="large" placeholder="50"/>
                                    </Col>
                                    <Col>
                                        <span className={styles.input_title}>staff number</span>
                                        <Input className={styles.input} size="large" placeholder="20"/>
                                    </Col>
                                    <Col>
                                        <span className={styles.input_title}>staff number</span>
                                        <Input className={styles.input} size="large" placeholder="30"/>
                                    </Col>
                                </Row>
                                <div className={styles.results}>
                                    <div className={styles.results_title}>
                                        <h1>Results</h1>
                                        <hr/>
                                    </div>
                                    <Row className={styles.row_result}>
                                        <Col>
                                            <ResultItem title="Revenue generated per yr." currency valSize="large" value='20'/>
                                        </Col>
                                    </Row>
                                    <Row className={styles.row_result}>
                                        <Col>
                                            <ResultItem title="Hours Saved per yr." value='20'/>
                                        </Col>
                                        <Col>
                                            <ResultItem title="Productivity Pounds Saved per yr." value='20'/>
                                        </Col>
                                        <Col>
                                            <ResultItem title="Addt'l Revenue per yr." currency value='20'/>
                                        </Col>
                                    </Row>
                                </div>
                            </Container>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </Layout>
    );
};

export default ROI;