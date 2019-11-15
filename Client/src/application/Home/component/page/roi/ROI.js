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
        let hoursSavedPerCons = 85;
        let revenueSavedPerCons = 43;
        let revenueGenerated = this.state.consultants * hoursSavedPerCons * revenueSavedPerCons;
        let hoursSavedPerYear = this.state.consultants * 85;
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
                                        <Col xs={12}>
                                            <span className={styles.input_question}>How many recruiters & consultants work in your firm?</span>
                                        </Col>
                                        <Col xs={{span: 4, offset: 4}}>
                                            {/*<span className={styles.input_title}>Consultant number</span>*/}
                                            <Input className={styles.input} size="large" placeholder="50"
                                                   value={this.state.consultants}
                                                   onChange={e => {
                                                       if (isNaN(e.target.value))
                                                           return;
                                                       this.setState({consultants: e.target.value})
                                                   }}/>
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
                                                <ResultItem title="revenue generated per year" currency valSize="large"
                                                            value={revenueGenerated}/>
                                            </Col>
                                        </Row>
                                        <Row className={styles.row_result_text}>
                                            <Col md={{span: 8, offset: 2}}>
                                                <h1>So, per year the following is potential...</h1>
                                            </Col>
                                        </Row>
                                        <Row className={styles.row_result}>
                                            <Col>
                                                <ResultItem title="Hours saved"
                                                            value={hoursSavedPerYear}/>
                                            </Col>
                                            <Col>
                                                <ResultItem title="£ saved per consultant" currency
                                                            value={this.state.consultants.length === 0 ? 0 : hoursSavedPerCons * revenueSavedPerCons}/>
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
                                            <Col xs={3}>
                                                <ResultItem title="Days"
                                                            value={((this.state.consultants * 84) / 24).toFixed()}/>
                                            </Col>
                                            <Col xs={3}>
                                                <ResultItem title="Audiobooks"
                                                            value={(this.state.consultants * 84 / 11).toFixed()}/>
                                            </Col>
                                            <Col xs={3}>
                                                <ResultItem title="Ferrari 488"
                                                            value={(revenueGenerated / 195363).toFixed()}/>
                                            </Col>
                                            <Col xs={3}>
                                                <ResultItem title="Gold Britannia Coin"
                                                            value={(revenueGenerated / 1177).toFixed()}/>
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