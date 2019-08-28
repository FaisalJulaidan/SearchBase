import React from 'react';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import styles from "./get-started.module.css";
import {Card, Col, Container, Row} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";
import DemoForm from "./DemoForm";

const GetStarted = () => {

    document.title = "Get Started | " + WEBSITE_TITLE;

    return (
        <Layout background={"#FEFEFE"}>
            <div className={styles.wrapper}>
                <Container>
                    <Row>
                        <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}}>
                            <Card className={styles.card}>
                                <Card.Body>
                                    <h1 className={styles.title}>Get started with SearchBase</h1>
                                    <h4 className={styles.subtitle}>Interested in our products? Fill out this form to
                                        arrange a demo</h4>

                                    <DemoForm/>

                                    <h6 className={styles.bottom_desc}>The Demo is free of charge and provided for your
                                        evaluation</h6>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                </Container>
            </div>
        </Layout>
    );
};


export default GetStarted;
