import React from 'react';
import {WEBSITE_TITLE} from "../../../config";
import styles from "./get-started.module.css";
import {Button, Card, Col, Container, Form, Row} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";

const GetStarted = () => {

    document.title = "Get Started | " + WEBSITE_TITLE;

    return (
        <Layout background="#FBFAFF">
            <div className={styles.wrapper}>
                <Container>
                    <Row>
                        <Col md={{span: 10, offset: 1}} lg={{span: 8, offset: 2}}>
                            <Card className={styles.card}>
                                <Card.Body>
                                    <h1 className={styles.title}>Get started with SearchBase</h1>
                                    <h4 className={styles.subtitle}>Interested in our products? Fill out this form to
                                        arrange a demo</h4>
                                    <Form>
                                        <Form.Group controlId="formName">
                                            <Form.Label className={styles.label}>Full Name</Form.Label>
                                            <Form.Control className={styles.input} placeholder="John Lennon"/>
                                        </Form.Group>

                                        <Form.Group controlId="formEmail">
                                            <Form.Label className={styles.label}>E-Mail</Form.Label>
                                            <Form.Control className={styles.input} type="email"
                                                          placeholder="example@mail.com"/>
                                        </Form.Group>

                                        <Form.Group controlId="formCompany">
                                            <Form.Label className={styles.label}>Company Name</Form.Label>
                                            <Form.Control className={styles.input} placeholder="Your company name"/>
                                        </Form.Group>

                                        <Form.Group controlId="formPhone">
                                            <Form.Label className={styles.label}>Phone Number</Form.Label>
                                            <Form.Control className={styles.input} placeholder="+123456789"/>
                                        </Form.Group>

                                        <Form.Group controlId="mCRMSelect">
                                            <Form.Label className={styles.label}>CRM Type</Form.Label>
                                            <Form.Control className={styles.input} as="select">
                                                <option>Adapt</option>
                                                <option>Bullhorn</option>
                                                <option>RDB Pro Net</option>
                                                <option>Microdec</option>
                                                <option>JobDiva</option>
                                                <option>JobAdder</option>
                                                <option>Vincere</option>
                                                <option>Greenhouse</option>
                                                <option>Eploy</option>
                                                <option>Zoho</option>
                                                <option>Mercury Xrm</option>
                                                <option>Job Science</option>
                                                <option>Other</option>
                                            </Form.Control>
                                        </Form.Group>

                                        <Form.Group controlId="formChecbox">
                                            <Form.Check className={styles.checkbox}
                                                        custom
                                                        type="checkbox"
                                                        label="Subscribe to newsletters"/>
                                        </Form.Group>

                                        <Button className={styles.submit} block variant="primary" type="submit">
                                            Submit
                                        </Button>

                                    </Form>
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
