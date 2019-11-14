import React from 'react';
import styles from './roi.module.css'
import {Button, Col, Container, Row, Card} from "react-bootstrap";
import {Link} from "react-router-dom";
import Layout from "../../../hoc/layout/Layout";
import {Input, Icon} from 'antd';
import ResultItem from "./result-item/ResultItem";

class ROI extends React.Component {

    state = {
        consultants: "",
    };

    render() {
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
                                            <span className={styles.input_title}>Consultant number</span>
                                            <Input className={styles.input} size="large" placeholder="15"
                                                   value={this.state.consultants}
                                                   onChange={e => {
                                                       if (isNaN(e.target.value))
                                                           return;
                                                       this.setState({consultants: e.target.value})
                                                   }}/>
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
                                        <div className={styles.results_title_wrapper}>
                                            <div className={styles.results_title}>
                                                <hr/>
                                                <h1>Results</h1>
                                                <hr/>
                                            </div>
                                        </div>
                                        <Row className={styles.row_result}>
                                            <Col>
                                                <ResultItem title="Revenue generated per yr." currency valSize="large"
                                                            value={this.state.consultants * 3612}/>
                                            </Col>
                                        </Row>
                                        <Row className={styles.row_result_text}>
                                            <Col md={{span: 8, offset: 2}}>
                                                <h1>So, per year the following is potential...</h1>
                                            </Col>
                                        </Row>
                                        <Row className={styles.row_result}>
                                            <Col>
                                                <ResultItem title="Hours Saved per yr."
                                                            value={this.state.consultants * 84}/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Productivity Pounds Saved per yr." value='0'/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Addt'l Revenue per yr." currency value='0'/>
                                            </Col>
                                        </Row>
                                        <Row className={styles.row_result_text}>
                                            <Col md={{span: 8, offset: 2}}>
                                                <h1>...in other words, automating activities like
                                                    NPS surveys, sales follow-up, candidate engagement and more
                                                    equals...</h1>
                                            </Col>
                                        </Row>
                                        <Row className={styles.row_result}>
                                            <Col>
                                                <ResultItem title="Hours Saved per yr."
                                                            valSize="small"
                                                            value={this.state.consultants * 84}/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Productivity Pounds Saved per yr."
                                                            valSize="small" value='0'/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Addt'l Revenue per yr." valSize="small"
                                                            currency
                                                            value='0'/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Hours Saved per yr."
                                                            valSize="small"
                                                            value={this.state.consultants * 84}/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Productivity Pounds Saved per yr."
                                                            valSize="small" value='0'/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="Addt'l Revenue per yr." valSize="small"
                                                            currency
                                                            value='0'/>
                                            </Col>
                                        </Row>
                                        <Row>
                                            <Col>
                                                <Link to="/get-started">
                                                    <Button className={styles.button} variant="outline-light">Book a
                                                        demo</Button>
                                                </Link>
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
    }
}

export default ROI;