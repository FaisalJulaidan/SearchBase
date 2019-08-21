import React from 'react';
import {connect} from 'react-redux';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import styles from "./get-started.module.css";
import {Button, Card, Col, Container, Form, Row} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";

import {authActions} from '../../../../../store/actions/index';

const GetStarted = (props) => {

    document.title = "Get Started | " + WEBSITE_TITLE;

    const handleSubmit = (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        let name = event.target.elements.name.value;
        let email = event.target.elements.email.value;
        let companyName = event.target.elements.companyName.value;
        let phone = event.target.elements.phone.value;
        let crm = event.target.elements.crm.value;
        let subscribe = event.target.elements.letter.value;
        // console.log(name);
        // console.log(email);
        // console.log(companyName);
        // console.log(phone);
        // console.log(crm);
        // console.log(subscribe);
        props.dispatch(authActions.demoRequest(name, email, companyName, phone, crm, subscribe));
    };

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
                                    <Form onSubmit={handleSubmit}>
                                        <Form.Group controlId="name">
                                            <Form.Label className={styles.label}>Full Name</Form.Label>
                                            <Form.Control className={styles.input} placeholder="John Lennon"/>
                                        </Form.Group>

                                        <Form.Group controlId="email">
                                            <Form.Label className={styles.label}>E-Mail</Form.Label>
                                            <Form.Control className={styles.input} type="email"
                                                          placeholder="example@mail.com"/>
                                        </Form.Group>

                                        <Form.Group controlId="companyName">
                                            <Form.Label className={styles.label}>Company Name</Form.Label>
                                            <Form.Control className={styles.input} placeholder="Your company name"/>
                                        </Form.Group>

                                        <Form.Group controlId="phone">
                                            <Form.Label className={styles.label}>Phone Number</Form.Label>
                                            <Form.Control className={styles.input} placeholder="+123456789"/>
                                        </Form.Group>

                                        <Form.Group controlId="crm">
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

                                        <Form.Group controlId="letter">
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

function mapStateToProps(state) {
    return {
        isRequestingDemo: state.auth.isRequestingDemo,
    };
}
export default connect(mapStateToProps)(GetStarted);
